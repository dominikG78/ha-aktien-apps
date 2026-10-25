## 1.0.7
- S6/PID1-Startfehler korrigiert: kein eigener Docker-`ENTRYPOINT`; Home-Assistant-Basisimage behaelt `/init`.
- `init: false` gesetzt, damit S6 direkt Prozess 1 bleibt.
- `CMD ["/run.sh"]` beibehalten.
- Read-Timeout-Fix unveraendert fortgefuehrt.
- Tick-, SQLite/WAL-, Candle-, Export- und Retentionslogik unveraendert.
