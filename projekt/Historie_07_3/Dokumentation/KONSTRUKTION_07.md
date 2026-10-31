# Konstruktion 07 – Änderungen und Nachweisgrenzen

## 1. Auftrag und unveränderte Bereiche

Die breite zweiteilige Senktür ist akzeptiert. Entfernt wird das Fenster im
Schaltschrankbereich; dieser Schrank soll direkt anliegen. Unten wird ein
Späneabgang berücksichtigt. Es wird NICHT eine neue Maschinengeometrie aus einem
Bild generiert. Grundlage ist ausschließlich das vorhandene NX-Modellrezept 06.
Die ursprünglichen Foto-Annahmen und die sechs bekannten Maschinenkonflikte
werden hier weder bestätigt noch verdeckt korrigiert.

## 2. Schrank

Die rechte äußere Blechfläche liegt im Standard bei x=889 mm; die Schrankrückseite
liegt jetzt ebenfalls dort. Die vorherige Kabinettposition lag x=947 mm: reale
Verschiebung im Modell 58 mm. Der alte Parameter 60 mm war auf die nominelle
Einhausungsgrenze bezogen; jetzt bezieht sich `cab_gap` auf die tatsächliche
äußere Blechfläche. Es wird kein Dichtspalt als konstruktive Lüftung benutzt.
Die Trennwand bleibt vollständig geschlossen, auch unter dem Schrank. Lastpfad
über eigene Ausleger und Stützbeine. Keine Aussage über Schutzart, Kabeldichtung,
Türschwenkraum oder erforderliche Schaltschrankkühlung.

## 3. Neuer Späne-/Flüssigkeitsweg

Leitbleche um die Maschineninsel → hinterer Trichter → breiter rechteckiger
Schacht → herausnehmbarer Grobkorb → Feinfilterreserve → Flüssigkeitsstutzen → Tank.

Die seitlichen Leitbleche haben 14 % Querneigung (etwa 7,97°) und im vorderen
Bereich 2,5 % Längsneigung. Die Front wird mit niedrigem Mittelfirst zu beiden
Seiten entwässert; die erhöhte Maschineninsel bleibt Lastträger. 2 mm normale
Plattendicke wird über die geneigte Ebene berücksichtigt. Das bedeutet keine
Zusicherung, dass alle Spanformen ohne Hilfsmittel rutschen.

Der Auslass ist 350 x 60 mm außen; im Schacht verbleiben bei 2 mm Wanddicke
346 x 56 mm. Er liegt standardmäßig y=400..460 mm zwischen Maschineninsel und
hinterem Gestellholm, nicht in der vorderen Senktürkassette.

Korb: 420 x 160 x 70 mm außen, rechnerisch rund 4,41 Liter Innenhülle, aber keine
zulässige Nutzfüllmenge. 50 offene 28 x 3 mm Bodenschlitze (4200 mm² Bruttofläche).
Feinspäne können diese Öffnungen passieren. Ein offener Klemmrahmen für ein noch
zu wählendes Feinfiltergewebe ist vorhanden, keine geschlossene Filterplatte und
kein angeblich bereits wirksamer Feinfilter.

KSS-Stutzen: 50 mm Lichtweite als geometrische Studie, KEIN ermittelter Durchsatz.
Der Tank behält 500 x 400 x 250 mm Außenmaße. Die Lage wurde um 80 mm nach vorn
verschoben, um den unteren hinteren Gestellholm freizuhalten. Rohr/Deckeldurchgang
haben einen geometrischen Spalt; Dichtung und Verbindung sind zu spezifizieren.
Der Pumpenkörper bleibt unveränderter Reservierungsraum, kein ausgewähltes Gerät.

## 4. Herstellung und Wartung

Rücklaufkasten, Spänekorb und Schacht als U-Kantprofil-Vorformen mit separaten
Stirnblechen. Geneigte Zuschnittfelder werden als ebene dünne Platten modelliert.
Die Blechbauteile sind zur gemeinsamen Verschweißung/Abdichtung gedacht; Schweißnähte,
Biegeverfahren, Eckabdichtungen und die benötigten Biegeradien/Reliefs fehlen noch.
Hintere Wartungsklappe abnehmen, Korb in +Y herausziehen. 220 mm Weg wurde an fünf
Stellungen untersucht. Als Planungsreserve 500 mm freie Bedienfläche HINTER der
Maschine berücksichtigen; Raumaufstellung ist noch nicht bekannt. Reinigung nur
bei sicher stillgesetzter Maschine. Schutz gegen unbeabsichtigten Zugang durch den
Späneauslass und gegen Quetschen beim Service bleibt Teil der Schutzkonstruktion.

## 5. Ergebnisse und Grenzen

Die neuen Bleche wurden vor der endgültigen Prüfung mehrfach angepasst: zuerst
trafen sie Frontpfosten/Frontquerholm, Tropfkante und Motorhauben; außerdem traf der
bestehende Tank den unteren hinteren Holm. Die Überlagerungen wurden nicht ignoriert,
sondern als fehlgeschlagene Zwischenprüfung dokumentiert.

Die aktuelle unabhängige OpenCascade-Prüfung umfasst gezeichnete KSS-Teile gegen
den Rest, KSS untereinander und den verschobenen Schrank gegen Gestell/Verkleidung.
Zusätzlich acht Achs-Eckstellungen für formkonstante Maschinenkörper, fünf
Korbauszüge und neun Türstellungen. Das ist kein kontinuierlicher Kollisionsnachweis,
keine NX-Ausführung und kein Nachweis für Biegeradien nach nativer Konvertierung.

Native NX-Builder und Konvertierung stammen aus der Vorgängerrevision. Neu ist
nur die sichere Formel-Freigabe `sqrt` zur normalen Plattendicke und eine lokale
NX-Vorprobe dafür; es wird kein neuer NX-Klassenname erfunden. Der Datenbestand
enthält weiter unbestätigte Kaufteilhüllen/Anschlussstellen.

## 6. Externe Einordnung, nicht als übernommenes Kaufteil

Haas beschreibt einen separaten Spänekorb/Filter im KSS-Rücklauf. Das unterstützt
nur das Trennprinzip. Unser Korb, seine Abmessungen und die offenen Filterdaten
sind Eigenentwurf; kein Haas-Teil wurde ausgewählt oder maßgleich nachgebildet.
Quelle, abgerufen 29.10.2026:
https://www.haascnc.com/productivity/chip-and-coolant-management/chip-strainer.html
