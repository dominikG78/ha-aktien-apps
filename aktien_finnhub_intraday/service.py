#!/usr/bin/env python3
import base64
import hashlib
import json
import os
import shutil
import socket
import sqlite3
import ssl
import struct
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

APP_VERSION = "1.2.0"
BUILD_MARKER = "AP5_FINNHUB_MULTI_PROVIDER_V1"
INSTRUMENTS_FILE = Path("/opt/aktien/instruments.json")
INTERVALS = {"30s": 30, "5m": 300, "15m": 900, "1h": 3600, "4h": 14400}
SOURCE = "FINNHUB_WEBSOCKET"

class WriterIsolationError(RuntimeError):
    pass

def atomic_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))
    os.replace(tmp, path)

class RegisterWriter:
    def __init__(self, root, instrument, export_points):
        self.rid = instrument["instrument_id"]
        self.instrument = instrument
        self.export_points = export_points
        self.db_path = root / "db" / self.rid / "intraday.sqlite3"
        self.export_root = root / "exports_v2" / self.rid
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.export_root.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.db_path, timeout=30)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=NORMAL")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS ticks(
            instrument_id TEXT, symbol TEXT, source TEXT,
            event_ms INTEGER, received_ms INTEGER,
            price REAL, volume REAL, quality TEXT,
            PRIMARY KEY(instrument_id,source,event_ms,price,volume)
        );
        CREATE INDEX IF NOT EXISTS ticks_t ON ticks(event_ms);
        CREATE TABLE IF NOT EXISTS candles(
            instrument_id TEXT, interval_s INTEGER, bucket_ms INTEGER,
            open REAL, high REAL, low REAL, close REAL,
            volume REAL, samples INTEGER, first_ms INTEGER, last_ms INTEGER,
            source TEXT, quality TEXT,
            PRIMARY KEY(instrument_id,interval_s,bucket_ms,source)
        );
        CREATE INDEX IF NOT EXISTS candles_t ON candles(interval_s,bucket_ms);
        """)
        self.db.commit()

    def add_tick(self, tick):
        if tick["instrument_id"] != self.rid:
            raise WriterIsolationError(f"{tick['instrument_id']}->{self.rid}")
        cur = self.db.execute(
            "INSERT OR IGNORE INTO ticks VALUES(?,?,?,?,?,?,?,?)",
            (self.rid, tick["symbol"], tick["source"], tick["event_ms"],
             tick["received_ms"], tick["price"], tick["volume"], tick["quality"]),
        )
        if not cur.rowcount:
            return
        for sec in INTERVALS.values():
            bucket_ms = (tick["event_ms"] // (sec * 1000)) * (sec * 1000)
            row = self.db.execute(
                "SELECT high,low,volume,samples,last_ms FROM candles WHERE instrument_id=? AND interval_s=? AND bucket_ms=? AND source=?",
                (self.rid, sec, bucket_ms, tick["source"]),
            ).fetchone()
            if row:
                self.db.execute(
                    "UPDATE candles SET high=?,low=?,close=?,volume=?,samples=?,last_ms=? WHERE instrument_id=? AND interval_s=? AND bucket_ms=? AND source=?",
                    (max(row[0], tick["price"]), min(row[1], tick["price"]), tick["price"],
                     row[2] + tick["volume"], row[3] + 1, max(row[4], tick["event_ms"]),
                     self.rid, sec, bucket_ms, tick["source"]),
                )
            else:
                self.db.execute(
                    "INSERT INTO candles VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (self.rid, sec, bucket_ms, tick["price"], tick["price"], tick["price"],
                     tick["price"], tick["volume"], 1, tick["event_ms"], tick["event_ms"],
                     tick["source"], tick["quality"]),
                )
        self.db.commit()
        self.export()

    def export(self):
        for name, sec in INTERVALS.items():
            rows = self.db.execute(
                "SELECT bucket_ms,open,high,low,close,volume,samples,first_ms,last_ms,quality FROM candles WHERE instrument_id=? AND interval_s=? ORDER BY bucket_ms DESC LIMIT ?",
                (self.rid, sec, self.export_points),
            ).fetchall()[::-1]
            atomic_json(
                self.export_root / f"{name}.json",
                {
                    "schema_version": 2,
                    "status": "OK" if rows else "NO_DATA",
                    "instrument_id": self.rid,
                    "symbol": self.instrument["symbol"],
                    "exchange": self.instrument["exchange"],
                    "currency": self.instrument["currency"],
                    "interval": name,
                    "source": SOURCE,
                    "quality": "LIVE" if rows else "UNKNOWN",
                    "updated_utc": datetime.now(timezone.utc).isoformat(),
                    "count": len(rows),
                    "candles": [
                        {"bucket_ms": r[0], "open": r[1], "high": r[2], "low": r[3],
                         "close": r[4], "volume": r[5], "samples": r[6],
                         "first_ms": r[7], "last_ms": r[8]}
                        for r in rows
                    ],
                },
            )

    def purge(self, retention_days):
        cutoff = int((time.time() - retention_days * 86400) * 1000)
        self.db.execute("DELETE FROM ticks WHERE event_ms<?", (cutoff,))
        self.db.commit()

class WriterManager:
    def __init__(self, root, instruments, export_points):
        self.root = root
        self.instruments = instruments
        self.export_points = export_points
        self.writers = {}

    def get(self, rid):
        instrument = self.instruments.get(rid)
        if not instrument or not instrument["enabled"] or not instrument["live_enabled"]:
            raise WriterIsolationError(f"RID_NOT_LIVE_ENABLED:{rid}")
        if rid not in self.writers:
            self.writers[rid] = RegisterWriter(self.root, instrument, self.export_points)
        return self.writers[rid]

    def close_all(self):
        for writer in self.writers.values():
            try:
                writer.db.close()
            except Exception:
                pass

class WebSocketClient:
    def __init__(self, token):
        self.url = "wss://ws.finnhub.io?token=" + urllib.parse.quote(token)
        self.sock = None

    def _read_exact(self, n):
        data = b""
        while len(data) < n:
            chunk = self.sock.recv(n - len(data))
            if not chunk:
                raise RuntimeError("WEBSOCKET_CONNECTION_CLOSED")
            data += chunk
        return data

    def connect(self):
        parsed = urllib.parse.urlparse(self.url)
        raw = socket.create_connection((parsed.hostname, parsed.port or 443), timeout=20)
        self.sock = ssl.create_default_context().wrap_socket(raw, server_hostname=parsed.hostname)
        self.sock.settimeout(35)
        key = base64.b64encode(os.urandom(16)).decode()
        path = (parsed.path or "/") + ("?" + parsed.query if parsed.query else "")
        request = (
            f"GET {path} HTTP/1.1\r\nHost: {parsed.hostname}\r\nUpgrade: websocket\r\n"
            f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n"
            "User-Agent: HA-AKT-FINNHUB/1.2.0\r\nOrigin: https://finnhub.io\r\n\r\n"
        )
        self.sock.sendall(request.encode())
        response = b""
        while b"\r\n\r\n" not in response and len(response) < 65536:
            response += self.sock.recv(4096)
        header = response.partition(b"\r\n\r\n")[0].decode(errors="replace").split("\r\n")
        if not header or " 101 " not in (" " + header[0] + " "):
            raise RuntimeError("WEBSOCKET_HANDSHAKE_FAILED")
        accept = ""
        for line in header[1:]:
            if line.lower().startswith("sec-websocket-accept:"):
                accept = line.split(":", 1)[1].strip()
                break
        expected = base64.b64encode(hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()).decode()
        if accept != expected:
            raise RuntimeError("WEBSOCKET_ACCEPT_INVALID")

    def send_json(self, obj):
        payload = json.dumps(obj, separators=(",", ":")).encode()
        mask = os.urandom(4)
        n = len(payload)
        if n < 126:
            header = bytes([0x81, 0x80 | n])
        elif n < 65536:
            header = bytes([0x81, 0x80 | 126]) + struct.pack("!H", n)
        else:
            header = bytes([0x81, 0x80 | 127]) + struct.pack("!Q", n)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(header + mask + masked)

    def recv_text(self):
        first = self._read_exact(2)
        opcode = first[0] & 0x0F
        length = first[1] & 0x7F
        masked = bool(first[1] & 0x80)
        if length == 126:
            length = struct.unpack("!H", self._read_exact(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", self._read_exact(8))[0]
        mask = self._read_exact(4) if masked else None
        payload = self._read_exact(length) if length else b""
        if mask:
            payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        if opcode == 0x8:
            raise RuntimeError("WEBSOCKET_CLOSED")
        if opcode == 0x9:
            self._send_control(0xA, payload)
            return None
        if opcode != 0x1:
            return None
        return payload.decode(errors="replace")

    def _send_control(self, opcode, payload=b""):
        mask = os.urandom(4)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(bytes([0x80 | opcode, 0x80 | len(payload)]) + mask + masked)

    def close(self):
        try:
            if self.sock:
                self.sock.close()
        except Exception:
            pass

def load_config():
    options = json.loads(Path("/data/options.json").read_text())
    root = Path(options["data_root"])
    payload = json.loads(INSTRUMENTS_FILE.read_text())
    instruments = {rid: dict(cfg, instrument_id=rid) for rid, cfg in payload["instruments"].items()}
    expected = {f"{i:03d}" for i in range(1, 21)}
    if set(instruments) != expected:
        raise SystemExit("INSTRUMENT_SET_INVALID")
    active = {
        rid: item for rid, item in instruments.items()
        if item["enabled"] and item["live_enabled"] and item["live_provider"] == "FINNHUB"
    }
    symbols = [item["symbol"] for item in active.values()]
    if any(not symbol for symbol in symbols) or len(symbols) != len(set(symbols)):
        raise SystemExit("ACTIVE_SYMBOL_SET_INVALID")
    return options, root, instruments, active

def write_collector_status(root, state, active, error=""):
    atomic_json(
        root / "status" / "collector.json",
        {
            "schema_version": 2,
            "status": state,
            "version": APP_VERSION,
            "build_marker": BUILD_MARKER,
            "instruments_file": str(INSTRUMENTS_FILE),
            "data_root": str(root),
            "updated_utc": datetime.now(timezone.utc).isoformat(),
            "active_instruments": len(active),
            "active_registers": sorted(active),
            "available_intervals": list(INTERVALS),
            "error": error[:250],
        },
    )

def main():
    print(
        f"AP5_START version={APP_VERSION} build={BUILD_MARKER} instruments={INSTRUMENTS_FILE}",
        flush=True,
    )
    options, root, instruments, active = load_config()
    (root / "status").mkdir(parents=True, exist_ok=True)
    if not options["enabled"]:
        write_collector_status(root, "INSTALLIERT_DEAKTIVIERT", active)
        while True:
            time.sleep(3600)

    token = (os.environ.get("FINNHUB_API_KEY", "") or os.environ.get("FINNHUB_TOKEN", "")).strip()
    if not token:
        write_collector_status(root, "GESPERRT", active, "FINNHUB_TOKEN_FEHLT")
        raise SystemExit(2)

    symbol_to_rid = {item["symbol"]: rid for rid, item in active.items()}
    manager = WriterManager(root, instruments, int(options["export_points"]))
    retention_days = int(options["retention_raw_days"])
    reconnect_delay = 10

    while True:
        ws = WebSocketClient(token)
        try:
            free_gb = shutil.disk_usage("/media").free / (1024 ** 3)
            if free_gb < float(options["stop_free_gb"]):
                write_collector_status(root, "GESPERRT", active, "SPEICHER_UNTER_STOPPGRENZE")
                time.sleep(60)
                continue

            write_collector_status(root, "VERBINDET", active)
            ws.connect()
            for symbol in symbol_to_rid:
                ws.send_json({"type": "subscribe", "symbol": symbol})
            write_collector_status(root, "STREAM_AKTIV", active)
            print("AP5_SUBSCRIPTIONS " + ",".join(f"{rid}:{active[rid]['symbol']}" for rid in sorted(active)), flush=True)
            last_maintenance = time.time()

            while True:
                try:
                    text = ws.recv_text()
                except socket.timeout:
                    text = None
                if text:
                    message = json.loads(text)
                    if message.get("type") == "trade":
                        for trade in message.get("data", []):
                            symbol = trade.get("s")
                            rid = symbol_to_rid.get(symbol)
                            if not rid:
                                continue
                            try:
                                price = float(trade["p"])
                                event_ms = int(trade["t"])
                                volume = float(trade.get("v") or 0)
                            except (KeyError, TypeError, ValueError):
                                continue
                            if price <= 0 or event_ms <= 0:
                                continue
                            manager.get(rid).add_tick(
                                {
                                    "instrument_id": rid,
                                    "symbol": symbol,
                                    "source": SOURCE,
                                    "event_ms": event_ms,
                                    "received_ms": int(time.time() * 1000),
                                    "price": price,
                                    "volume": volume,
                                    "quality": "LIVE",
                                }
                            )
                if time.time() - last_maintenance >= 60:
                    for writer in manager.writers.values():
                        writer.purge(retention_days)
                    write_collector_status(root, "STREAM_AKTIV", active)
                    last_maintenance = time.time()

        except Exception as exc:
            write_collector_status(root, "VERBINDUNGSFEHLER", active, f"{type(exc).__name__}:{exc}")
            print(f"AP5_PROVIDER_ERROR {type(exc).__name__}:{exc}", flush=True)
            time.sleep(reconnect_delay)
        finally:
            ws.close()

if __name__ == "__main__":
    main()
