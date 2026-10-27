# Publish AP5 Version 1.1.5

## Repository

Zielstruktur:

- `repository.yaml` auf Repository-Ebene.
- `aktien_finnhub_intraday/` mit:
  - `config.yaml`
  - `Dockerfile`
  - `run.sh`
  - `service.py`
  - `instruments.json`
  - `README.md`
  - `DOCS.md`
  - `CHANGELOG.md`
  - `PUBLISH_INSTRUCTIONS.md`

## Version

Verbindlicher Release-Stand:

`1.1.5`

Die App-Konfiguration muss enthalten:

`version: "1.1.5"`

Die Laufzeitdiagnose in `service.py` verwendet:

`APP_VERSION = "1.1.5"`

Der Build muss beim Start eindeutig ausgeben:

`AP5_START version=1.1.5 build=AP5_IMAGE_INTERNAL_INSTRUMENTS_V2 instruments=/opt/aktien/instruments.json`

## Instrumentenkonfiguration

Die Registerkonfiguration ist Bestandteil des App-Images:

`/opt/aktien/instruments.json`

Der Docker-Build muss enthalten:

`COPY instruments.json /opt/aktien/instruments.json`

`instruments_file` darf nicht mehr als App-Option oder Schemafeld verwendet werden.

Folgende Altpfade bzw. Altlogik dürfen im produktiven AP5-Code nicht mehr vorkommen:

- `/config/instruments.json`
- `options['instruments_file']`
- `options["instruments_file"]`
- `AP5_IMAGE_INTERNAL_INSTRUMENTS_V1`

## Persistente Marktdaten

Produktiver Datenroot:

`/media/COPILOT_DATA/aktien/intraday`

Registerdatenbanken:

`db/<RID>/intraday.sqlite3`

V2-Exporte:

`exports_v2/<RID>/<INTERVALL>.json`

Zulässige Register:

`001` bis `020`

Zulässige Intervalle:

- `30s`
- `5m`
- `15m`
- `1h`
- `4h`

Nicht zulässig:

- `10s`
- `1m`
- `30m`

## Gates

- Keine Tokens oder Laufzeitdaten committen.
- Keine SQLite-, WAL-, SHM-, Export-, Status-, Historien- oder Migrationsdaten committen.
- `service.py` darf kein `&gt;` enthalten.
- `service.py` darf keinen `/config/instruments.json`-Pfad enthalten.
- `service.py` muss den Build-Marker `AP5_IMAGE_INTERNAL_INSTRUMENTS_V2` enthalten.
- `collector.json` muss `"version": APP_VERSION` verwenden.
- Vor Publish Manifest und statisches AP5-Gate prüfen.
- Nach Publish muss Version `1.1.5` im Repository/App-Updatepfad sichtbar sein.
- App zun
