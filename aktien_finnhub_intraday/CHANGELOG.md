# Changelog

## 1.0.3
- WebSocket-Requestpfad auf gültige HTTP-Origin-Form mit führendem `/` korrigiert.
- Leerer `urlparse`-Pfad wird nun sicher als `/` behandelt.
- Redigierte Eigendiagnose und bestehende Tick-, SQLite-, Export- und Retentionslogik bleiben erhalten.


## 1.0.2
- Redigierte WebSocket-Eigendiagnose direkt im App-Prozess integriert.
- DNS-Ziele, Python-/OpenSSL-Version, TLS-Version, Cipher und Peer-IP werden dokumentiert.
- Requestlänge und Headernamen werden ohne Tokenwerte protokolliert.
- HTTP-Statuszeile, Antwortheader und begrenzter Antwortbody werden sicher redigiert.
- Erfolgreiche Sec-WebSocket-Accept-Prüfung wird nachgewiesen.
- Tick-, SQLite-, Export- und Retentionslogik bleiben unverändert.

## 1.0.1
- WebSocket-Handshake-Diagnose erweitert.

## 1.0.0
- Erstversion.
