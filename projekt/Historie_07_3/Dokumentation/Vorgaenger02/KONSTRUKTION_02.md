# Konstruktionsstand 02: Anschlüsse, CNC-Zelle und Elektrik

## Befestigungskonzept
Motor → vier eigene Flanschschrauben (X/Y M4 durch Katalogdurchgang Ø5 in entworfene M4-Plattengewinde; Z M5 bleibt Entwurf) → Motorplatte → vier verschraubte Distanzsäulen → Maschinenadapter. Die Flanschschraubenköpfe liegen hinter dem Motorflansch; die grobe Motorhülle besitzt nur schematische Zugangsfreistellungen. Das ist keine Bearbeitungsanweisung am Kaufmotor. Original-Katalogdurchgänge bleiben erhalten. Die Säulenschrauben sind eine andere Verbindung als das Motorlochbild.

Das Festlagergehäuse erhält einen Sitz mit hinterer Schulter, zwei Ringhüllen, einen eigenen vorderen Deckel und vier durchgehende Gehäuse-/Deckelschrauben in der Adapterplatte. Wellenabsatz und Sicherungsmutterhülle zeigen den axialen Haltepfad. Die Lagerbelastung muss über Gehäuse/Adapter in den Maschinenguss, nicht über den Motor oder eine Axialklemmung in der Kupplung gehen. Lagerpaarung, Passungen, axialer Anstellweg, Dichtungen, Schmierung und Muttergewinde sind offen. Die Modelle sind keine normgerechten BK/BF-Kaufteilmodelle.

Die Gegenlager erhalten separate Anschlussbrücken und vier Schrauben. Für X ist die Brücke verlängert. Für Z liegt eine zusätzliche Lastbrücke auf dem modellierten Säulenguss, nicht allein auf dem dünnen Elektrikdeckblech. Das dortige Deckblech muss im realen Aufbau angepasst werden; dessen aktuelle Überschneidungen werden nicht versteckt.

Die vier nominalen M6-Anschlüsse der Maschinenadapter sind Entwurfspositionen. Keine Freigabe für Bohren in die Originalmaschine. Die originalen Stirnflächen, Bohrbilder und freien Wandstärken sind vor Detailfertigung zu messen. Lange Abstandssäulen erlauben Einblick/Montage; eine steifere Kastenhalterung kann nach Einpassung vorzuziehen sein.

## Vollständiger Wegfall des Handbetriebs
X-/Y-Handräder und ursprünglicher Z-Hubmotor waren bereits entfallen. Jetzt sind auch Dreisternhebel, Kurzhebel, Feinvorschub und die innere manuelle Pinolen-Vorschubwelle/Ritzelhülle entfernt. Eine Deckelstudie schließt den Hebelanschluss. Die Pinole und Werkzeugspindel bleiben. Kein Betrieb ohne nachgewiesene Pinolenklemmung; die Klemmlösung selbst wird dadurch nicht als geprüft dargestellt.

## Längen und Zielhübe
Nominale Studienhübe X500/Y200/Z240 mm. In Ansicht01 fehlten bei X am Ende +250 mm 20 mm geometrische Überdeckung der Mutter-/Blockhülle; zusätzlich waren 10 mm Reserve verlangt. Bei Z blieben am unteren Zielpunkt nur 3,25 mm. In K02 wurden X um40 und Z um20 mm verlängert. Mindestreste sind nun X20/Y25/Z23,25 mm. Die Modell-Gesamthüllen lauten X841/Y413/Z563 mm, davon zylindrischer Kern X776/Y348/Z498 mm. **Keines dieser Maße ist eine fertige bestellbare Kugelspindel-Spezifikation.** Gewindeausläufe, Standard-Endenbearbeitung und Lage der realen Lager müssen separat ausgelegt werden.

Die Hüllraumprüfung gegenüber der Zellenaußenhülle umfasst nur formkonstante translatorische Teile an acht Eckkombinationen. Zwei veränderliche Faltenbälge werden nicht geprüft. Sie umfasst keine Guss-Kollisionen, Werkzeuge, Werkstücke, Kabel oder dynamische Bremswege. Die sechs bekannten statischen Anschlusskonflikte sind weiterhin dokumentiert.

## Untergestell / Arbeitshöhe
Entwurf:1850×1200 mm Grundrahmen, nominell60×60×3-mm-Vierkantrohre, Maschinengrundfläche750 mm über Boden. Mit180 mm Modellhöhe bis zur Tischoberfläche ergibt sich930 mm Arbeitshöhe. 20-mm-Tragplatte auf zwei Traversen. Schrank zusätzlich außen abgestützt; Gesamtbreite mit Schrank etwa2213 mm, ohne Türschwenk-/Wartungsraum. Keine Statik, Schweißfolge, Schwingungs-/Kipp- oder Bodenankerauslegung. Dargestelltes Rohrmaß ist keine geprüfte Tragfähigkeitszusage.

## Einhausung / KSS
Geschlossene Dach-/Rück-/Seitenhülle, zwei frontseitige Türrahmen mit Sichtfeldern, Überdeckung am Mittelstoß und Rücktropfkante. Einhausung1250 mm über Maschinenstandebene, damit etwa2000 mm ab Boden. 2-mm-Blech und8-mm-Fenster sind Darstellungs-/Entwurfsmaße. Fenster müssen nach Schutzfunktion, Rückhaltevermögen, Einspannung und KSS-Beständigkeit ausgewählt werden; nicht einfach beliebiges Acrylglas bestellen.

Wanne mit geneigten Außenfeldern, erhöhter Maschineninsel samt vorgesehenen Innenaufkantungen, geschlossen zu schweißenden Außenrändern und50-mm-Ablauf. Tank500×400×250 mm:50 Liter geometrisches Außenvolumen, NICHT nutzbares Betriebsvolumen. Herausnehmbarer Filterkorb und Pumpenbauraum; Pumpenleistung/Filtergröße/Schlauchdurchmesser nicht ausgelegt. Türen/Durchführungen benötigen spritzdichte Überlappungen/Dichtungen. Sichtmodell garantiert weder Dichtheit noch Schutz vor Aerosolen; Rückhalte-/Spritzprüfung und ggf. Absaugung gehören zum weiteren Entwurf. Dichtungen, Scharniere und funktionsgeprüfte Türzuhaltung nicht vollständig modelliert.

## Elektrische Architektur – noch kein Verdrahtungsplan
LinuxCNC-PC → Ethernet → Mesa7i95T → differenzielle Step/Dir-Signale → je Achse passender Treiber → Motor.
Motorencoder des Closed-Loop-Schrittmotors gehört primär an dessen Treiber. Treiber-Störmeldung/Ready an Steuerung über passende Signalpegel; optionale weitere Rückmeldung nur nach Schaltungsprüfung.

Die Mesa liefert keine Motorleistung. Sie benötigt eine separate geregelte5-V-Versorgung. Feldsignale/Bremsansteuerung sind gesondert auszulegen;24 V nicht an die5-V-Einspeisung legen. Für aktuelle XY-Schrittmotorreferenzen sind2×CS-D508 vorgesehen (Hersteller-Umriss116×69,2×26,5 mm). Der modellierte48-V-Versorgungsplatz ist nur eine Planungsebene: Versorgungstoleranz und Rückspeisespitzen müssen unter der Treibergrenze bleiben; keine freigegebene Leistungs-/Spannungsauslegung.

Für echte AC-Servos werden passende Motor-/Servoverstärkerpaare und Encoder-/Bremskabel benötigt, z.B. eine Step/Dir-fähige Servo-Familie. Ein EL7-RS400P ist als reale Beispielreferenz recherchiert (400 W,220 VAC einphasig, Pulse+Direction), aber hier NICHT als ausgewählter Kaufteil- oder Sicherheitsantrieb integriert. EtherCAT ist nicht allein deshalb passend, weil die Mesa eine Ethernet-Buchse hat. Ein allgemeiner Frequenzumrichter ersetzt nicht den achsspezifischen Positionierantrieb. Die originale bürstenlose Spindel bleibt mit Originalregler; keine ungeprüfte FU-Substitution.

## Schaltschranklayout
Separater trockener Bereich außen rechts, Entwurfsgehäuse600(B)×800(H)×300(T) mm. Motorleistung links, Steuer-/Feldbereiche rechts, Montageplatte, DIN-Träger und Kabelkanäle. Die CS-D508-Hüllen sind Herstellerabmessungen; Mesa220×140×30 mm, Z-Treiber, Netzteile, Schütze, Filter und Sicherheitsgerät sind ausdrücklich unbestätigte Bauräume. Keine vollständige Verdrahtung, Klemmenbelegung, Kurzschluss-/EMV-/Wärme-/Lüftungsbemessung. Altelektrik des Spindelantriebs bleibt im originalen Säulengehäuse. Netzanschluss, Schutzleiter aller Metallteile, Not-Halt, Türüberwachung/Nachlauf, Z-Absturzschutz und Bremsfolge sind fachlich auszulegen. Keine Funktion allein durch LinuxCNC als sicher behauptet.

## Priorität für die nächsten realen Messungen
Tisch-/Basis-/Säulenlochbilder, Mutternräume und Wellenachsen; geforderte Hübe und Führungskontakt; Kopfmasse; belastbare Motor-/Treiberentscheidung; Pinolenklemmung. Danach konkrete Lager-/Kupplungs-/Endenbearbeitung und steife Halter konstruieren. Keine Bestellung der Spindeln nach reinen Ansichtshüllen.
