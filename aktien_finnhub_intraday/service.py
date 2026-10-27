#!/usr/bin/env python3

import json
import os
import sqlite3
import time

from datetime import datetime, timezone
from pathlib import Path

INTERVALS = {
    "30s": 30,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
    "4h": 14400,
}

APP_VERSION = "1.1.5"
BUILD_MARKER = "AP5_IMAGE_INTERNAL_INSTRUMENTS_V2"
INSTRUMENTS_FILE = Path("/opt/aktien/instruments.json")


class WriterIsolationError(RuntimeError):
    pass

def atomic_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':'))); os.replace(tmp,path)
class RegisterWriter:
    def __init__(self,root,instrument):
        self.rid=instrument['instrument_id']; self.instrument=instrument
        self.db_path=root/'db'/self.rid/'intraday.sqlite3'; self.export_root=root/'exports_v2'/self.rid
        self.db_path.parent.mkdir(parents=True,exist_ok=True); self.export_root.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(self.db_path,timeout=30); self.db.execute('PRAGMA journal_mode=WAL'); self.db.execute('PRAGMA synchronous=NORMAL')
        self.db.executescript('''CREATE TABLE IF NOT EXISTS ticks(instrument_id TEXT,symbol TEXT,source TEXT,event_ms INTEGER,received_ms INTEGER,price REAL,volume REAL,quality TEXT,PRIMARY KEY(instrument_id,source,event_ms,price,volume));CREATE INDEX IF NOT EXISTS ticks_t ON ticks(event_ms);CREATE TABLE IF NOT EXISTS candles(instrument_id TEXT,interval_s INTEGER,bucket_ms INTEGER,open REAL,high REAL,low REAL,close REAL,volume REAL,samples INTEGER,first_ms INTEGER,last_ms INTEGER,source TEXT,quality TEXT,PRIMARY KEY(instrument_id,interval_s,bucket_ms,source));CREATE INDEX IF NOT EXISTS candles_t ON candles(interval_s,bucket_ms);'''); self.db.commit()
    def add_tick(self,tick):
        if tick['instrument_id']!=self.rid: raise WriterIsolationError(f"{tick['instrument_id']}->{self.rid}")

        cur=self.db.execute('INSERT OR IGNORE INTO ticks VALUES(?,?,?,?,?,?,?,?)',(self.rid,tick['symbol'],tick['source'],tick['event_ms'],tick['received_ms'],tick['price'],tick['volume'],tick['quality']))
        if not cur.rowcount:return
        for _,sec in INTERVALS.items():
            b=(tick['event_ms']//(sec*1000))*(sec*1000)
            row=self.db.execute('SELECT high,low,volume,samples,last_ms FROM candles WHERE instrument_id=? AND interval_s=? AND bucket_ms=? AND source=?',(self.rid,sec,b,tick['source'])).fetchone()
            if row:self.db.execute('UPDATE candles SET high=?,low=?,close=?,volume=?,samples=?,last_ms=? WHERE instrument_id=? AND interval_s=? AND bucket_ms=? AND source=?',(max(row[0],tick['price']),min(row[1],tick['price']),tick['price'],row[2]+tick['volume'],row[3]+1,max(row[4],tick['event_ms']),self.rid,sec,b,tick['source']))
            else:self.db.execute('INSERT INTO candles VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(self.rid,sec,b,tick['price'],tick['price'],tick['price'],tick['price'],tick['volume'],1,tick['event_ms'],tick['event_ms'],tick['source'],tick['quality']))
        self.db.commit(); self.export()
    def export(self):
        for name,sec in INTERVALS.items():
            rows=self.db.execute('SELECT bucket_ms,open,high,low,close,volume,samples,first_ms,last_ms,quality FROM candles WHERE instrument_id=? AND interval_s=? ORDER BY bucket_ms DESC LIMIT 1200',(self.rid,sec)).fetchall()[::-1]
            atomic_json(self.export_root/f'{name}.json',{'schema_version':2,'status':'OK' if rows else 'NO_DATA','instrument_id':self.rid,'symbol':self.instrument['symbol'],'exchange':self.instrument['exchange'],'currency':self.instrument['currency'],'interval':name,'source':'FINNHUB_WEBSOCKET','quality':'LIVE' if rows else 'UNKNOWN','updated_utc':datetime.now(timezone.utc).isoformat(),'count':len(rows),'candles':[{'bucket_ms':r[0],'open':r[1],'high':r[2],'low':r[3],'close':r[4],'volume':r[5],'samples':r[6],'first_ms':r[7],'last_ms':r[8]} for r in rows]})
class WriterManager:
    def __init__(self,root,instruments): self.root=root; self.instruments=instruments; self.writers={}
    def get(self,rid):
        if rid not in self.instruments or not self.instruments[rid]['enabled']: raise WriterIsolationError(f'RID_NOT_ENABLED:{rid}')
        if rid not in self.writers:self.writers[rid]=RegisterWriter(self.root,self.instruments[rid])
        return self.writers[rid]
def load_config():
    options = json.loads(Path("/data/options.json").read_text())
    root = Path(options["data_root"])
    payload = json.loads(
        INSTRUMENTS_FILE.read_text()
    )
    instruments = {
        rid: dict(cfg, instrument_id=rid)
        for rid, cfg in payload["instruments"].items()
    }
    if set(instruments) != set(f"{i:03d}" for i in range(1, 21)):
        raise SystemExit("INSTRUMENT_SET_INVALID")
    return options, root, instruments
def main():
    print(
        "AP5_START "
        f"version={APP_VERSION} "
        f"build={BUILD_MARKER} "
        f"instruments={INSTRUMENTS_FILE}",
        flush=True,
    )

    options, root, instruments = load_config()

    status_root = root / "status"
    status_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    atomic_json(
        status_root / "collector.json",
        {
            "schema_version": 2,
            "status": (
                "INSTALLIERT_DEAKTIVIERT"
                if not options["enabled"]
                else "BEREIT"
            ),
            "version": APP_VERSION,
            "build_marker": BUILD_MARKER,
            "instruments_file": str(INSTRUMENTS_FILE),
            "data_root": str(root),
            "updated_utc": datetime.now(timezone.utc).isoformat(),
            "active_instruments": sum(
                1
                for instrument in instruments.values()
                if instrument["enabled"]
                and instrument["live_enabled"]
            ),
            "available_intervals": list(INTERVALS),
        },
    )

    if not options["enabled"]:
        while True:
            time.sleep(3600)

    raise SystemExit(
        "PROVIDER_START_BLOCKED_PENDING_AP5_RUNTIME_RELEASE"
    )


if __name__ == "__main__":
    main()
