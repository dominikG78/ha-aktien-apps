#!/usr/bin/env python3
import base64, hashlib, json, os, shutil, socket, sqlite3, ssl, struct, time, urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path('/share/aktien_intraday'); ACTIVE=ROOT/'active'; STATUS=ROOT/'status'; EXPORT=ROOT/'exports'; ARCHIVE=ROOT/'archive'
for p in (ACTIVE,STATUS,EXPORT,ARCHIVE): p.mkdir(parents=True,exist_ok=True)

def opt(name,default):
 p=Path('/data/options.json')
 try:return json.loads(p.read_text()).get(name,default)
 except:return default
CFG={k:opt(k,v) for k,v in {'enabled':False,'instrument_id':'006','symbol':'NVDA','exchange':'NASDAQ','currency':'USD','retention_raw_days':90,'export_points':1200,'warn_free_gb':100,'stop_free_gb':50}.items()}

def token():
 p=Path('/config/secrets.yaml')
 if not p.exists(): return ''
 for line in p.read_text(errors='ignore').splitlines():
  if line.strip().lower().startswith(('finnhub_api_key:','finnhub_token:')):
   return line.split(':',1)[1].strip().strip('"\'')
 return ''
TOKEN=token()
INTERVALS={'10s':10,'30s':30,'1m':60,'5m':300,'15m':900,'30m':1800,'1h':3600,'4h':14400}
DB=sqlite3.connect(ACTIVE/'intraday.sqlite3',timeout=30)
DB.execute('PRAGMA journal_mode=WAL'); DB.execute('PRAGMA synchronous=NORMAL')
DB.executescript('''CREATE TABLE IF NOT EXISTS ticks(instrument_id TEXT,symbol TEXT,source TEXT,event_ms INTEGER,received_ms INTEGER,price REAL,volume REAL,conditions TEXT,quality TEXT,PRIMARY KEY(instrument_id,source,event_ms,price,volume));CREATE INDEX IF NOT EXISTS ticks_t ON ticks(instrument_id,event_ms);CREATE TABLE IF NOT EXISTS candles(instrument_id TEXT,interval_s INTEGER,bucket_ms INTEGER,open REAL,high REAL,low REAL,close REAL,volume REAL,samples INTEGER,first_ms INTEGER,last_ms INTEGER,source TEXT,quality TEXT,PRIMARY KEY(instrument_id,interval_s,bucket_ms,source));CREATE INDEX IF NOT EXISTS candles_t ON candles(instrument_id,interval_s,bucket_ms);'''); DB.commit()

def atomic(p,obj):
 t=p.with_suffix(p.suffix+'.tmp'); t.write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':'))); os.replace(t,p)
def stat(state,error=''):
 du=shutil.disk_usage('/share'); data={'status':state,'updated_utc':datetime.now(timezone.utc).isoformat(),'instrument_id':CFG['instrument_id'],'symbol':CFG['symbol'],'source':'FINNHUB_WEBSOCKET','enabled':bool(CFG['enabled']),'error':error[:250],'free_gb':round(du.free/2**30,2),'db_bytes':(ACTIVE/'intraday.sqlite3').stat().st_size if (ACTIVE/'intraday.sqlite3').exists() else 0}
 row=DB.execute('SELECT COUNT(*),MAX(event_ms),MAX(received_ms),MAX(price) FROM ticks').fetchone(); data.update({'tick_count':row[0],'last_event_ms':row[1],'last_received_ms':row[2],'last_price':row[3]})
 atomic(STATUS/'service_status.json',data)
def add_tick(d):
 try:p=float(d['p']); em=int(d['t']); vol=float(d.get('v') or 0)
 except:return
 if p<=0 or em<=0:return
 rm=int(time.time()*1000); cond=json.dumps(d.get('c') or [],separators=(',',':'))
 cur=DB.execute('INSERT OR IGNORE INTO ticks VALUES(?,?,?,?,?,?,?,?,?)',(CFG['instrument_id'],CFG['symbol'],'FINNHUB_WEBSOCKET',em,rm,p,vol,cond,'LIVE'))
 if not cur.rowcount:return
 for sec in INTERVALS.values():
  b=(em//(sec*1000))*(sec*1000)
  r=DB.execute('SELECT high,low,volume,samples,first_ms,last_ms FROM candles WHERE instrument_id=? AND interval_s=? AND bucket_ms=? AND source=?',(CFG['instrument_id'],sec,b,'FINNHUB_WEBSOCKET')).fetchone()
  if r: DB.execute('UPDATE candles SET high=?,low=?,close=?,volume=?,samples=?,last_ms=? WHERE instrument_id=? AND interval_s=? AND bucket_ms=? AND source=?',(max(r[0],p),min(r[1],p),p,r[2]+vol,r[3]+1,max(r[5],em),CFG['instrument_id'],sec,b,'FINNHUB_WEBSOCKET'))
  else: DB.execute('INSERT INTO candles VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(CFG['instrument_id'],sec,b,p,p,p,p,vol,1,em,em,'FINNHUB_WEBSOCKET','LIVE'))
 DB.commit(); export_all()
def export_all():
 for name,sec in INTERVALS.items():
  rows=DB.execute('SELECT bucket_ms,open,high,low,close,volume,samples,quality FROM candles WHERE instrument_id=? AND interval_s=? ORDER BY bucket_ms DESC LIMIT ?',(CFG['instrument_id'],sec,int(CFG['export_points']))).fetchall()[::-1]
  atomic(EXPORT/f"chart_{CFG['instrument_id']}_{name}.json",{'status':'OK','instrument_id':CFG['instrument_id'],'symbol':CFG['symbol'],'interval':name,'source':'FINNHUB_WEBSOCKET','count':len(rows),'updated_utc':datetime.now(timezone.utc).isoformat(),'candles':[{'t':r[0],'o':r[1],'h':r[2],'l':r[3],'c':r[4],'v':r[5],'samples':r[6],'quality':r[7]} for r in rows]})
def purge():
 cut=int((time.time()-int(CFG['retention_raw_days'])*86400)*1000); DB.execute('DELETE FROM ticks WHERE event_ms<?',(cut,)); DB.commit()
class WS:
 def __init__(self,url):self.url=url;self.s=None
 def connect(self):
  u=urllib.parse.urlparse(self.url); raw=socket.create_connection((u.hostname,u.port or 443),20); self.s=ssl.create_default_context().wrap_socket(raw,server_hostname=u.hostname)
  key=base64.b64encode(os.urandom(16)).decode(); path=u.path+('?' + u.query if u.query else '')
  req=f'GET {path} HTTP/1.1\r\nHost: {u.hostname}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'; self.s.sendall(req.encode()); resp=b''
  while b'\r\n\r\n' not in resp:resp+=self.s.recv(4096)
  if b' 101 ' not in resp.split(b'\r\n',1)[0]:raise RuntimeError('WEBSOCKET_HANDSHAKE_FEHLER')
 def send(self,obj):
  b=json.dumps(obj,separators=(',',':')).encode(); mask=os.urandom(4); hdr=bytes([129,128|len(b)]) if len(b)<126 else bytes([129,128|126])+struct.pack('!H',len(b)); self.s.sendall(hdr+mask+bytes(x^mask[i%4] for i,x in enumerate(b)))
 def recv(self):
  h=self._read(2); op=h[0]&15; n=h[1]&127
  if n==126:n=struct.unpack('!H',self._read(2))[0]
  elif n==127:n=struct.unpack('!Q',self._read(8))[0]
  payload=self._read(n)
  if op==8:raise RuntimeError('WEBSOCKET_GESCHLOSSEN')
  if op==9:self.send_raw(10,payload);return None
  return payload.decode(errors='replace') if op==1 else None
 def send_raw(self,op,payload):self.s.sendall(bytes([128|op,len(payload)])+payload)
 def _read(self,n):
  b=b''
  while len(b)<n:
   x=self.s.recv(n-len(b))
   if not x:raise RuntimeError('VERBINDUNG_ABGEBROCHEN')
   b+=x
  return b

def main():
 if not CFG['enabled']:stat('INSTALLIERT_DEAKTIVIERT'); time.sleep(2); return
 if not TOKEN:stat('GESPERRT','FINNHUB_TOKEN_FEHLT'); raise SystemExit(2)
 while True:
  try:
   free=shutil.disk_usage('/share').free/2**30
   if free<float(CFG['stop_free_gb']):stat('GESPERRT','SPEICHER_UNTER_STOPPGRENZE');time.sleep(60);continue
   stat('VERBINDET'); w=WS('wss://ws.finnhub.io?token='+urllib.parse.quote(TOKEN));w.connect();w.send({'type':'subscribe','symbol':CFG['symbol']});stat('STREAM_AKTIV')
   last=time.time()
   while True:
    msg=w.recv()
    if msg:
     obj=json.loads(msg)
     if obj.get('type')=='trade':
      for d in obj.get('data',[]):
       if d.get('s')==CFG['symbol']:add_tick(d)
    if time.time()-last>30:stat('STREAM_AKTIV');purge();last=time.time()
  except Exception as e:stat('VERBINDUNGSFEHLER',type(e).__name__+':'+str(e));time.sleep(10)
if __name__=='__main__':main()
