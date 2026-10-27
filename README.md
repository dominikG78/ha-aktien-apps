# Changelog

## 1.1.0

### Added
- Generische Instrumentenkonfiguration fuer Register 001 bis 020.
- Registerisolierter SQLite-Writer.
- Registerisolierte V2-Exportpfade.
- Persistenter Datenroot unter `/media/COPILOT_DATA/aktien/intraday`.
- Schreibbarer `media`-Mount fuer die App.

### Changed
- Produktive Candle-Intervalle auf `30s`, `5m`, `15m`, `1h` und `4h` standardisiert.
- Writer-Routing erfolgt ueber Registerkonfiguration anstelle einer gemeinsamen neuen SQLite-DB.

### Safety
- Providerstart bleibt bis zur AP5-Runtime-Abnahme gesperrt.
- Bestehender `/share/aktien_intraday`-Bestand bleibt unangetastet.
- `migration_20261027` und historische Daten bleiben geschuetzt.
- Keine Legacy-Loeschung in diesem Release.
