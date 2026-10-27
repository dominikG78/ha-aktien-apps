# Changelog

## 1.1.5

### Fixed
- AP5-Build-Identität auf Version `1.1.5` konsolidiert.
- Instrumentenkonfiguration wird fest aus `/opt/aktien/instruments.json` geladen.
- Veraltete Abhängigkeit von `/config/instruments.json` entfernt.
- Veraltete `instruments_file`-Option aus der Laufzeitkonfiguration entfernt.
- Build-Marker auf `AP5_IMAGE_INTERNAL_INSTRUMENTS_V2` aktualisiert.
- Runtime-Status verwendet `APP_VERSION` statt einer fest codierten Versionsnummer.
- Writer-Isolationslogik und Python-Code-Struktur bereinigt.

### Runtime verification
Erwarteter Startmarker:

`AP5_START version=1.1.5 build=AP5_IMAGE_INTERNAL_INSTRUMENTS_V2 instruments=/opt/aktien/instruments.json`

### Safety
- App bleibt fuer die erste Runtime-Abnahme mit `enabled: false` deaktiviert.
- Providerstart bleibt bis zur separaten AP5-Runtime-Freigabe gesperrt.
- Keine bestehenden SQLite-, WAL- oder SHM-Dateien werden geloescht oder migriert.
- `/share/aktien_intraday` bleibt geschuetzt.
- `migration_20261027` bleibt geschuetzt.
- Historische Marktdaten bleiben geschuetzt.
- Keine `.storage`-Aenderungen.
- Kein Home-Assistant-Core-Neustart erforderlich.

---

## 1.1.4

### Fixed
- Gebuendelte `instruments.json` nach `/opt/aktien/instruments.json` verlagert.
- Verhindert, dass der Runtime-Mount unter `/config` die gebuendelte Instrumentenkonfiguration verdeckt.

### Safety
- Keine Writer-, Datenbank- oder Marktdatenmigration.
- Providerbetrieb bleibt bis zur AP5-Runtime-Abnahme gesperrt.

---

## 1.1.0

### Added
- Generische Instrumentenkonfiguration fuer Register 001 bis 020.
- Registerisolierter SQLite-Writer.
- Registerisolierte V2-Exportpfade.
- Persistenter Datenroot unter `/media/COPILOT_DATA/aktien/intraday`.
- Schreibbarer `media`-Mount fuer die App.

### Changed
- Produktive Candle-Intervalle auf `30s`, `5m`, `15m`, `1h` und `4h` standardisiert.
- Writer-Routing erfolgt ueber Registerkonfiguration anstelle einer gemeinsamen neuen SQLite-DB.

### Safety
- Providerstart bleibt bis zur AP5-Runtime-Abnahme gesperrt.
- Bestehender `/share/aktien_intraday`-Bestand bleibt unangetastet.
- `migration_20261027` und historische Daten bleiben geschuetzt.
- Keine Legacy-Loeschung in diesem Release.
