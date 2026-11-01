# Übergabe des letzten Gesprächs: automatische Werkzeugspannung

## Produktauswahl01.11.2026 ergaenzt

Magazinartikel1005009887984460 ist vorerst gewaehlt; sechs Lieferantenbildkopien
liegen im Repository. Die konkrete Werkzeugaufnahme ist noch nicht bestaetigt.
Der BAIDI SU32X200-S im Bild gehoert zur Magazinzustellung; er ist kein
nachgewiesener Spindel-Loesezylinder. Das ZD-25W-Aggregat treibt das Magazin,
nicht die Fraesspindel. Kein Feder-/Greifer-/Zugstangenpaket aus diesen Bildern
ableiten. OriginalSK30/DIN2080/M12 bleibt von einer ATC-Schnittstelle zu trennen.

## Stand11

Rechter Teller erreicht die nominelle Spindelachse/-hoehe in einer eigenen
NX-Wechselbaugruppe; native Halterkegellage gemessen. Die mechanische Schnittstelle
SK30/M12 zu BT30 und das automatische Spannpaket sind weiterhin offen. Sichtbare
Koaxialitaet ist kein Greifer-/Federkraft-/Passungs-/Lagerlastnachweis.

## Fortschreibung01.11.2026: Pflichtanforderung und offener Nachweis

Der Nutzer hat das Spannpaket ausdruecklich als zwingend bezeichnet. Neuer
Tellerentwurf10 ersetzt das Tischmagazin; drei orange Raumkoerper markieren
Anschluss, Feder-/Spanneinheit und Loeseeinheit. **Dies ist noch kein ausgelegtes
Spannpaket.** SK30/M12 bleibt unveraendert, keine BT30-Kompatibilitaet behauptet.

Lieferantenvergleich mit DAIYA/CHUMPOWER/Automation Technology sowie
AliExpress-Tellern unter `projekt/Werkzeugwechsler/Teller_Spannpaket_Vergleich_10.md`.
Kopfaufmass, abgestimmte Herstellerzeichnung, Kraft-/Hub-/Lagerlastnachweis,
Sensorik und Orientierung fehlen. Aktueller Schnittstellenbericht traegt `_10`.
Die folgenden Aussagen zum fehlenden Modellzusatz und6er-Magazin beschreiben09.

**Status: Konzeptdiskussion, noch keine entsprechende Modelländerung und keine Kaufentscheidung.**
Diese Notiz dokumentiert den letzten besprochenen Ansatz; sie ist keine neue Lieferantenauslegung.
Die vorhandenen Katalog-/Quellenbelege bleiben unter `projekt/Quellen/` und
`projekt/Werkzeugwechsler/`. Referenzen aus dem letzten Gespräch sind am Ende genannt,
bei der Übergabe aber nicht erneut technisch geprüft worden.

## Ausgangspunkt

Die Originalspindel bleibt als SK30/M12 DIN2080 modelliert. Im Stand09 liegen sechs
BT30-ER20-70-Raumreferenzen in einer Magazinoption. Die automatische Spann-/Löseeinheit fehlt;
`machine_operation_enabled`, `spindle_clamping_verified` und `trajectory_verified` sind false.
Siehe `projekt/Werkzeugwechsler/ATC_Schnittstellenstatus_09.json`.

## Besprochenes Prinzip

Greifer hinter dem Werkzeugkegel, Zugstange durch die Spindelwelle, Feder-/Spanneinheit im
oberen Spindelbereich, koaxiale Löseeinheit oberhalb. Das genaue Prinzip und die Innenkontur
müssen vom gewählten Hersteller stammen. Federkraft hält, die geeignete Betätigung löst;
keine Federanzahl, Spannkraft, Luftdruck- oder Zylinderdimension ist bisher verbindlich bestimmt.
Die Lastabstützung beim Lösen und die Beanspruchung der Lager sind eigens zu prüfen.

## Variante A – Originalspindel umbauen

Vorhandene Werkzeugspindel/Pinole ausbauen und Innenkontur messen. Nicht nur der Zugstangendurchgang,
sondern auch Greiferbewegung und definierte Führungs-/Spannflächen müssen Platz haben.
Mögliche Neuteile: Greifer/Zugstange/Federaufnahme, steife Lösezylinderbrücke und ggf. neue Spindelwelle.
Kein "einfach aufbohren" aus einer Fotoannahme. Tragfähige Aufnahme am Kopf, nicht am Riemenschutzblech.
Herstellung, Härte/Schliff, Wandstärken, Lagerstellen, Rundlauf und Montage bleiben ungeklärt.

## Variante B – vollständige ATC-Spindelpatrone

Als bevorzugt zu UNTERSUCHENDE Richtung wurde ein zusammengehöriges System aus Spindel,
Lagerung, Spannung und passender Lösebetätigung empfohlen. Die manuelle Pinolenbewegung
würde entfallen; der gesamte Kopf übernimmt CNC-Z. Die Werkzeugachse soll möglichst erhalten bleiben.
Eine Präzisionsaufnahme im vorhandenen Kopf oder ein neuer Träger am Z-Schlitten wäre zu vergleichen.
Noch keine Patrone gekauft oder als einbaufähig nachgewiesen. Originalmotor nur nach Prüfung
von Übersetzung, Drehmoment/Drehzahl und Orientierung übernehmen.

## Zunächst benötigte Informationen

| Eingang | Inhalt |
|---|---|
| Reale Spindel | Innenkontur, Durchmesser/Tiefen, nutzbare Durchgangsgeometrie, Nasen-/Lagerbezüge |
| Pinole/Kopf | Durchmesser/Länge der Aufnahme, Wandstärken und belastbare Anschlussflächen |
| Freiraum | Riemenscheibe, Motor und Platz über der Spindel bei höchster Kopfstellung bis Einhausungsdach |
| Kandidat | Maßzeichnung/STEP, Schnittstelle/Halter/Anzugsbolzen, Spann-/Lösekräfte und Hub, Masse |
| Funktion | Antrieb, Orientierung, Sensoren, Ausstoß, Luft-/Hydraulikbedarf, Verhalten bei Störung |

Ohne diese Daten keine endgültigen Adapterbohrungen, Passungen, Federpakete oder Kopf-Fräsarbeiten.

## Auswirkungen auf den bisherigen Stand09

Das Tischmagazin belegt 620 × 100 mm der nominal 740 × 180 mm Tischfläche. Die 16,6 mm
Höhenreserve gilt nur für die bisher angesetzte Hüllkombination. Ein neuer Spindelkopf, echte
Werkzeuglängen und Spannmittel können das Ergebnis verändern. Die alte Endpunktprüfung ließ
außerdem den aufzunehmenden Halter wegen der offenen Schnittstelle aus: kein Funktionsnachweis.
Spindelentscheidung zuerst, dann Magazin/Schutzhaube/Retention und die gesamte Wechselbahn anpassen.
Kein ausführbares M6-Makro mit geschätzten Koordinaten erstellen.

## Quellenpfade und Referenzen

- Projekt: `projekt/Quellen/Quellen_09.json`, Quellen S09-10 bis S09-13.
- Projekt: `projekt/Werkzeugwechsler/Lieferantenanfrage_ATC_09.txt`.
- Letztes Gespräch, nicht neu validiert: RÖHM automatische SK-Spannsysteme,
  https://www.roehm.biz/en/products/tool-clamping-systems/sk-automatic-clamping-systems/
- Letztes Gespräch, nicht neu validiert: OTT-JAKOB Steilkegel,
  https://www.ott-jakob.de/en/steep_taper/
- Letztes Gespräch, nicht neu validiert: Fischer Spannsystem-Erläuterung,
  https://repair.fischerspindle.com/news/spindle-system-clamping-system

## Nächster Liefergegenstand

Ein belegter Variantenvergleich mit Schnitt-/Einbauskizze, Messliste, Kraftfluss,
Kaufteil-Lieferumfang, Restfreiräumen und nötigen Originalteilbearbeitungen.
Erst nach Entscheidung eine neue native NX-Konstruktionsrevision mit den realen Schnittstellen beginnen.
