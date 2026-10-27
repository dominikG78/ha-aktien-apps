# Publish AP5 Version 1.1.4

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

`1.1.4`

Die App-Konfiguration muss enthalten:

`version: "1.1.4"`

Die Laufzeitdiagnose in `service.py` verwendet:

`APP_VERSION = "1.1.4"`

Der Build muss beim Start eindeutig ausgeben:

`AP5_START version=1.1.4 build=AP5_IMAGE_INTERNAL_INSTRUMENTS_V1 instruments=/opt/aktien/instruments.json`

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

## Persistente Marktdaten

Produktiver
