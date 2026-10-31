# K05 — nach unten oeffnende Teleskop-Senktuer

## Nutzerkorrektur und Konstruktionsentscheidung

Die Tuer soll nicht mehr nach oben fahren, sondern den Platz vor dem Gestell
nach unten nutzen. Keine Aenderung des Kopfes, der Antriebe, Hubbereiche,
Tischhoehe oder Maschinenaufstellung. Die bisherige 1000-mm-Oeffnung bleibt.
Eine 1:1-Richtungsumkehr des 1040-mm-Blatts wuerde zum Bodendurchtritt fuehren.
Deshalb zwei Segmente mit unterschiedlichen Tiefenebenen statt einer stillen
Verkleinerung der Oeffnung oder Erhoehung des gesamten Gestells.

## Koordinaten und Nennmasse

Maschinenaufstellebene z=0, Boden z=-750 mm. Oeffnung z=100...1100 mm.
Unteres Segment geschlossen z=80...610, oberes z=590...1120 mm.
Breite 800 mm, Hoehe 530 mm je Segment, mittige Ueberdeckung 20 mm.
Untere Rahmenebene y=-525...-495, obere y=-585...-555 mm.
Die aussen angesetzten Scheiben befinden sich vor der jeweiligen Rahmenebene.

Bei Oeffnungsgrad f in [0,1]:
- Unteres Segment delta_z=-515*f mm.
- Oberes Segment delta_z=-1030*f mm.

Offen: unteres z=-435...95, oberes z=-440...90 mm. Beide Segmentoberkanten
liegen unterhalb der z=100-mm-Schwelle. Tiefste Segment-Unterkante 310 mm ueber
Boden. Kassette-Unterkante 245 mm ueber Boden. Frontkante der Kassette 175 mm
vor der Einhausungsfront. Einbauraum fuer reale Hardware kann groesser werden.

## Geometrie

Je Segment eigener Rahmen und Scheibe, zwei C-Fuehrungen, vier Schlitten,
vier Mitnehmer und eigene Schaltfahne. Je Segment separater reservierter
Geschlossen-Schalter/Zuhaltung. Der Griff sitzt am oberen Segment: geschlossen
im oberen Bereich, offen nahe der Schwelle. Tiefe Fuehrungstuerme verbinden
beide Schienenebenen und werden mit Konsolen an den Gestellholmen angesetzt.
Die Quertraverse endet unter dem Dach. Kein hoher Ueberbau mehr.

Schutzkasten mit Seiten, Boden und Rueckschutz vor dem Untergestell. Aussparungen
fuer feste Pfosten sind geometrisch dargestellt. Kein fertig abgedichteter
Nassraum: KSS-Abstreifer, Sammelrinne, Ablauf und Schlauchfuehrung fehlen.
Der Kasten verkleinert den freien Zugang zur Untergestellfront.

## Was absichtlich nicht behauptet wird

Die Bewegungsbeziehung ist keine konstruierte Seil-/Kettenkopplung und kein
fertiger Tuerantrieb. Kraefte, Beschlaege, Seile, Rollen, Gegengewichte,
Gasfedern, Fangvorrichtungen, Zuhaltung und Bedienergonomie sind offen.
Rahmen und C-Profile sind Ansichtsentwuerfe, keine ausgesuchten Kaufteile.
Keine Schutzscheiben-, Rueckhalte-, Elektro- oder Dichtheitsfreigabe.

## Geometriepruefung

Die pruefbaren Teile des Rezepts werden lokal als Volumenkoerper aufgebaut.
Das ist kein NX-Test. Der Bewegungstest vergleicht an neun Stellungen alle
bewegten Tuerteile mit allen gezeichneten stationaeren Teilen einschliesslich
Gestell und KSS; gegenseitige Segmente werden ebenfalls verglichen.
Verbindungen innerhalb desselben Segments werden nicht als Kollision gewertet.
Daraus folgt kein lueckenloser Bewegungs-/Toleranz- oder Sicherheitsnachweis.

## Unveraenderter Bestand

Alle 366 Teile ausserhalb der Einhausungsgruppe haben dieselben ausgewerteten
Geometrieoperationen, Positionen und Materialien wie die Vorlage K03/K04.
Die bekannten statischen Maschinen-Anschlusskonflikte werden nicht versteckt.

## Native Datei

`NX_CNC_Gesamtansicht.py` verwendet den vorhandenen NX-Adapter ohne neue
API-Aufrufe. `door_open` bleibt einheitenlos; Laengen werden in Millimetern
gefuehrt. Lokale Einzelteilgeometrie bleibt beim Oeffnen starr, die Komponentendatums
verschieben sich. Neues Ausgabeziel pro Lauf. Kein echter NX-Lauf hier erfolgt.
