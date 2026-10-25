## 1.0.4
- Read-Timeout als Leerlaufintervall behandelt; bestehende WebSocket-Verbindung bleibt erhalten.
- Keine Änderung an Tick-, SQLite-/WAL-, Kerzen-, Export- oder Retentionslogik.

## 1.0.3
- WebSocket-Requestpfad auf gültige HTTP-Origin-Form mit führendem `/` korrigiert.
- Leerer urlparse-Pfad wird sicher als `/` behandelt.
- Redigierte Eigendiagnose und bestehende Tick-, SQLite-, Export- und Retentionslogik bleiben erhalten.
