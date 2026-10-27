# Veroeffentlichung AP5 Version 1.1.5

Dieses Verzeichnis ist die vollstaendige Repository-Quellbasis fuer das Projekt:

`dominikG78/ha-aktien-apps`

## Verbindlicher Release-Stand

App-Version:

`1.1.5`

Build-Marker:

`AP5_IMAGE_INTERNAL_INSTRUMENTS_V2`

Instrumentenkonfiguration:

`/opt/aktien/instruments.json`

Persistenter Datenroot:

`/media/COPILOT_DATA/aktien/intraday`

Produktive Intervalle:

- `30s`
- `5m`
- `15m`
- `1h`
- `4h`

Nicht produktiv zulaessig:

- `10s`
- `1m`
- `30m`

## Kontrolle vor Push

1. `MANIFEST_SHA256.txt` mit `sha256sum -c MANIFEST_SHA256.txt` pruefen.

2. Sicherstellen, dass
   `aktien_finnhub_intraday/config.yaml`
   Version `1.1.5` enthaelt.

3. Sicherstellen, dass `service.py` enthaelt:

   `APP_VERSION = "1.1.5"`

4. Sicherstellen, dass `service.py` enthaelt:

   `BUILD_MARKER = "AP5_IMAGE_INTERNAL_INSTRUMENTS_V2"`

5. Sicherstellen, dass die Instrumentenkonfiguration ausschliesslich aus

   `/opt/aktien/instruments.json`

   geladen wird.

6. Sicherstellen, dass das Dockerfile enthaelt:

   `COPY instruments.json /opt/aktien/instruments.json`

7. Folgende Altlogik muss 0 Treffer ergeben:

   - `/config/instruments.json`
   - `options['instruments_file']`
   - `options["instruments_file"]`
   - `AP5_IMAGE_INTERNAL_INSTRUMENTS_V1`
   - HTML-Artefakt `&gt;`

8. `collector.json` muss seine Version dynamisch ueber

   `"version": APP_VERSION`

   erhalten.

9. Keine Tokens oder Zugangsdaten committen.

10. Keine SQLite-, WAL-, SHM-, Export-, Status-, Historien- oder Migrationsdaten committen.

11. Gesamten geprueften Repository-Inhalt in das bestehende Git-Repository 
