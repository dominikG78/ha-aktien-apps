# Home Assistant Aktien Apps

Repository fuer den isolierten Finnhub-Intraday-Dienst des Aktienprojekts.

## Aktueller Stand
- App: `aktien_finnhub_intraday`
- Version: `1.0.9`
- Datenquelle: Finnhub WebSocket
- Testinstrument: Register-ID `006`, Symbol `NVDA`, NASDAQ, USD
- Speicherung: SQLite/WAL unter `/share/aktien_intraday/active/intraday.sqlite3`
- Exporte: 10s, 30s, 1m, 5m, 15m, 30m, 1h und 4h
- Token: ausschliesslich lokale geschuetzte App-Option, niemals im Repository

### 1.0.9
Verifizierter Read-Timeout-Fix: nachrichtenarme Phasen werden als Leerlauf behandelt, ohne die WebSocket-Verbindung automatisch als defekt zu bewerten. Startvertrag, SQLite/WAL, Candle-, Export- und Retentionslogik bleiben unveraendert.
