# Entwicklungspruefung vom 31.10.2026

Gepruefte aktive Quellrevision: `6631f8b65e7a1188d24391d8b10ce84c1cd7b114`.
Roadmap und Auswertung stehen unter `docs/superpowers/plans/` in
`2026-10-31-entwicklungsroadmap.md` und `2026-10-31-journalpruefbericht.md`.

- `journal_matrix.json`: Befehle, Umgebung, Zeit, Exitcode und Rohprotokoll je
  nativem Lauf; sieben Projektjournale plus ein Rezept-Diagnosejournal.
- `wiederoeffnung.json`, `teilemanifest_gesamt.json`, `blech_nachweis_gesamt.json`:
  native Ergebnisse des neuen Gesamt-Testlaufs, keine Fertigungsfreigabe.
- `pytest_baseline*`, `unittest*`, `verify_package*`: unveraenderte Offline-
  Rohprotokolle und Metadaten. Der pytest-Metadateneintrag nennt den Pythonpfad
  relativ zum Paketstamm; aus cwd `projekt/` lautet er
  `../.venv/Scripts/python.exe`. Alle Offline-Laeufe vom 31.10.2026.
- `offline_umgebung.txt`, `offline_freeze.txt`, `pip_install*`: getrennte lokale
  Standard-Python-Umgebung, keine Installation in NX.
- `hashdiagnose/`: Diagnose der numerischen Rezept-Serialisierung inklusive
  Reproduktionsskript; produktive Referenzpruefung bleibt unveraendert.
- `detailaudit_zahlen.json`: Tabellenzaehlung, keine Geometriepruefung.

Die Rohprotokolle enthalten die urspruenglichen absoluten Ausfuehrungspfade.
`lokales_laufarchiv.json` ordnet die anschliessend verschobenen Testverzeichnisse
zu. `NX_Laeufe/` ist ein **nur lokales, nicht versioniertes Testarchiv**. Diese
Duplikate wurden nach dem Verschieben nicht erneut nativ geoeffnet. Der zuvor
gespeicherte und versionierte CAD-Lieferstand unter `cad/nx/` bleibt unveraendert.
Neue CAD-Erzeugung aus diesem Quellstand ist mit den dokumentierten Journaleinstiegen
moeglich; kein Rueckgriff auf alte CAD-Dateien ausserhalb des Projekts.

Ergebnis: sieben native Journale Exitcode 0, 112 Offline-Tests und 91 Untertests
bestanden; neun Hilfstests bestanden, ein Symlink-Test umgebungsbedingt skip.
Historischer Paketidentitaetscheck: Exitcode 1, sieben absichtlich geaenderte
Dateien gegen das Originalmanifest; dieses wurde nicht ersetzt.
