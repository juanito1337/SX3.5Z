# Ausführungsumgebungen – nicht miteinander verwechseln

## Nativer Nachweis13,01.11.2026

Quelle feaf3950c142590da45f353dc60b65c70ee527ed. NX2406/Python3.10.15 unveraendert,
separate run_journal-Prozesse; gemeinsame Oberflaeche unberuehrt. Vier
finale Laeufe Exit0: PARK-Aufbau, frisches Oeffnen/AP214, WECHSEL-Aufbau,
frisches Oeffnen/AP214. Je532 Einzelteile/17 Gruppen/24 native Blechkoerper.
Native Werkzeuglage WECHSEL nominell0/0/530mm. Keine reale Spindelpassung.

Erster Vollaufbau scheiterte beim JSON-Dateischreiben (OSError22); separater
NX-Schreibtest1000 Wiederholungen bestanden, Fehler im zweiten Lauf nicht
wiederaufgetreten. Ursache nicht abschliessend geklaert; keine spekulative
API-Aenderung. Unvollstaendige Laeufe lokal im Audit erhalten, nicht geliefert.
Offline-Pruefungen ersetzen keinen NX-Nachweis. Matrix/Rohlogs und Grenzen:
[Pruefbericht13](ergebnisse/entwicklung/20261101_atc13/README.md).


## Nativer Nachweis12,01.11.2026

Quellrevision b6e4643d5558780936f7b622af0102ad64041215. NX2406/Python3.10.15, separate eigene
run_journal-Prozesse; gemeinsame Oberflaeche nicht benutzt. Fuenf erfolgreiche
Journallaeufe: Normteil/ATC-Teilpruefung, PARK, frisches PARK-Oeffnen, WECHSEL,
frisches WECHSEL-Oeffnen. Je461 Einzelteile/17 Gruppen/19 native Blechteile.
Laufmatrix/Rohprotokolle: ergebnisse/entwicklung/20261101_revision12/.
Ein vorheriger Lauf wurde wegen Reviewbefund kontrolliert gestoppt; dessen
Zwischenstand ist als versuch01 erhalten und nicht ausgeliefert. Keine fremden
NX-Prozesse beendet. Aktuelle Pfade und Pruefgrenzen: cad/README.md.

## Nativer Nachweis11, 01.11.2026

NX2406/Python3.10.15 unveraendert. Neun Journallaeufe Exit0 einschliesslich
zweier kompletter Baugruppen und frischer Wiedereroeffnungen. Neue
NX_CNC_Wechselstellung.py erzeugt die Wechselposition; das Gesamtjournal erzeugt
PARK. Beide454 Parts/17 Unterbaugruppen, je19 native Blechkonvertierungen.
Native Werkzeuglagenpruefung in NX_Werkzeuglage_11.json des WECHSEL-Laufs.
Separate Offline-Suite173 Tests und99 Untertests. Vollstaendige Laufmatrix:
ergebnisse/entwicklung/20261101_revision11/native_matrix.json.
Aktuelle Pfade: cad/README.md. Historische Lieferstaende mit ihrem Quellstand pruefen.

## Fortschreibung01.11.2026

Gleiche unveraenderte Laufzeiten: NX2406/Python3.10.15, separate Offline-Umgebung
CPython3.12.14/CadQuery2.8/OCP7.9.3.1.1. Sieben aktuelle Journale Exit0,
511 Einzelteile erneut geladen,19 native Blechkonvertierungen; Offline163 Tests
und91 Untertests. Befehle/Rohprotokolle/Quellhashes:
`ergebnisse/entwicklung/20261101_teller/`. Aktueller Lieferlauf in `cad/README.md`.
Wiedereroeffnungsjournal prueft jetzt das mitgespeicherte aktuelle Rezept kanonisch.
Fuer historische09-Pruefungen die zugehoerige alte Git-Revision verwenden;
das neue Journal akzeptiert nicht stillschweigend ein abweichendes altes Rezept.

## Separate Offline-Umgebung, 31.10.2026

Unter `.venv/` liegt jetzt eine lokale Standard-Python-Umgebung: CPython 3.12.14,
pytest 9.0.2, CadQuery 2.8.0 und cadquery-ocp 7.9.3.1.1. Erstellt mit der
vorhandenen gebuendelten Laufzeit, ohne globale Python- oder NX-Aenderungen.
Alle 112 Tests und 91 Untertests der aktiven Suite bestanden. Vollstaendige
Paketversionen: `ergebnisse/entwicklung/20261031_134859/offline_freeze.txt`.

Aus `projekt/`:
`../.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider`

Aus Paketstamm:
`.venv/Scripts/python.exe tools_handoff/verify_package.py`
und `.venv/Scripts/python.exe -m unittest discover -s tools_handoff -p "test_*.py" -v`.
Der historische Paketcheck meldet absichtliche Git-Aenderungen; sein Manifest
nicht zum Gruenfaerben ersetzen. Ein Hilfstest fuer Symlinks ist unter diesem
Windows nicht ausfuehrbar. Native Tests separat mit `run_journal.exe`.

Die `.venv` ist lokal und ignoriert. Bei neuem Checkout mit einer separaten
Standard-Python-Installation eine `.venv` erstellen und dort
`python -m pip install -r requirements-offline.txt` ausfuehren; niemals in NX.

## Lokal nachgewiesen am 31.10.2026

`C:/Siemens/nx2406/NXBIN/run_journal.exe` fuehrt Python-Journale mit NXOpen und
Python 3.10.15 aus. Der Gesamtaufbau09 und das Oeffnen in frischem Prozess waren
erfolgreich (Exitcode 0). Native Blechkonvertierung ist in dieser Umgebung
verfuegbar. `ugraf.exe` meldet Dateiversion 2406.6000, `NXOpen.pyd` 2406.8100.

`projekt/NX_Ausgabe.json` zeigt jetzt explizit auf
`C:/Users/1337/Documents/ChatGPT/SX3.5Z/cad/nx`. Bei anderem Checkout-Pfad diesen
absoluten Konfigurationswert anpassen. Jeder Lauf erhaelt weiterhin ein neues
Verzeichnis. Neue Nutzerentscheidung: keine alten CAD-Dateien einlesen.
Ausfuehrungs- und Oeffnungsbefehle stehen in `cad/README.md`.
Die folgenden Abschnitte beschreiben den frueheren Uebergabestand; insbesondere
der dort genannte leere `output_root` und unbekannte Launcher sind ueberholt.

## Nutzerumgebung: aus historischen Logs beobachtet

- Windows, Siemens NX 2406.
- `NXOpen.pyd` in `C:\Siemens\nx2406\nxbin\python\NXOpen.pyd` bzw. gleichlautendem Pfad mit anderer Großschreibung.
- In verschiedenen Logs Python 3.10.12 und 3.10.15. Die aktive Installation erneut protokollieren.
- Ausgabe bisher `%LOCALAPPDATA%\SX35Z\NX_Output\`.
- Ein früherer Versuch auf `W:\` scheiterte an Dateisystem/Pfadauflösung; neue Tests lokal durchführen.

Quellen: `referenzen/nx_protokolle/`. Diese Pfade sind Beobachtungen, keine universellen Vorgaben.
NX-Binärmodule nicht in normales Python kopieren oder über einen erfundenen pip-Namen installieren.

## Aktuelles Journalprojekt

Alle relativen Konfigurationen müssen neben `projekt/NX_CNC_Gesamtansicht.py` bleiben.
`NX_Ausgabe.json` enthält einen leeren `output_root`, somit greift die bestehende Standardlogik.
Jede Ausführung erhält ein neues Laufverzeichnis; ältere Teilergebnisse nicht als neuen Gesamterfolg behandeln.

| Versionsanzeige | Bedeutung |
|---|---|
| 4.8 | Grundadapter / gemeinsame NX-Datei- und Geometrieerzeugung |
| 07.2 | Korrigierter nativer Blechadapter |
| 07.3 | Formelübersetzung für geneigte KSS-Bleche |
| CNC_UMSETZUNG_09 | Aktives Maschinen-/Magazinrezept |

Keine dieser Zahlen nur zur kosmetischen Angleichung umbenennen.

## Sichere native Testfolge

NX öffnen; keine Originaldateien überschreiben. Über **Journal wiedergeben / Play Journal** ausführen:

1. `projekt/NX_Blech_Pruefen.py` – Blech-Einzelteilprobe.
2. `projekt/NX_KSS_Pruefen.py` – geneigte Bleche / Einheitenkorrektur.
3. `projekt/NX_Umbau_Kern_Pruefen.py` bzw. `NX_Normteile_ATC_Pruefen.py` – gezielter Teilumfang.
4. `projekt/NX_CNC_Gesamtansicht.py` – vollständiger Aufbau.

Benötigte Modellierungs-/Blechfunktionen und Lizenz in der tatsächlichen Installation prüfen.
`Blech_Optionen.json` im Pflichtmodus belassen. Erfolgreiches `CommitFeature`, geprüfte Körper,
Speichern und erneutes Öffnen der Hauptbaugruppe sind getrennte Schritte.
Ergebnisse/Fehler mit Version, Parametern, Laufkennung und Dateihashes unter `ergebnisse/nx/` sichern.
Eine mögliche spätere Kommandozeilenanbindung an NX erst anhand der lokalen Dokumentation einrichten;
hier ist KEIN pauschal funktionierender automatischer NX-Launcher zugesichert.

## Offline-Entwicklung

Eine separate Standard-Python-Umgebung verwenden. Nicht in NX-Python pip-Pakete installieren.
Die neue Prüfung bei der Übergabe lief mit Python3.13.5 auf Linux; siehe
`uebergabe/pruefung/umgebung_beobachtet.json`. Python-3.10-Grammatik wird zusätzlich statisch geprüft,
ist aber kein Python3.10-Lauf und kein NX-Test.

Ab `projekt/`:

```powershell
python -m pytest -q -p no:cacheprovider
```

Mindestens pytest und CadQuery/OCP werden für die derzeitige Offline-Suite benötigt. Die Datei
`requirements-offline.txt` im Paketstamm benennt die bei dieser Übergabe beobachteten Direktversionen;
sie ist kein vollständig aufgelöster Windows-Lockfile. Plattformkompatibilität separat prüfen.

Optionale Dokumentwerkzeuge verwenden python-docx, openpyxl, artifact_tool, Playwright/Chromium
und ggf. lokale Renderwerkzeuge. `artifact_tool` stammt aus der bisherigen Erstellungsumgebung;
seine allgemeine Installierbarkeit auf dem Nutzer-PC ist nicht zugesichert. Die vorhandenen
Excel/PDF/Word-Dateien sind ohne Neugenerierung vorhanden. Abhängigkeiten vor Generatorlauf prüfen.

## Codex lokal oder Cloud

Für native Prüfungen bevorzugt lokal auf dem NX-PC arbeiten. WSL-/Linux-/Cloud-Codeausführung
ist keine NX-2406-Windows-Laufzeit. Zugriff auf einen Ordner allein bedeutet keine Verbindung zur
laufenden NX-Sitzung. Keine globalen Sicherheits-/Freigabeeinstellungen automatisch herabsetzen.
