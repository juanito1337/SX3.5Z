# Entscheidungen und offene Annahmen

## Nutzerentscheidung01.11.2026: konkreter AliExpress-Werkzeugwechsler

Der Nutzer legt Artikel1005009887984460 als zu verwendenden Werkzeugwechsler
fest und verlangt die auf der Artikelseite enthaltenen Massbilder zur Ansicht.
Quelle: https://de.aliexpress.com/item/1005009887984460.html
Das ersetzt fuer das Magazin die bisherige offene Eigenbau-/Kaufproduktwahl.
Die genaue Variante, Abmessungen und der Lieferumfang sind noch nicht auslesbar.
Artikel- und Variantenkennungssuche lieferte keine zuordenbaren Massbilder;
Direktzugriff schlug fehl. Keine fremden Produktzeichnungen als Ersatz zuordnen.
CAD11 bleibt bis zu belegten Abmessungen die bisherige Eigenentwurfsgeometrie,
nicht das Herstellerabbild dieses Artikels. Auswahl ist keine Bestellung oder
Passungs-/Betriebsfreigabe. Spindel-/Spannpaketauswahl bleibt davon unabhaengig offen.

## Nutzerkorrektur01.11.2026: rechte Parkseite, Spaenefang, Demontage

Nutzer fordert Reichweite bis Spindel und Spaenefang links/rechts der Maschine.
Original-Schutzabdeckungen, Elektroanbauten und Schutzbleche duerfen fuer den
eingehausten CNC-Umbau entfallen. Auf Rueckfrage ausdruecklich bestaetigt:
Teller rechts neben dem Kopf parken und von dort zur Spindel fahren.

Umgesetzt als getrennte native Park-/Wechselstellungen, vier Fangbleche und
61 explizit aufgelistete entfallene Originalanbauten. Werkzeugeingriff/Spannpaket
ist dadurch nicht freigegeben. Tragende Gussbauteile, Motoren, neue CNC-Elektrik
und Fuehrungsbaelge bleiben erhalten. Alte elektrische Funktionen muessen im
Neuaufbau ersetzt werden. Abmessungen bleiben Entwurf, keine Bild-Istmasse.

## Nutzerentscheidung01.11.2026: Teller und zwingendes Spannpaket

Werkzeugwechsler darf nicht auf dem Tisch stehen; Tellerbauform erforderlich.
Kein Budget oder feste Platzzahl vorgegeben; Eigenbau erlaubt, guenstiges passendes
Kaufprodukt ebenso. Spindel muss Spannpaket erhalten. Nutzer nennt den moeglichen
AliExpress-Artikel1005009887984460; Identitaet/Variante noch nicht auslesbar.
Keine Bestellung, Herstellerwahl oder Passungsfreigabe daraus ableiten.

Bearbeiterentwurf10:8 Plaetze, seitliche Gestellstuetze, radiale Zustellreserve,
Spann-/Loeseraum oberhalb Originalspindel. Das sind Entwurfsannahmen; die
automatische Spannung ist noch nicht ausgelegt. Komplette passende BT30-Patrone
weiterhin bevorzugt zu untersuchen, nicht endgueltig vom Nutzer ausgewaehlt.
Konstruktionsbericht: `projekt/Dokumentation/Entwicklungsstand_Teller_10.md`.

## Nutzerentscheidung 31.10.2026: neue native Dateien im Git-Projekt

Der Nutzer verlangt die Neuerzeugung der 3D-Dateien im Git-Ordner und ihre
Versionierung. Alte CAD-Dateien an anderen Orten des Rechners werden dafuer
nicht verwendet. Ausgangspunkt dieses Laufs sind ausschliesslich die aktuellen
Rezepte und Parameter unter `projekt/`; Ziel ist `cad/nx/`.
Dies ersetzt fuer diesen Lieferstand die zuvor vorgeschlagene Uebernahme alter
PRT. Es bestaetigt keine Fotoannahmen als Istmasse und erteilt keine Fertigungs-,
Bestell-, Betriebs- oder ATC-Freigabe.

Dieses Register fasst die sichtbaren Nutzervorgaben und den vorhandenen Code zusammen.
Es ist keine wortgetreue vollständige Chatarchivierung.

## Ausdrücklich vom Nutzer vorgegeben / im Gespräch akzeptierte Richtung

- Eigene vorhandene, bereits zerlegte SX3.5Z als Grundlage; Nachmessen ist möglich.
- Native, möglichst parametrische Siemens-NX-Konstruktion mit NX Open Python.
- Detaillierte Einzelteile zuerst, danach Gesamtbaugruppe; Farben nahe den Originalfotos.
- Reiner CNC-Betrieb, keine aktiven manuellen Handräder/Vorschubhebel.
- LinuxCNC und Mesa; passende Treiber/Verstärker separat, kein Motorleistungsbezug von der Mesa-Karte.
- Kompaktes Untergestell/Einhausung, Arbeitshöhe, Späne-/KSS-Rückhaltung.
- Breite Tür über fast die Frontbreite, vertikal **nach unten** öffnend; zweiteilige Teleskopausführung
  als akzeptierter Darstellungsstand. Nicht auf eine nach oben öffnende Tür zurückändern.
- Wirkliche Blechkonstruktion, Federunterstützung berücksichtigen; nicht nur massive Hüllquader.
- Fenster hinter dem Schaltschrank entfernen, Schrank direkt an die Seitenwand legen.
- Späne/KSS nach unten sammeln und zum Tank zurückführen; Front-Türraum nicht blockieren.
- Reale Norm-/Kaufteile, passende Einkaufsliste und Bauanleitung; nötige Originalteilbearbeitung ausweisen.
- Automatischer Werkzeugwechsler erwünscht; günstige AliExpress-Angebote untersuchen.
- Projekt mit Superpowers weiterentwickeln und jetzt nach Codex übergeben.

## Entwurfswerte / Bearbeiterentscheidungen, NICHT bestätigtes Istmaß

1.650 × 1.000 mm Einhausungsgrundfläche, 1.420 × 1.000 mm Türöffnung, 930 mm Tischhöhe,
2-mm-Bleche/angenommene Biegeradien, 1.030/515 mm Türhübe, vier Gasdruckfeder-Bauräume,
Schrank- und KSS-Dimensionen: im aktuellen Rezept hinterlegt, keine Fertigungsfreigaben.
Die neu gewählten Leadshine-Antriebe sind Closed-Loop-Schrittmotoren; die frühere Verwendung
von "Servo" im Gespräch ist keine bestätigte Umstellung auf einen AC-Servosatz.

## Offen, ausdrücklich nicht als endgültig entschieden behandeln

- Konkrete ATC-Spindel, Spannpaket, Anzugsbolzen, Lösezylinder und deren Kräfte/Hübe.
- Nachrüstung Originalspindel vs. komplette feste ATC-Patrone oder neuer Spindelträger.
- Originalmotor-/Antriebsweiterverwendung und Spindelorientierung.
- Tischmagazin dauerhaft akzeptabel oder alternatives Seitenmagazin erforderlich.
- Endgültige Lager-/Spindel-/Kupplungsbestellungen und Antriebsnachweise.
- Sicherheit, Türkopplung/Fangsicherung, Gasfedern, elektrische Schutzfunktionen und Inbetriebnahme.

Eine positive Bewertung einer Vorschau bedeutet keine Bestätigung ungeprüfter Maße oder Kräfte.
