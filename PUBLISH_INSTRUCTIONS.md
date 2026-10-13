# Veroeffentlichung Version 1.0.1

Dieses Verzeichnis ist die vollstaendige Repository-Quellbasis fuer:

`https://github.com/dominikG78/ha-aktien-apps`

## Kontrolle vor Push

1. `MANIFEST_SHA256.txt` mit `sha256sum -c MANIFEST_SHA256.txt` pruefen.
2. Sicherstellen, dass `aktien_finnhub_intraday/config.yaml` Version `1.0.1` enthaelt.
3. Gesamten erzeugten Repository-Inhalt in das bestehende Git-Repository uebernehmen.
4. Commit und Push nach GitHub ausfuehren.
5. In Home Assistant den App-Store neu laden.
6. Ausschliesslich die App `Aktien Finnhub Intraday` auf Version `1.0.1` aktualisieren.
7. App starten und den gesonderten Laufzeit-Abschlusstest ausfuehren.

Kein Home-Assistant-Core-Neustart ist vorgesehen.
