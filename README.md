# Aktien Finnhub Intraday 1.1.0

Generischer AP5 Multi-Instrument-Collector fuer die Register 001 bis 020.

## Architektur

- Persistenter Datenroot: `/media/COPILOT_DATA/aktien/intraday`
- Registergetrennte SQLite-Pfade: `db/<RID>/intraday.sqlite3`
- Registergetrennte V2-Exporte: `exports_v2/<RID>/<INTERVALL>.json`
- Produktionsintervalle: `30s`, `5m`, `15m`, `1h`, `4h`
- Instrumentenkonfiguration: `instruments.json`
- Providerstart bleibt bis zur AP5-Runtime-Freigabe gesperrt.

## Schutz

Version 1.1.0 veraendert nicht automatisch:

- `/share/aktien_intraday`
- `migration_20261027`
- historische Kursdaten
- Home-Assistant `.storage`

Legacy-Bereinigung ist nicht Bestandteil dieses Releases.
