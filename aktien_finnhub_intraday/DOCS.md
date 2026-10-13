# Aktien Finnhub Intraday

Isolierter Dienst fuer Finnhub-WebSocket, SQLite/WAL und OHLC-Kerzen.

## Laufzeitpfade

- SQLite: `/share/aktien_intraday/active/intraday.sqlite3`
- Status: `/share/aktien_intraday/status/service_status.json`
- Exporte: `/share/aktien_intraday/exports/chart_<instrument_id>_<intervall>.json`
- Secret: `/config/secrets.yaml`, Schluessel `finnhub_api_key` oder `finnhub_token`

## Version 1.0.1

Der WebSocket-Handshake sendet einen definierten User-Agent und Origin-Header. HTTP-Status und `Sec-WebSocket-Accept` werden explizit validiert. Fehler werden differenziert als fehlende Antwort, zu grosser Header, HTTP-Status oder ungueltiger Accept-Header dokumentiert.

Die App verwendet weiterhin `boot: manual`, keinen Watchdog und keine automatischen Updates. Ein Home-Assistant-Neustart ist fuer ein App-Update nicht erforderlich.
