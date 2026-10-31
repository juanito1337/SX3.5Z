# Was die bereitgestellten BF20-Anleitungen tatsächlich verwenden

Basis: BF20_neu.zip und BF20_alt.zip, vom Nutzer bereitgestellt. Kein Austausch durch Internetmaße.
`Quellen/BF20_Spindeln_Quellenauszug.pdf` enthält fünf unveränderte Quellenseiten, mit Lesezeichen.

| Achse | Spindel in gemeinsamer Fertigungsliste | Rohteilangabe Spindel | separates Verlängerungs-Rohteil | Lagerbezeichnung dort |
|---|---|---:|---:|---|
| X | KG-Spindel 16 × 4 | 683 mm | 85 × Ø16 mm | 3000-2RSR und 6000-2RSR |
| Y | KG-Spindel 16 × 4 | 287 mm | 90 × Ø16 mm | 3000-2RSR |
| Z | KG-Spindel 16 × 4 | 410 mm | 100 × Ø24 mm | 3003-2RSR |

Quelle: `Stückliste anzufertigende Teile.pdf`, Seite 1. Die Datei ist in beiden Archiven bytegleich und ausdrücklich **BF20 alt** betitelt. Die Zahlen stehen in der Spalte **Rohteil**, nicht als Gesamtlänge des fertig montierten Spindelstrangs. Verlängerungen sind eigene Teile. Rohteil und Verlängerung dürfen deshalb nicht unkritisch addiert werden.

Die Liste nennt für jede Achse eine HTD-5×9-Spindelscheibe mit 30 Zähnen und ein Motorritzel mit 15 Zähnen. Daraus folgt rechnerisch: zwei Motorumdrehungen pro Spindelumdrehung; bei 4 mm Steigung ergeben sich 2 mm Vorschub pro Motorumdrehung.

Der Zeichnungssatz `BF20_neu.pdf` zeigt auf PDF-Seite 19 (BF20-20) ein 666-mm-Maß am langen Abschnitt der X-Spindel, auf PDF-Seite 20 (BF20-21) 275 mm bei Y und auf PDF-Seite 21 (BF20-22 C) eine 400-mm-Bemaßung bei Z. **Die Bezugspunkte sind nicht mit der Rohteilliste identisch.** Besonders bei Z beginnt das Maß im Bereich der eingesteckten Verbindung zur Verlängerung. Diese 400 mm sind weder ohne Weiteres die freie Kugellaufbahn noch die vollständige Baugruppenlänge.

Alt-/Neu-Spindelenden und Lagerdetails unterscheiden sich. Die gemeinsame Liste ersetzt nicht die zugehörige Variantenzeichnung. `Montage der Z-Spindel.pdf` beschreibt den Originalumbau der BF20; die Montagefolge und Gegenbauteile sind nicht als SX3.5Z-Anschluss nachgewiesen.

`Umbauanleitung.pdf` zeigt/benennt Isel-Spindeln und Schrittmotoren Sanyo Denki 103H78231740. Das ist kein Nachweis für eine aktuelle Bezugsquelle oder eine Servoausrüstung.

## Abgrenzung zum aktuellen Modell
Der SX3.5Z-Ansichtsentwurf verwendet weiterhin Direktantrieb, 16×5 für X/Y und 20×5 für Z. Diese Auswahl ist ein anderer Entwurf. Die BF20-Rohteillängen werden **nicht** als passende SX3.5Z-Bestelllängen übernommen. Die früheren 352-/252-mm-Katalogstudien aus Entwicklung09/10 waren reine Referenzpaare, nicht Achs-Bestelllängen für die Gesamtmaschine.

Die K02-Längenrechnung enthält Spindelhüllen, Muttern-/Aufnahmehüllen und 10 mm gewählte Reserve. Sie prüft weder Gewindeausläufe, reale Mutterbefahrbarkeit, kritische Drehzahl/Knicken noch Lagerpositionen und Führungsüberdeckung. Sie ersetzt keine Endenbearbeitungszeichnung.
