## 1.1.1

### Fixed
- Include `instruments.json` in the app image at `/config/instruments.json`.
- Fix AP5 startup failure caused by the missing instrument configuration.

### Safety
- Provider runtime remains disabled pending AP5 runtime validation.
- No market data, history or migration data is modified.
