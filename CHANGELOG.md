## 1.2.0

### Added
- Generischer Finnhub-Multi-Instrument-Provider.
- Dynamische Finnhub-Subscriptions aus der zentralen Instrumentenkonfiguration.
- Symbol-zu-Register-Routing fuer alle freigegebenen Register.
- Registerisolierte SQLite-Writer fuer Live-Ticks.
- Registerisolierte V2-Exporte.
- Reconnect- und Speicher-Schutzlogik.

### Changed
- Eine gemeinsame Finnhub-WebSocket-Verbindung bedient die aktivierten Instrumente.
- Produktive Intervalle bleiben auf `30s`, `5m`, `15m`, `1h` und `4h` begrenzt.
- Writer und Exporte verwenden ausschliesslich die jeweilige Register-ID.

### Safety
- Keine Datenkopien zwischen Registern.
- Keine technische Sonderrolle fuer Register 006.
- `009` und `010` bleiben deaktiviert, solange sie nicht explizit freigegeben werden.
- Bestehende Historien bleiben unveraendert.
- `migration_20261027` bleibt geschuetzt.
- `/share/aktien_intraday` bleibt geschuetzt.
- Keine `.storage`-Aenderungen.
- Kein Home-Assistant-Core-Neustart erforderlich.

### Runtime validation
Vor der Livefreigabe bleibt:

`enabled: false`

Die Livefreigabe erfolgt erst nach bestandener 1.2.0-Build- und Runtime-Abnahme.

## 1.1.5

### Fixed

- Finalized the AP5 image-internal instrument configuration at `/opt/aktien/instruments.json`.
- Removed remaining legacy references to `/config/instruments.json`.
- Removed the obsolete configurable `instruments_file` path.
- Added explicit AP5 build identification:
  `AP5_IMAGE_INTERNAL_INSTRUMENTS_V2`.
- Synchronized runtime status reporting with `APP_VERSION`.
- Corrected the register-writer isolation path and startup code structure.

### Runtime verification

The expected startup marker is:

`AP5_START version=1.1.5 build=AP5_IMAGE_INTERNAL_INSTRUMENTS_V2 instruments=/opt/aktien/instruments.json`

### Safety

- Provider runtime remains disabled pending AP5 runtime validation.
- `enabled` remains `false` for the initial runtime acceptance.
- No existing SQLite, WAL or SHM data is migrated or deleted.
- Existing `/share/aktien_intraday` data remains protected.
- `migration_20261027` remains protected.
- Historical market data remains protected.
- No Home Assistant `.storage` changes.
- No Home Assistant Core restart is required.
