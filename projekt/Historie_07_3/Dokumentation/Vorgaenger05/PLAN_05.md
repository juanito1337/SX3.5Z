# K05 — Senktuer / Umsetzungsplan

Auftrag: Tuer nach UNTEN oeffnen, nicht nach oben. Native NX-Teile aus
bestehendem Rezept weiterverwenden, Maschine und kompakte Grundflaeche erhalten.

Entscheidung: zwei nach unten teleskopierende Segmente in getrennten Tiefenebenen.
Das bisherige 1040-mm-Blatt wuerde bei -1025 mm Hub den Boden um 195 mm
unterschreiten (750+80-1025). Zweiteilung erhaelt 760 x 1000-mm-Oeffnung
und 930-mm-Tischhoehe. Schienen nicht ueber Dach. 2:1-Bewegungsbeziehung ist
nur modellierte Sollkinematik; die Kopplung, Haltesicherung und Antriebe werden
nicht als konstruiert oder ausgewaehlt behauptet.

- [x] T1: Tests fuer negative Z-Bewegung, Teleskopueberdeckung, Bodenfreiheit,
  Fuehrungsueberdeckung, unveraenderte restliche Maschine. RED protokollieren.
- [x] T2: Rezept, Parameter, Lagebericht, native Versionskennung anpassen.
- [x] T3: Browserbewegung pro Segment und CAD-Stichproben anpassen.
- [x] T4: Geometrie, offene/geschlossene Browserbilder, Dokumentation, ZIP-Test.

Keine neue NX-API; bestehender Adapter unveraendert. Keine Originaldatei
ueberschreiben. Keine Sicherheits-, Dichtheits- oder Fertigungsfreigabe.
Autoren-Selbstpruefung, kein zweiter Agent und kein nativer NX-Lauf.
