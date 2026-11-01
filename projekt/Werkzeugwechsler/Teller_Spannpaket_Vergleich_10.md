# Teller und automatische Werkzeugspannung – Recherche01.11.2026

Nutzervorgabe: Tischmagazin entfaellt, Teller zwingend. Eigenbau zulaessig,
kein Budget vorgegeben. Spindel muss automatische Spannung erhalten.
Aktuell **kein belegter Preis-Leistungs-Sieger**: Direkte AliExpress-Seiten
waren nicht lesbar, der Browserversuch wurde von der Site-Safety-Policy blockiert.
Keine Umgehung, keine Anfrage, kein Kauf. Titel aus Preisarchiven belegen
weder Lieferumfang noch den aktuellen Preis einer bestimmten Variante.

## Konkrete Kandidaten

| Kandidat | Einordnung | Preis-/Liefergrenze |
|---|---|---|
| [Nutzerartikel1005009887984460](https://de.aliexpress.com/item/1005009887984460.html) | Identitaet noch unbekannt; Titel/Variante beim Nutzer angefragt | Kein Preis oder Lieferumfang auslesbar |
| [Mech-Parts1005010692739531](https://www.aliexpress.com/item/1005010692739531.html) | Rotary/Umbrella, BT30 und Luftzylinder im archivierten Titel; erste technische Pruefprioritaet | Archiv988.40USD vom30.10.2026; kein aktuelles Angebot/DE-Endpreis |
| [Disc1005013224584008](https://www.aliexpress.com/item/1005013224584008.html) | 8/12/16/20, Luftzylinder, fuer NEMA34 im archivierten Titel | Archiv1327.37USD vom20.09.2026; 'fuer NEMA34' bestaetigt keinen mitgelieferten Motor |
| [Stellar1005010546824456](https://www.aliexpress.com/item/1005010546824456.html) | Rotary Disk, BT30 als Variante | Archiv1285.52USD vom31.10.2026; Umfang und Gesamtpreis offen |

Sekundaere Identifikationshilfen: [Mech-Parts](https://ms.pricearchive.org/aliexpress.com/item/1005010692739531),
[NEMA34](https://ms.pricearchive.org/aliexpress.com/item/1005013224584008),
[Stellar](https://ms.pricearchive.org/aliexpress.com/item/1005010546824456).
Abweichende niedrigere Suchlistenpreise konnten keiner Variante zugeordnet werden.
Kein Bestellpreis wird daraus in die Stueckliste eingetragen.

## Technische Empfehlung und Eigenbauvergleich

Vorlaeufig bevorzugt: kompakter8er-Teller, Kauf nur als vollstaendig belegtes
Paket mit Gabeln/Retention, Antrieb/Treiber, Referenz-/Endlagensensoren und
geeigneter Zustellung. Eigenbau kann bei Teller, Gestellkonsole und Schutzhaube
sinnvoll sein; eine komplette Indexierung/Teleskopmechanik ist kein kostenloser
Zusatz. Material, Lagerung, Antrieb, Elektrik, Fertigung und Einstellzeit sind
gemeinsam zu vergleichen. Ohne belegte Variantenpreise keine Rangliste nach Preis.

[HOLRY](https://www.holry.net/iso-bt-hsk-disc-cylinder-rod-type-servo-tool-magazine-for-atc-spindle-motor.html)
belegt eine passende Produktfamilie mit BT30-Varianten,200mm Hub und1:40-Untersetzung.
Motoroptionen sind750W,400W oder86Hybrid. Die L1/L2-Tabelle ist ohne passende
BT30-Zeichnung keine freigegebene Gesamthuelle. Identitaet mit einem der
AliExpress-Angebote ist nicht nachgewiesen. Unser Layout braucht etwa419mm
Zustellung;200mm Familienhub genuegt dafuer nicht.

## Spannpaket ist Pflicht, kein optionales Zubehoer

Vorzug zur Untersuchung: komplette riemengetriebene BT30-ATC-Patrone mit
abgestimmtem Greifer, Zugstange, Tellerfederpaket und Loeseeinheit. Der Teller
kann davon unabhaengig selbst gebaut werden. SK30/M12 DIN2080 bleibt im
Bestandsmodell; kein einfaches Aufschrauben eines Zylinders macht daraus BT30.

[DAIYA BT30SP](https://daiya.co.jp/en/product/spindle/atc/) nennt8000/min,
1200N Spannkraft und2000N Loesekraft. Diese modellspezifischen Werte werden
nicht fuer unsere Spindel angesetzt. Der komplette Loesehub und Lieferumfang
muessen zum gewaehlten System passen.

[CHUMPOWER BA900TTB30001A](https://www.chumpowerchuck.com/en/products_i_OTT.html)
ist ein BT30-45-Grad-Greifer, keine komplette Patrone.10kN ist sein maximaler
Greiferkraftwert, keine berechnete Sollspannkraft;1mm Ausstossweg ist nicht der
gesamte Zylinderhub. Kein Federpaket aus diesen beiden Zahlen ableiten.

[Automation Technology Komplettkit](https://www.automationtechnologiesinc.com/products-page/cnc-spindle/bt30-belt-drive-spindle-kit)
ist eine Lieferumfangsreferenz:2.2kW,6000/min, Spindel/Halter/Zylinder/Rahmen,
Motor/Treiber/Riemenantrieb. Angezeigter Artikelpreis2780USD; Versand/Einfuhr
nach Deutschland ungeklaert. Kein Preis-Leistungs-Sieger und kein nachgewiesener
Einbau in den SX3.5Z-Kopf.

## Was der neue CAD-Stand zeigt

Parametrischen Eigenentwurf mit8 Plaetzen, seitlichem Parkraum, eigenem
Zustellbauraum, Gestellstuetze und Spritzschirm. Orange Spannpaketkoerper zeigen
nur zu reservierenden Funktionsraum oberhalb der Originalspindel. Sie enthalten
keine erfundenen Federanzahlen, Kraefte, Greiferpassungen oder Sensorfreigaben.
Die automatische Werkzeugspannung ist **noch nicht konstruktiv geloest**.

Vor einer realen Ausfuehrung fehlen: Istmasse am Kopf/Spindeldurchgang,
gemeinsame Masszeichnung der ausgewaehlten Patrone, Loesekraft und Hub,
Spannkraftnachweis, Lastabstuetzung, Orientierung, Endlagenerkennung,
Werkzeug-/Anzugsbolzensystem sowie Z-Massen-/Freiraumpruefung.
