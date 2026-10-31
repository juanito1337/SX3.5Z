# Konstruktionsaenderung 03

## Bedeutung des Nutzerwunsches
"Tuer horizontal" wurde als horizontale seitliche Schiebebewegung interpretiert.
Keine horizontal geteilte oder nach oben klappende Tuer. Zwei schmale Fluegel
vermeiden seitlichen Ueberstand, begrenzen die lichte Zugangsbreite aber auf 760 mm.
Grosse Werkstuecke/Spannmittel und die benoetigte Handhabung sind gesondert zu pruefen.

## Abmessungen
| Merkmal | Stand 02 | Stand 03 |
|---|---:|---:|
| Gehaeuse-/Rahmenbreite | 1850 | 1650 mm |
| Gehaeuse-/Rahmentiefe | 1200 | 1000 mm |
| Einhausung ueber Maschinenauflage | 1250 | 1200 mm |
| Maschinenaufstellebene ueber Boden | 750 | 750 mm |
| Arbeitstisch ueber Boden | 930 | 930 mm |
| Gezeichnete Gesamthoehe inkl. 2-mm-Dach | 2002 | 1952 mm |
| Gesamte gezeichnete Aussenhuelle mit Schrank/Griffen | 2233 x 1295 | 2033 x 1131 mm |

Die rechteckige Nenn-Grundflaeche der Huelle sinkt von 2,22 auf 1,65 m²
(25,68 %). Die Aussenhuelle ist kein Wartungs-/Bedienflaechennachweis.

## Bewegungsraum und Zentrierung
Die Maschinenlage wird nicht skaliert. Die Huellenmitte liegt bei x=62/y=25 mm
im vorhandenen Maschinenkoordinatensystem. Die konservativen Modellgrenzen im
Zielbereich sind x=-690..814, y=-382..427, z=0..1111 mm. Die verwendeten inneren
Grenzen ergeben 63 mm Reserve je Seite, 53 mm vorn, 96 mm hinten und 89 mm oben.
Z=0 ist die beabsichtigte Aufstellebene, kein Sicherheitsabstand.
Die zusaetzlich modellierten Balgformen werden nur als gezeichnete Koerper erfasst;
die reale flexible Form, Leitungen und Werkstuecke fehlen im Nachweis.

## Schiebetuerentwurf
Lichte Oeffnung: 760 x 1000 mm, Unterkante z=100 mm ueber der Maschinenauflage.
Blaetter: 410 x 1040 x 30 mm, 20-mm-Mittelueberdeckung auf um 38 mm versetzten
Ebenen; Weg je Blatt 395 mm. Geoeffnet verbleiben 30 mm seitlicher Abstand zur
Gehaeuse-Aussenkante. Glas und Griffe werden gemeinsam mit den Blaettern bewegt.
Drei gemeinsame Konsolen tragen die zwei schematischen C-Laufschienen; je Blatt
zwei Rollen/Haenger und eine durchgehende untere U-Fuehrung. Noch nicht enthalten:
endgueltige Schrauben/Endanschlaege/Abstreifer, erprobte Rollenteile, nachgewiesene
Abhebesicherung, konkrete Tuersensoren und Sicherheitsverschaltung.
Die Mittelueberdeckung ist unten 8 mm freigestellt, damit sie nicht in die
Fuehrungskanaele greift. Der untere Dicht-/Ablaufanschluss ist daher ausdruecklich
offen. Es wird keine KSS-Dichtheit behauptet.

## Software und Nachweise
Verkleinerte Parameter, neue Türkörper und einheitenlose door_open-Ausdrucks-
erzeugung; ansonsten bestehender NX-Featureadapter. Keine neuen NX-API-Methoden.
Vollstaendige Neuaufbauten schreiben eigene Verzeichnisse. Die Originalmodelle
und alten Pakete bleiben unveraendert. Die Browseransicht verwendet dieselben
Geometrien; Positionsaenderungen werden ohne Skalierung auf die Tuerteile angewendet.

## Offene Punkte aus 02
Unveraenderte sechs statische Guss-/Deckblechkonflikte. Keine neue Maschinen-
Kollisionsfreigabe, keine Motor-/Lagerauslegung, keine originale PRT importiert.
