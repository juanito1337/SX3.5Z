# Stand12: BT30-Wechsler auf rechter Saeulenkonsole

01.11.2026. Nutzer priorisiert die sinnvolle Magazinbefestigung; eine spaetere
BT30-Spindel beziehungsweise passende automatische Spannung bleibt offen und
blockiert die Einbaustudie nicht. Grundlage ist die vorhandene SX3.5Z, kein
neuer Maschinenentwurf. Rechts parken, zur Spindel zustellen, Tisch frei halten.

## Anordnung

- Feste Anschlussplatte an der nominalen rechten Saeulenflaeche, Tragplatte
  und zwei obere Verstaerkungsrippen. Der Tisch kann unter der Konsole fahren.
- Linearer Einschub schraeg von rechts vorn zur Spindel. Arbeitsannahme200mm
  Hub statt389.33mm im bisherigen Entwurf. Parkmittelpunkt ca329.09/-190mm,
  Wechselmittelpunkt ca155.88/-90mm; Werkzeugaufnahme in Wechselstellung0/0.
- Werkzeug-Bezugshoehe400mm, angehobener Kopf fuer Zustellung und anschliessend
  Absenkung zur Uebergabe. Der Z-Bewegungsablauf ist nur geometrische Studie.
- Die bisherige Gestellstuetze, ihr Dichtkragen und die Wannenoeffnung entfallen.
  Bestehende Sammelwanne wieder ohne Stuetzendurchbruch. Vier seitliche
  Fangbleche und die entfernten61 Originalanbauten bleiben wie in11.
- Halboffener Park-Spritzschirm mit Dach bleibt. Ein dichter Magazinverschluss,
  Befestigung der Haube und Abstreifer sind noch auszuarbeiten.

## Quellen und Annahmen

| Geometrie | Wert | Herkunft / Nachweisgrenze |
|---|---:|---|
| Grundplatte |330x175x22mm|Lieferantenbild4; ohne erfundenes Lochbild|
| Tellerscheibe |Durchmesser280mm, Dicke16mm|Lieferantenbild5; kein Werkzeugteilkreis|
| Werkzeugaufnahme |BT30|Nutzer ausdruecklich bestaetigt|
| Zustellung |200mm|Aus SU32X200-S abgeleitete Arbeitshypothese; nutzbarer Hub unbestaetigt|
| Werkzeugradius |180mm|Entwurf, NICHT aus Scheibendurchmesser abgeleitet|
| Schlitten/Teller-Achsversatz |70mm|Entwurf|
| Motor, Lager, Fuehrung, Traeger, Zylinderhuellen |vereinfachte Volumen|Unbestaetigte Entwurfsabmessungen, keine Hersteller-CAD-Geometrie|
| Anschlussplatte/Tragplatte/Rippen |12/15/8mm|Vorentwurf; Lasten, Materialguete, Schrauben und Festigkeit fehlen|
| Werkzeughalter und Gabeln |uebernommene Huellen|Keine nachgewiesene RATTM-Greifergeometrie oder Retention|

Produktbelege: `Werkzeugwechsler/Produktdaten_RATTM_1005009887984460.json` und
`referenzen/kaufteile/rattm_1005009887984460/`. Die Fotos belegen weder
Betriebsorientierung noch alle Achsabstaende. Das Modell ist eine Einbaustudie
des ausgewaehlten Produkttyps mit zwei belegten Aussenkonturen.

## Aufbau und offene Befestigung

Die Anschlussplatte liegt an der nominalen rechten Saeulenflaeche. Keine
Bohrung, kein Gewinde und keine Freistellung wird in das Originalgussmodell
eingebracht. Vor Fertigung: Anschlussflaeche/Wandstaerke/Rippen aufmessen,
Schraubverband und Lastfall aus Wechslermasse/Werkzeuglast auslegen. Tragplatte
und Rippen stellen eine moegliche geschweisste Konsole dar, keine freigegebene
Schweisskonstruktion. Justage und Demontagezugang sind noch zu detaillieren.

Magazin komplett als eine KaufpositionO10-TELLER fuehren. Eigene Konsole und
Haube sind separate Fertigungspositionen. Keine Doppelbestellung des Motors,
Zylinders oder der acht Gabeln aus den vereinfachten Einzelkoerpern ableiten.
Aktuelle Tabellen tragen `_12`; Tabellen09/10/11 sind historische Staende.

Die OriginalspindelSK30 bleibt im Modell als Referenz. Der gewaehlt darstellte
BT30-Halter wird zur nominellen Achse gefuehrt; seine Ueberschneidung mit dem
Bestands-Spindelraum ist keine Passungspruefung. Spaetere Spindelwahl und
Spannpaketauslegung muessen die festgelegten Uebergabebezuege uebernehmen oder
die Anordnung erneut pruefen. Orange Spannpaketkoerper bleiben Raumreserven.

## Pruefumfang

Die erste Offline-Pruefung fand52 Schnittbefunde der unteren Konsolenrippen
mit Tisch/X-Antrieb in17 Stellungen. Ursache war der zu tief liegende
Rippenverlauf. Rippen oberhalb der Tragplatte und hinter der Grundplatte
beseitigten diese Befunde im gleichen Pruefumfang:470 BRep-Schnittpruefungen,
keine Kollision bei5 Zustell-,4 Kopf-Absenk- und8 Park-Achseckstellungen.
Das prueft den nominalen geometrischen Entwurf, nicht die reale Maschine.

Ausgeschlossen: ausgewaehlter Halter gegen alte Spindel/Kopf, Spannpaketreserven,
verformbare Baelge, innere Passungen der vereinfachten Kaufteilhuellen,
Werkstuecke/Spannmittel und ueber die Halter hinausgehende Fraeser. Keine
kontinuierliche Bahn-, Festigkeits-, KSS-Durchsatz- oder Betriebspruefung.
Sechs bekannte Maschinenanschluss-Konflikte und35 Istmasse bleiben offen.

Native Erzeugung/Wiedereroeffnung und konkrete Laufpfade werden im
`cad/README.md` und im Ergebnisverzeichnis zur Revision12 nachgewiesen.
Kein nativer Erfolg allein aus Offline-Pruefungen ableiten.

`build_ready`, `purchase_released`, `machine_operation_enabled` und
`atc_operational` bleiben false.
