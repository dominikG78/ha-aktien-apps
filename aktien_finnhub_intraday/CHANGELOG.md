## 1.0.8
- Tokenpfad gehaertet: `finnhub_api_key` als optionale geschuetzte App-Option hinzugefuegt.
- `service.py` liest den Token primaer aus `/data/options.json`, mit bestehendem `secrets.yaml`-Fallback.
- S6/PID1-Startfix und WebSocket-Read-Timeout-Fix unveraendert fortgefuehrt.
