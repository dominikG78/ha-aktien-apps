# Home Assistant Aktien Apps

Repository für den isolierten Finnhub-Intraday-Dienst des Aktienprojekts.

## Aktueller produktiver Stand

- App: `aktien_finnhub_intraday`
- Version: `1.0.4`
- Datenquelle: Finnhub WebSocket
- Testinstrument: Register-ID `006`, Symbol `NVDA`
- Handelsplatz: `NASDAQ`
- Währung: `USD`
- Speicherung: SQLite/WAL unter `/share/aktien_intraday/active/intraday.sqlite3`
- Retention Rohdaten: `90 Tage`
- Exportpunkte: `1200`
- Exporte: `10s`, `30s`, `1m`, `5m`, `15m`, `30m`, `1h` und `4h`

## 1.0.4

- Read-Timeout wird als WebSocket-Leerlauf behandelt und löst nicht mehr automatisch einen Verbindungsabbruch aus.
- Bestehende WebSocket-Verbindung bleibt während nachrichtenarmer Phasen erhalten.
- Tick-, SQLite-/WAL-, Kerzen-, Export- und Retentionslogik bleiben unverändert.
- Register-ID `006` / `NVDA` bleibt der freigegebene Finnhub-Livepfad.
- Keine automatischen Orders.
