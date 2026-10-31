# Ausführungsumgebungen – nicht miteinander verwechseln

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
