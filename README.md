# Home Assistant Aktien Apps

## Aktien Finnhub Intraday 1.0.10
- Register-ID `006`, Symbol `NVDA`, NASDAQ, USD
- Geschuetzte lokale App-Option fuer den Finnhub-Key
- Tokenuebergabe nur fluechtig von `bashio::config` an den App-Prozess
- Verifizierte Read-Timeout-Leerlaufbehandlung
- SQLite/WAL unter `/share/aktien_intraday/active/intraday.sqlite3`
- Exporte: 10s, 30s, 1m, 5m, 15m, 30m, 1h und 4h
- Keine automatischen Orders; 009/010 bleiben ohne Livefreigabe
