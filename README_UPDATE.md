# Home Assistant Aktien Apps

Repository fuer den isolierten Finnhub-Intraday-Dienst des Aktienprojekts.

## Aktueller Stand

- App: `aktien_finnhub_intraday`
- Version: `1.0.7`
- Datenquelle: Finnhub WebSocket
- Live-Testpfad: Register-ID `006`, Symbol `NVDA`
- Handelsplatz: `NASDAQ`
- Waehrung: `USD`
- Speicherung: SQLite/WAL unter `/share/aktien_intraday/active/intraday.sqlite3`
- Rohdatenaufbewahrung: `90 Tage`
- Exportpunkte: `1200`
- Exporte: `10s`, `30s`, `1m`, `5m`, `15m`, `30m`, `1h`, `4h`

## 1.0.7

- Startvertrag an die aktuelle Home-Assistant-S6-Vorgabe angepasst.
- Das Home-Assistant-Basisimage behaelt seinen eigenen `/init`-Entrypoint; das Dockerfile setzt keinen eigenen `ENTRYPOINT`.
- `init: false` verhindert einen zusaetzlichen Docker-Init vor S6, damit S6 Prozess 1 bleibt.
- `CMD ["/run.sh"]` startet weiterhin den belegten App-Laufweg.
- Der Read-Timeout-Fix aus 1.0.4 bleibt enthalten: nachrichtenarme WebSocket-Phasen fuehren nicht automatisch zu einem vollstaendigen Reconnect.
- Tick-, SQLite/WAL-, Candle-, Export- und Retentionslogik bleiben unveraendert.
- Register `009` und `010` bleiben ohne Livefreigabe; automatische Orders bleiben gesperrt.

## Versionshistorie

### 1.0.6
- Versuch zur Korrektur der S6/PID1-Startkette; Laufzeitabnahme zeigte weiterhin `s6-overlay-suexec: fatal: can only run as pid 1`.

### 1.0.5
- Startvertrag des rekonstruierten 1.0.3-Images und Read-Timeout-Fix zusammengefuehrt.

### 1.0.4
- Read-Timeout als Leerlauf behandelt, statt die WebSocket-Verbindung sofort als defekt zu bewerten.

### 1.0.3
- WebSocket-Requestpfad auf gueltige HTTP-Origin-Form korrigiert; leerer Pfad wird `/`.

### 1.0.2
- Redigierte WebSocket-Eigendiagnose integriert.

### 1.0.1
- WebSocket-Handshake-Diagnose erweitert.

### 1.0.0
- Erstversion.
