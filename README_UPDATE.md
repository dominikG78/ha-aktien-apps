# Home Assistant Aktien Apps

Repository fuer den isolierten Finnhub-Intraday-Dienst des Aktienprojekts.

## Aktueller produktiver Stand

- App: `aktien_finnhub_intraday`
- Version: `1.0.6`
- Datenquelle: Finnhub WebSocket
- Freigegebener Livepfad: Register-ID `006`, Symbol `NVDA`
- Handelsplatz: `NASDAQ`
- Waehrung: `USD`
- Speicherung: SQLite/WAL unter `/share/aktien_intraday/active/intraday.sqlite3`
- Retention Rohdaten: `90 Tage`
- Exportpunkte: `1200`
- Exporte: `10s`, `30s`, `1m`, `5m`, `15m`, `30m`, `1h` und `4h`

## Version 1.0.6

- Container-Init-Kollision korrigiert: Supervisor-Init ist mit `init: false` deaktiviert.
- Der belegte s6-Startvertrag bleibt mit `ENTRYPOINT [\"/init\"]` und `CMD [\"/run.sh\"]` erhalten.
- Der Read-Timeout-Fix bleibt aktiv: nachrichtenarme WebSocket-Phasen werden als Leerlauf behandelt, nicht als vollstaendiger Verbindungsabbruch.
- `homeassistant_config` wird read-only eingebunden; `share` bleibt read-write.
- Tick-, SQLite/WAL-, Candle-, Export- und Retentionslogik bleiben unveraendert.
- Register `009` und `010` bleiben ohne Finnhub-Livefreigabe.
- Automatische Orders bleiben gesperrt.

## Versionshistorie

### 1.0.5
- Startvertrag des funktionierenden 1.0.3-Images wiederhergestellt.
- Read-Timeout-Fix beibehalten.

### 1.0.4
- Read-Timeout wird als WebSocket-Leerlauf behandelt; die bestehende Verbindung bleibt erhalten.

### 1.0.3
- WebSocket-Requestpfad auf gueltige HTTP-Origin-Form mit fuehrendem `/` korrigiert.
- Leerer `urlparse`-Pfad wird als `/` behandelt.

### 1.0.2
- Redigierte WebSocket-Eigendiagnose integriert.
- DNS-, TLS-, Cipher-, Peer-IP-, HTTP- und Sec-WebSocket-Accept-Diagnose ergaenzt.

### 1.0.1
- WebSocket-Handshake-Diagnose erweitert.

### 1.0.0
- Erstversion.

## Sicherheitsgrenzen

- Finnhub-Livebetrieb bleibt auf Register `006` / `NVDA` begrenzt.
- Register `009` und `010` bleiben inaktiv.
- Keine automatischen Kauf-/Verkaufsentscheidungen und keine Orders.
- Ein erfolgreicher WebSocket-Handshake allein gilt nicht als Nachweis aktueller Marktdaten.
