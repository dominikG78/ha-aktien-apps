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
