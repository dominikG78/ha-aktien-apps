# Home Assistant Aktien Apps

Repository fuer den isolierten Finnhub-Intraday-Dienst des Aktienprojekts.

## Aktueller Stand

- App: `aktien_finnhub_intraday`
- Version: `1.0.1`
- Datenquelle: Finnhub WebSocket
- Testinstrument: Register-ID `006`, Symbol `NVDA`
- Speicherung: SQLite/WAL unter `/share/aktien_intraday/active/intraday.sqlite3`
- Exporte: 10s, 30s, 1m, 5m, 15m, 30m, 1h und 4h

Version 1.0.1 korrigiert den WebSocket-Handshake, validiert `Sec-WebSocket-Accept` nach RFC 6455 und liefert genaue HTTP-Fehlercodes. Die App bleibt auf manuellem Start und ohne Watchdog.
