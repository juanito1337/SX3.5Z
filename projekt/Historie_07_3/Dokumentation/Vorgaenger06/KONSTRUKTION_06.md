# Konstruktion 06 – Übertragung des freigegebenen Bildkonzepts in NX Open

## Umfang und Herkunft

Ausgangspunkt ist Gesamtansicht 05, nicht eine aus einem Bild abgeleitete neue Maschine.
Die ursprünglichen Modellrezepte werden weiterverwendet. Die jüngsten generierten Bilder
liefern Gestaltung und Zielaufbau, aber keinerlei belastbare Maße, Lagerstellen oder
Federnkennlinien. Sie sind keine CAD-Exporte.

Die Revision setzt die ausdrücklich gewünschte breite, nach unten öffnende Front und
blechgerechtere Bauteilzerlegung um. Der tragende Ständer bleibt ein Rohrprofilrahmen;
er wird nicht ohne Festigkeitsnachweis durch dünne Blechwände ersetzt.

## Geometrische Eckdaten – nominelle Entwurfswerte

| Größe | Wert |
|---|---:|
| Traggestell / nominale Einhausungsbasis | 1650 × 1000 mm |
| Größte Dachblech-Vorform | 1658 × 1004 mm |
| Lichte Zugangsöffnung | 1420 × 1000 mm |
| Anteil an nominaler Frontbreite | ca. 86 % |
| Türsegment außen, je Segment | 1460 × 530 mm |
| Profil-Bautiefe / Blechdicke | 30 / 2 mm |
| Gewünschter Innenbiegeradius / K-Faktor | 3 mm / 0,40 |
| Hublängen unten / oben | 515 / 1030 mm nach unten |
| Tischhöhe ab Boden | 930 mm |
| Gesamthöhe des Dachblechs ab Boden | 1952 mm |
| Unterkante des tiefsten Türsegments bei voller Öffnung | 310 mm ab Boden |
| Vorderste Kassettenfläche | 205 mm vor nominaler Einhausungsfront |

Griffe, Schrank und Füße benötigen zusätzlich Raum. 1650 × 1000 ist NICHT die gesamte
Aufstellfläche aller Anbauteile. Die Dach- und Seitenabstände wurden zur Biege-/Montagereserve
leicht vergrößert; seitlicher/realer Platzbedarf muss am realen Modell geprüft werden.

## Blechgerechte Zerlegung

16 Bauteile sind für die native NX-Sheet-Metal-Konvertierung markiert (siehe Blechliste_06.csv).
Jeder Kantkörper besitzt zwei parallele, offene Rückkantungen; komplizierte geschlossene
Vierfachkanten werden durch separate Querholme und Halteleisten vermieden.

Die Türrahmen bestehen aus einer U-gekanteten, ausgeschnittenen Front mit separaten
Querholmen. Die beiden Scheiben liegen zwischen Profil und dünnen Halteringen. Modelliert
sind vier durchgehende Befestigungen je Segment; ihre Anzahl, Klemmflächen und
Fensterbefestigung sind nicht belastungs- oder sicherheitstechnisch freigegeben.

Seitenwände, Rückwand, Dach, schmale Frontfelder, Federkanäle und Ständerschürzen sind
Dünnwand-Kantprofile. Die untere Kassetten-Servicefront ist bewusst ein separates
FLACHES Blech ohne Biegekonvertierung. Schnittkonturen/Ausklinkungen schaffen Freiraum
für Führungen und Federteile. Befestigungsflansche geben einen konstruktiven Anschluss vor;
nicht jedes noch offene Rahmenlochbild oder jede Naht ist fertig detailliert.

Native Aufbaufolge: assoziative Extrusion der scharfen Vorform, native Bohr-/Taschenabzüge,
danach Convert to Sheet Metal mit ausgewählter Basisfläche und Radiusvorgabe.
Keine ungeprüfte Abwicklung wird ausgegeben. Die Ausdehnung und Materialverteilung
kann sich durch die native Radiusbildung gegenüber der scharfen Vorform verändern.
Die Offline-Volumenreferenz prüft deshalb nur die Vorform, nicht den gerundeten Endkörper.

## Federunterstützung – Konzept, keine Bestellliste

Verwendet werden vier zylindrische Gasdruckfeder-Einbauräume mit getrenntem Gehäuse,
Kolbenstange und Augenhüllen, jeweils mit 515 mm relativem Hub. Kein Herstellerprodukt
und keine garantierte Verfügbarkeit dieser Abmessungen ist damit bezeichnet.

Zwei Federn wirken zwischen Festgestell und unterem Segment. Zwei weitere wirken
zwischen unterem und oberem Segment. Beim Öffnen nach unten werden sie komprimiert;
ihre Kraft wirkt nach oben. Sie helfen beim Wiederhochschieben zum Schließen und
ersetzen NICHT eine Fangsicherung oder Verriegelung.

Rechnerische Massenannahmen: 17,87 / 18,47 kg, Stahl 7850 kg/m³, Scheiben 1200 kg/m³,
plus geschätzte Beschlag-/Griffmassen. Kein in NX bestimmtes Materialgewicht.
Bei 70 % angenommener Kompensation und 1,30 Progression ergibt sich als Vergleich
je Hauptfeder ungefähr F1=125 N, je Zwischenfeder F1=63 N. Am oberen Segment
verbleibt je nach Stellung etwa 81 bis 24 N aufwärts aufzubringende Haltekraft.
**Dies ist weder die erforderliche Bestellkraft noch eine nachgewiesene Bedienkraft.**
Führungreibung, Temperatur, Dichtungsreibung, Verschleiß und Ausfall fehlen.

Die Modellpositionen folgen einem vorgegebenen 2:1-Verhältnis, aber eine tatsächliche
Kette/Seilkopplung oder Verkantungssicherung ist noch nicht konstruiert. Federlaschen,
Gelenke, Befestigungsschrauben, Führungslasten, mechanische Anschläge und die sichere
Fixierung bei Ausfall eines Elements müssen vor Realbau ausgelegt werden.

## Grenzen der Übertragung

Kein sicherheitsgeprüftes Fenster, keine nachgewiesene KSS-Dichtheit, keine berechnete
Rahmensteifigkeit, keine reale Federproduktauswahl. Lichtschranken/Schalter-Symbole
stellen keinen Sicherheitskreis dar. Das Schrankinnere und die Motorhalter bleiben
im bisherigen, ausdrücklich vorläufigen Detaillierungsstand.
