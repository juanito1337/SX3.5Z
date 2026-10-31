# API-Prüfstand 06

## Vorhandener Grundadapter
Native Parameter, Blöcke, Zylinder, Kegel, Profil-Extrusionen, separate boolesche
Operationen, Teil-Dateiverwaltung und AddComponent stammen aus den bisherigen
Paketen. Historische Nutzerprotokolle zeigen Teilprüfungen, aber keine Bestätigung
dieser gesamten Revision. Grundadapter-Version 4.8 ist bewusst beibehalten.

## Neuer Pfad
`nx_sheetmetal06.py` übernimmt nur mit ausdrücklich gewähltem Modus `required`
die Konvertierung. Basisfläche wird anhand der lokalen Ebene und Normale eindeutig
bestimmt. Konvertierung mit nicht-null-Biegeradius; anschließend:
- genau ein Körper,
- IsSheetmetalBody == True,
- GetBodyThickness innerhalb 0,005 mm des angeforderten Werts.

Die 0,005 mm sind eine numerische Prüfgrenze, KEINE Fertigungstoleranz.
Der gemessene Radius wird nicht ausgelesen. Berichtsfelder heißen deshalb
`requested_inner_radius_mm` und `requested_neutral_factor`.
Keine Abwicklung, Biegetabelle, Blechzeichnung oder CNC-Fertigungsdatei erzeugt.
Der Neutralfaktor wird als Part-Vorgabe gesetzt. Die Abwicklungsmethode der
Installation wird hier noch nicht geprüft oder umgestellt.

## Laufzeitgrenze
KEIN tatsächlicher NX-Lauf dieser Revision. Die Adaptertests verwenden Testobjekte.
Sie prüfen Fehlerbehandlung und Argumentreihenfolge, aber keine echten Siemens-Bindungen.
Die API-Recherche ist in `Quellen/API_06.md` mit ihrem begrenzten Versionsbezug dokumentiert.

Vor dem Gesamtaufbau wird eine U-Blechprobe erstellt. Bei Fehler endet der Pflichtmodus
vor den 458 Maschinenteilen. Für einen isolierten Türrahmenversuch kann alternativ
`NX_Blech_Pruefen.py` gestartet werden. Nur der absichtlich eingestellte `solid`-Modus
überspringt die Konvertierung und bleibt ausdrücklich als Vorform ausgewiesen.

Die Konvertierung erfolgt nach den Vorform-Volumenprüfungen. Die Offline-Meshes und
Kollisionsstichproben gelten für Vorformen, NICHT für einen vermeintlich bereits in NX
konvertierten Endzustand. Tatsächliche Biegeradien können benachbarte Freiräume verändern.
