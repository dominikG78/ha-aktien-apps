## 1.0.9
- Verifizierten Read-Timeout-Fix aus der belegten Reparaturquelle produktiv uebernommen.
- `socket.timeout`/`TimeoutError` wird im Empfangspfad als `__IDLE_TIMEOUT__` behandelt und fuehrt nicht mehr automatisch zum Reconnect.
- Token bleibt lokale geschuetzte App-Option; kein Token im Repository.
- S6-Startvertrag aus 1.0.7/1.0.8 bleibt erhalten: kein eigener Docker-ENTRYPOINT, `init: false`, `CMD ["/run.sh"]`.
- Tick-, SQLite/WAL-, Candle-, Export- und Retentionsvertrag unveraendert.
- Register 006/NVDA bleibt einziger freigegebener Finnhub-Livepfad; keine automatischen Orders.
