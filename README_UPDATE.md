# Home Assistant Aktien Apps

## Aktueller Stand
- App: `aktien_finnhub_intraday`
- Version: `1.0.8`
- Datenquelle: Finnhub WebSocket
- Livepfad: Register `006` / `NVDA`
- SQLite/WAL: `/share/aktien_intraday/active/intraday.sqlite3`
- Exporte: `10s`, `30s`, `1m`, `5m`, `15m`, `30m`, `1h`, `4h`

## 1.0.8
- Finnhub-Token kann sicher ueber die App-Konfiguration (`finnhub_api_key`) bereitgestellt werden.
- `service.py` liest zuerst `/data/options.json`; bestehender `secrets.yaml`-Fallback bleibt erhalten.
- Kein Token wird in GitHub, README oder Quellcode eingebettet.
- S6-Startvertrag aus 1.0.7 bleibt erhalten: kein eigener Docker-ENTRYPOINT, `init: false`, `CMD ["/run.sh"]`.
- Read-Timeout-Fix bleibt erhalten.
- Tick-, SQLite/WAL-, Kerzen-, Export- und Retentionslogik bleiben unveraendert.
- Register 009/010 ohne Livefreigabe; automatische Orders gesperrt.
