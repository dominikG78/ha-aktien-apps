## 1.0.6
- Container-Init-Kollision korrigiert: Supervisor-Init deaktiviert (`init: false`), waehrend der belegte s6-Startvertrag des Images `ENTRYPOINT ["/init"]` und `CMD ["/run.sh"]` erhalten bleibt.
- Read-Timeout-Fix aus 1.0.4/1.0.5 bleibt in `service.py` erhalten.
- `homeassistant_config` wird read-only eingebunden; `share` bleibt read-write.
- Tick-, SQLite/WAL-, Candle-, Export- und Retentionsvertrag bleiben unveraendert.
- Register 006/NVDA bleibt der einzige freigegebene Finnhub-Livepfad; 009/010 und Orders bleiben gesperrt.
