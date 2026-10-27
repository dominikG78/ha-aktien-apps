# AP5 Betriebs- und Abnahmehinweise

## Vor dem Build

1. Statisches AP5-Gate muss `GESAMTERGEBNIS=BESTANDEN` melden.
2. Install-Prepare muss `STATIC_GATE=BESTANDEN`, `STORAGE_GATE=BESTANDEN` und `SCHUTZGATE=BESTANDEN` melden.
3. App-Konfiguration bleibt fuer den ersten Build `enabled: false`.

## Nach dem Build

Pruefen:

- App-Version `1.1.0`.
- `/media/COPILOT_DATA/aktien/intraday` im App-Laufzeitkontext erreichbar.
- 20 Registerordner unter `db/` und `exports_v2/` sichtbar.
- Bei `enabled: false` keine Provider-Subscription und keine neuen Live-DBs.
- Keine produktiven `10s`, `1m` oder `30m`-Pfade.

## Runtime-Freigabe

Providerintegration erst nach separater AP5-Runtime-Abnahme freigeben. Writer-Isolation muss mit mindestens zwei unterschiedlich konfigurierten Registern real nachgewiesen werden, bevor eine breitere Registerfreigabe erfolgt.
