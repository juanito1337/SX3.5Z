# Codex-Übergabepaket – Umsetzungsplan

> For agentic workers: use superpowers:executing-plans for the verification and handoff steps.

**Goal:** Den vorhandenen Entwicklungsstand 09 unverändert mit genügend Kontext für die Fortsetzung ausliefern.
**Architecture:** Aktiver Quellstand unter `projekt/`, Quellen unter `referenzen/`, neuer Übergabekontext im Paketstamm und unter `uebergabe/`. Keine Zusammenführung historischer Entwicklungszweige.
**Tech Stack:** Python 3.10+ für Hilfsprüfung; unverändertes Siemens-NX-Open-Projekt; Markdown/JSON/ZIP.
**Spec:** `uebergabe/UMFANG.md` sowie `referenzen/anforderungen/Eingefügter Text(7).txt`.

## Grenzen und Prüfschwerpunkte
- Kein Schreibzugriff auf bestehende NX-Originaldateien.
- Alle Projektdateien gegenüber dem Quell-ZIP per SHA-256 prüfen.
- Fehlende oder veränderte Dateien dürfen nicht als identisch gemeldet werden.
- Ungültige Manifestpfade dürfen nicht außerhalb des Paketverzeichnisses gelesen werden.
- NX-Funktionsprüfung und mechanische Freigabe nicht aus Offline-Tests ableiten.

## Aufgaben
- [x] Quell-ZIP inventarisieren und sicher unter `projekt/` entpacken.
- [x] Vorhandene Offline-Tests unverändert erneut ausführen und eigenes Protokoll sichern.
- [x] Originalanforderungen, Fotos, Handbücher, BF20-Referenzen und NX-Protokolle übernehmen.
- [x] AGENTS, Projektstatus, Umgebungsbeschreibung, Entscheidungen, ATC-Notiz und Startprompt schreiben.
- [x] Integritätsprüfer testgetrieben erstellen; Fehlerfälle und korrekte Kopie prüfen.
- [x] Gesamtmanifest erstellen, ZIP packen, neu entpacken und erneut prüfen.
- [x] Ergebnis und Grenzen ohne Behauptung einer NX-Ausführung dokumentieren.

Die abschließende ZIP-Wiederentpackprüfung wird im separat mitgelieferten `SX35Z_Codex_Uebergabe_Pruefung.json` belegt; kein nativer NX-Lauf.
