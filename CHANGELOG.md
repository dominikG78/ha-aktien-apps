## 1.0.10
- Behebt den belegten Startabbruch `FINNHUB_TOKEN_FEHLT`, obwohl die Supervisor-Option gesetzt ist.
- `run.sh` liest die geschuetzte App-Option mit `bashio::config` und uebergibt sie nur fluechtig als Prozessumgebungsvariable.
- `service.py` nutzt diese Umgebungsvariable als letzten Fallback vor dem bestehenden Token-Gate.
- Der verifizierte `__IDLE_TIMEOUT__`-Fix bleibt enthalten.
- Kein Token im Repository, Manifest, Log oder Austauschpaket.
- SQLite/WAL, Candle-, Export-, Retentions- und Registervertrag bleiben unveraendert.
