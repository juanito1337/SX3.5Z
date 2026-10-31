# K04 Hubtuer — Umsetzungsplan

Ziel: Korrektur des Nutzerwunsches: vertikale statt horizontale Tuerbewegung.
Grundflaeche 1650 x 1000, Maschine, CNC-Antriebe, Gestell, KSS und Schaltschrank
bleiben unveraendert. Keine neue NX-API. Keine neuen Fertigungsfreigaben.

Entscheidung: eine nach oben verfahrende Tuer, kein Klappen und keine Teleskopkinematik.
Die feste Fuehrung wird ueber das Dach hinaus verlaengert. Den Platzbedarf der
festen Fuehrung auch bei geschlossener Tuer nennen. Gewichtsausgleich, Fangsicherung,
Zuhaltung, Dichtungen und Tragfaehigkeit bleiben offene Auslegungen.
Die wiederholte Bitte um Modellanpassung und die Korrektur 'vertikal' gelten als
Auftrag zur direkten Umsetzung dieser Anschauungsvariante.

- [x] 1. Fehlende Hubtuerfunktion mit Tests nachweisen (RED).
- [x] 2. Parametrische Tuer, vertikale Fuehrungen, Laengenkette (GREEN).
- [x] 3. Browserbewegung +Z statt +/-X; NX-Einstieg auf Version 04.
- [x] 4. Vollstaendiger lokaler Geometrieaufbau und Tuer-Stichproben.
- [x] 5. Browser visuell und funktional testen, Paket frisch entpacken/pruefen.

Kein nativer NX-Lauf in dieser Umgebung. Unabhaengiger CAD-Kern dient nur
Geometriepruefung und Ansicht, nicht als Ersatz fuer das native NX-Journal.
