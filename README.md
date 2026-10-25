# Home Assistant Aktien Apps

Repository für den isolierten Finnhub-Intraday-Dienst des Aktienprojekts.

## Aktueller produktiver Stand

- App: `aktien_finnhub_intraday`
- Version: `1.0.3`
- Datenquelle: Finnhub WebSocket
- Testinstrument: Register-ID `006`, Symbol `NVDA`
- Handelsplatz: `NASDAQ`
- Währung: `USD`
- Speicherung: SQLite/WAL unter `/share/aktien_intraday/active/intraday.sqlite3`
- Retention Rohdaten: `90 Tage`
- Exportpunkte: `1200`
- Exporte: `10s`, `30s`, `1m`, `5m`, `15m`, `30m`, `1h` und `4h`

## Versionshistorie

### 1.0.3

- WebSocket-Requestpfad auf gültige HTTP-Origin-Form mit führendem `/` korrigiert.
- Leerer `urlparse`-Pfad wird sicher als `/` behandelt.
- Redigierte Eigendiagnose bleibt erhalten.
- Tick-, SQLite-, Export- und Retentionslogik bleiben unverändert.

### 1.0.2

- Redigierte WebSocket-Eigendiagnose direkt in den App-Prozess integriert.
- DNS-Ziele, Python-/OpenSSL-Version, TLS-Version, Cipher und Peer-IP werden dokumentiert.
- Requestlänge und Headernamen werden ohne Tokenwerte protokolliert.
- HTTP-Statuszeile, Antwortheader und begrenzter Antwortbody werden sicher redigiert.
- Erfolgreiche `Sec-WebSocket-Accept`-Prüfung wird nachgewiesen.
- Tick-, SQLite-, Export- und Retentionslogik bleiben unverändert.

### 1.0.1

- WebSocket-Handshake-Diagnose erweitert.

### 1.0.0

- Erstversion.

## Laufzeitstatus

Version `1.0.3` ist derzeit der produktive und rollbackfähige Stand.

Die HA-seitige Statusauswertung unterscheidet Transportverbindung, Datenaktualität und Exportaktualität. Ein erfolgreicher WebSocket-Verbindungsaufbau allein gilt nicht als Nachweis für aktuelle Marktdaten.

## Entwicklung 1.0.4

Version `1.0.4` befindet sich in Vorbereitung.

Ziel ist ausschließlich die Korrektur der Read-Timeout-Behandlung: Eine nachrichtenarme WebSocket-Phase soll nicht mehr automatisch als Verbindungsabbruch behandelt werden.

Unverändert bleiben:

- Finnhub-Datenquelle
- Register-ID `006`
- Symbol `NVDA`
- SQLite-/WAL-Datenhaltung
- Tickverarbeitung
- Kerzenintervalle
- Exportformate
- Retention
- Register `009` und `010` ohne Live-Freigabe
- keine automatischen Orders

Version `1.0.4` gilt erst nach erfolgreichem Build, Installation, Laufzeitvalidierung und bestandener Rollbackprüfung als produktiv.
