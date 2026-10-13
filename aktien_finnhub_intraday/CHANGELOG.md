# Changelog

## 1.0.1

- Finnhub-WebSocket-Handshake an den erfolgreich validierten Upgrade-Request angeglichen
- `User-Agent` und `Origin` im Upgrade-Request ergaenzt
- HTTP-Status des Handshakes explizit ausgewertet
- maximale Handshake-Headergroesse auf 64 KiB begrenzt
- Verbindungsabbruch vor vollstaendigem Header erkannt
- `Sec-WebSocket-Accept` nach RFC 6455 validiert
- bestehende Token-, SQLite-, Daten-, Export- und Retentionslogik unveraendert beibehalten

## 1.0.0

- Finnhub-WebSocket-Test fuer NVDA
- SQLite/WAL
- 10s bis 4h OHLC-Kerzen
- atomare JSON-Exporte
