# Landkarte des vorhandenen Codes

Keine Umstrukturierung bei der Übergabe. Alle hier genannten Pfade beginnen in `projekt/`.

| Datei / Gruppe | Rolle |
|---|---|
| `NX_CNC_Gesamtansicht.py` | NX-Einstieg: Vorprüfungen, Einzelteile, Unterbaugruppen, Hauptbaugruppe, Protokolle |
| `NX_*_Pruefen.py` | Auswahljournale für überschaubare native Teiltests |
| `cnc_ansichtsmodell.py` | Aktueller Einstieg des Rezepts09; importiert den erhaltenen Stand08 |
| `normteile09.py` | Geometrische Ergänzungen der Normteile und Magazinoption09 |
| `cnc_ansichtsmodell08.py`, `cnc_ansichtsmodell07.py`, `cnc_ansichtsmodell01.py` | Aktive historische Rezeptabhängigkeiten, NICHT einfach Archivdateien |
| `modell_v4.py`, `v3_geometriebasis.py` | Foto-/Bestandsrekonstruktion, geometrische Grundbausteine |
| `blech06.py`, `ruecklauf07.py`, `formeln07.py` | Blechvorformen und Späne/KSS-Rezepte bzw. Maßformeln |
| `nx_native.py`, `nx_files.py`, `nx_geometry.py` | Native NX-Features, sichere Dateierzeugung und Mess-/Geometrieprüfungen |
| `nx_sheetmetal06.py` | Nativer Blechadapter, Patch07.2 trotz Dateiname06 |
| `nx_formeln073.py` | Dimensionsgerechte Ausdrucksübersetzung, Patch07.3 |
| `umbau_daten08.py`, `umbau_daten09.py` | Katalog, Herkunft, Freigabevoraussetzungen, Mengen-/Modellzuordnung |
| `Projekt08_Berichte.py`, `Projekt09_Berichte.py` | Berichtserzeugung; schreibt CSV/JSON, keine reine Leseprüfung |
| `tools/` | Ergänzende unabhängige Geometrie-/Browser-/Dokumentwerkzeuge |
| `tests`, `tests08`, `tests09` | Aktive pytest.ini-Tests; getrennt von historischen Testberichten |

## Eingabeschichten

`Parameter.json`: Bestands-/Maschinenparameter; `CNC_Parameter.json`: CNC-Zusätze;
`Ausbau_Parameter.json`: Einhausung/Tür/KSS; `Detail_Parameter_09.json`: Details09.
Tatsächliche Aufmaßdatensätze stehen getrennt unter `Aufmass/`; Nullwerte bedeuten fehlende Daten.
`Einkauf/Kaufteile_09.json` und `Quellen/Quellen_08.json` + `Quellen_09.json` verbinden
Artikel und Herkunft. Kataloghauptmaße sind gegen willkürliche Änderungen abgesichert.

## Nicht verwechseln

`Historie_07_3/` ist ein Archiv mit alten Ansichten, Berichten und Testläufen.
`referenzen/archiv/CNC_UMBAU_NXOPEN_Entwicklung_10.zip` ist ein anderer, früherer Entwicklungszweig
mit Bestandsanalyse/Modulen; die höhere Nummer10 bedeutet nicht "aktueller als Umsetzung09".
`referenzen/archiv/SX35Z_NX_Journale_v4_8.zip` enthält die ursprüngliche Fotorekonstruktion.
Vor einer Wiederverwendung beide separat entpacken und Schnittstellen prüfen.

## Datenfluss für spätere Änderungen

Belegte Änderung → Katalog/Maßparameter → Rezept → nativer NX-Aufbau → geometrische Prüfung
→ Modellzuordnung/Stückliste → Bauanleitung und Fertigungszeichnungen.
Keine isolierte Excel- oder HTML-Änderung als Änderung des tatsächlichen NX-Modells ausgeben.
