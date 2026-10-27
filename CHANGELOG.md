"version": "1.1.4"

### Fixed
- Move bundled `instruments.json` to `/opt/aktien/instruments.json`.
- Avoid the runtime `/config` mount hiding the bundled instrument configuration.

### Safety
- No writer, database or market-data changes.
- Provider runtime remains disabled pending AP5 runtime validation.
