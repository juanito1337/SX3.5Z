# Stand11: rechter Teller, Wechselstellung und beidseitiger Spaenefang

01.11.2026, Basis7bffcd4. Aktuelles Rezept CNC_UMSETZUNG_11_FANGBLECHE.
Nutzer hat die rechte Parkseite ausdruecklich bestaetigt. Seine drei markierten
NX-Ansichten sind Anforderungsskizzen, keine vermessenen Bauteilzeichnungen.
Original-CAD anderer Rechnerordner wurde nicht verwendet.

## Werkzeugwechsler bis zur Spindel

Es gibt zwei getrennt erzeugte native Baugruppen aus demselben Rezept:
PARK und WECHSEL. Einstieg und genaue Laufpfade: ../../cad/README.md.
Die Wechselstellung faehrt den ersten Werkzeugplatz auf X=0/Y=0 und auf die
nominelle Spindelflaeche Z=370mm. Der Kopf steht dafuer bei head_down=160mm.
Die rechte Parklage liegt etwa bei X=512,97/Y=-246,99mm. Der erforderliche
Zustellweg betraegt389,33mm. Die Diagonale nach vorn/rechts ist eine Entwurfswahl
fuer Freiraum zwischen benachbarten Haltern und Gusskopf, kein Herstelleranschluss.

Die Parkhaube hat jetzt440mm Aussendurchmesser und2mm Wandstaerke.
Ihr Innenradius218mm laesst nominell11,10mm gegenueber den Gabelecken.
Die bisherige Haube hatte fuenf echte Ueberschneidungen; diese wurden im
neuen Wegtest gefunden, reproduziert und korrigiert. Durch das Hereinruecken
der Parklage bleibt die groessere Haube innerhalb der Einhausung.
Die rechte Gestellstuetze traegt die Konsole; die Durchfuehrung/Dichtkragen
liegt jetzt im rechten Leitblech. Die linke Durchfuehrung entfaellt.

Aus `projekt/` bzw. mit absolutem Pfad in NX ausfuehren:

- NX_CNC_Gesamtansicht.py: neue komplette Parkstellung.
- NX_CNC_Wechselstellung.py: neue komplette Wechselstellung.
- NX_Git_Lieferstand_Pruefen.py mit SX35Z_VERIFY_RUN: den jeweiligen Lauf frisch oeffnen.

Eine Datei stellt jeweils einen Zustand dar, keine gekoppelte Animation.
Die native Lagepruefung misst die erzeugte Halterkegelgeometrie gegen die
nominelle Spindelachse und -hoehe. Das ist **kein Passungsnachweis**:
SK30/M12 bleibt Originalbestand, BT30-Halter und automatisches Spannpaket
sind weiterhin nicht aufeinander abgestimmt. Die drei Spannpaketkoerper
bleiben Funktionsraumreserven. Keine M6-Funktion oder reale Maschinenbewegung.

## Spänefang links und rechts

Vier neue geneigte2mm-Fangblechvorformen bilden beidseitig der Maschineninsel
eine offene Rinne. Je Seite reichen sie von |X|=227 bis500mm, Rinnengrund bei
|X|=350mm; Laengsbereich Y=-220 bis382mm. Hinterer Rinnengrund40mm, innere
Kante80mm, aeussere Kante90mm; Gefaelle nach hinten4%. Die vorderen Kanten
liegen durch das Gefaelle24,08mm hoeher. Die hintere Kante wirft in die darunter
vorhandene Sammelwanne ab; deren Trichter, Grobkorb und KSS-Ruecklauf bleiben.

Neue Parameter catch_z, catch_rise, catch_slope in Layout_Parameter_11.json.
Die seitlichen Aussenbereiche bleiben durch die vorhandene Einhausungswanne
abgedeckt. Fangbleche sollen abnehmbar sein; Halter, Verschraubungen, Fugen und
Zugang darunter sind noch zu detaillieren. Lange Spaene werden durch4% Gefaelle
nicht nachweislich selbst gefoerdert; Spaene-/KSS-Durchsatz und Reinigung bleiben offen.
Vier native parametrische Blechvorformen sind keine nachgewiesenen Abwicklungen
und keine zusaetzlich behaupteten NX-Blechkonvertierungen. Pflichtmodus required
bleibt fuer die bereits gekennzeichneten Blechbauteile aktiv.

## Demontage und weiter benoetigte Funktionen

61 Originalanbauteile sind aus dem neuen CAD-Rezept entfernt, getrennt
aufgelistet in ../Pruefung_11/Demontageliste_11.json:

- Altes Bedienpanel samt Halter, Tastern und Anzeige.
- Originale Blech-Elektrosaeule samt dortigen Elektro-/Kabelanbauten.
- Alte Spindelschutzscheiben, deren Halter, Riemenhauben und alte Arbeitslampe.

Die Liste enthaelt auch den alten Not-Halt, Z-Endschalter, XMT-Treiber und
PE-Schiene. Ihre Funktionen sind dadurch **nicht entbehrlich**. Not-Halt,
Schutzleiter-/Potentialausgleich, Endlagen, Motorregelung und Schutzverriegelung
muessen im neuen CNC-Schaltschrank/Aussenpult fachgerecht ersetzt bzw. neu
verdrahtet und geprueft werden. Die modellierten neuen Geraetehuellen sind kein
fertiger Stromlaufplan. Es wurde nur das CAD-Modell geaendert.

Spindelmotor, tragende Gusskoerper, CNC-Antriebe, neue Schrank-/Bedienpultteile
bleiben erhalten. Ebenso Faltenbalg_Z und Faltenbalg_Y_hinten: Sie schuetzen
Fuehrungen im Spaene-/Nassraum; die Einhausung ersetzt diese Funktion nicht.
Keine Gussbearbeitung oder neue Passung aus einer Bildmarkierung abgeleitet.

## Zusammengehoerige Daten und Nachweise

454 Einzelteile,17 Unterbaugruppen. Vier neue Fangbleche,61 entfallene
Originalanbauten; bisheriger Stand10 mit511 Teilen bleibt historisch erhalten.
Aktuell: Einkauf/*_11.csv, Pruefung_11/, Werkzeugwechsler/ATC_Schnittstellenstatus_11.json.
70 Katalogpositionen,148 Fertigungspositionen; alle Freigaben bleiben false.
Alte Parameterdateien wurden nicht geaendert. Layout_Parameter_11.json legt
explizit rechte Richtung und neue Parkdistanz ueber die alten10-Werte.

Offline173 Tests und99 Untertests bestanden. Teller:552 Endpunktchecks gegen
Gusskopf/Frontplatte/Pinole ohne Kollision; ausgewaehlte Halter-Spindel-Passung
ausgenommen. Neuer Wegcheck: neun endliche Stellungen,87 notwendige BRep-
Schnittpruefungen, keine Kollisionen. Erst Zustellen bei hohem Kopf, danach
Absenken. Keine kontinuierliche Bahnpruefung, keine realen Werkzeuge/Spannmittel
oder nachgewiesene Indexierung/Retention/Lagerung.

KSS-Check: acht Achsecken und Korbauszug ohne Kollision. Exit1 bleibt wegen
sechs unmontierter IFS206-Prueffeldreferenzen gegen das linke Leitblech bestehen.
Die beiden verformbaren Faltenbaelge sind von der starren Achsverschiebungspruefung
ausgeschlossen. Die sechs bekannten Maschinenanschluss-Konflikte sind ein
anderer Befund und weiter offen; ebenso35 Istmasse und der hintere Tankauszug.

Native Ergebnisse, Quellrevision/-hashes, genaue Befehle, Datum, Umgebung,
Exitcodes und Rohprotokolle stehen bei den neuen CAD-Lieferordnern und unter
ergebnisse/entwicklung/20261101_revision11. Kein Bau-/Bestell-/Betriebsnachweis.
