# Publish 1.1.0

## Repository

Zielstruktur:

- `repository.yaml` auf Repository-Ebene.
- `aktien_finnhub_intraday/` mit `config.yaml`, `Dockerfile`, `build.yaml`, `run.sh`, `service.py`, `instruments.json`, `README.md`, `DOCS.md`, `CHANGELOG.md`.

## Gates

- Keine Tokens oder Laufzeitdaten committen.
- Keine SQLite-, WAL-, SHM-, Export-, Status-, Historien- oder Migrationsdaten committen.
- Vor Publish Manifest und statisches AP5-Gate pruefen.
- Nach Publish muss Version 1.1.0 im Repository/App-Updatepfad sichtbar sein.
- App zunaechst mit `enabled: false` bauen/aktualisieren.
- Kein Home-Assistant-Core-Neustart als Bestandteil des Publish-Schritts.
