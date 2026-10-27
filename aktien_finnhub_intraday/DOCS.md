# AP5 Betriebs- und Abnahmehinweise

## Zielstand

Verbindliche App-Version:

`1.1.5`

Verbindlicher Build-Marker:

`AP5_IMAGE_INTERNAL_INSTRUMENTS_V2`

Instrumentenkonfiguration:

`/opt/aktien/instruments.json`

Persistenter Datenroot:

`/media/COPILOT_DATA/aktien/intraday`

Zulässige Register:

`001` bis `020`

Produktive Intervalle:

- `30s`
- `5m`
- `15m`
- `1h`
- `4h`

Nicht zulässig:

- `10s`
- `1m`
- `30m`

---

## Vor dem Build

Folgende Gates müssen bestanden sein:

- Statisches AP5-Gate:
  `GESAMTERGEBNIS=BESTANDEN`

- Install-Prepare:
  `STATIC_GATE=BESTANDEN`

- Storage-Gate:
  `STORAGE_GATE=BESTANDEN`

- Schutzgate:
  `SCHUTZGATE=BESTANDEN`

- Registerstruktur:
  `001` bis `020` vollständig vorhanden.

- Writerstruktur:
  getrennte Zielpfade je Register.

- Media-Mount:
  schreibbarer `/media`-Mount vorhanden.

- Instrumentenkonfiguration:
  `/opt/aktien/instruments.json`

- App-Konfiguration:
  `enabled: false`

Vor dem Build dürfen keine produktiven Datenbanken,
Historien oder Migrationsbestände verändert oder gelöscht werden.

---

## Build-Identität

Nach Installation muss die App Version `1.1.5` melden.

Im aktuellen App-Log muss dieser Marker erscheinen:

`AP5_START version=1.1.5 build=AP5_IMAGE_INTERNAL_INSTRUMENTS_V2 instruments=/opt/aktien/instruments.json`

Dieser Marker ist Pflicht für die Build-Freigabe.

Folgende Altlogik darf im aktuellen Build nicht mehr vorkommen:

- `/config/instruments.json`
- `options['instruments_file']`
- `options["instruments_file"]`
- `AP5_IMAGE_INTERNAL_INSTRUMENTS_V1`

Folgende Fehler sind für die Build-Freigabe nicht zulässig:

- `SyntaxError`
- `IndentationError`
- `FileNotFoundError`
- `PermissionError`
- unerwarteter `Traceback`

---

## Nach dem Build

Prüfen:

- App-Version `1.1.5`.
- App-Zustand `started`.
