# Entwicklungsprotokoll 09
Ruling: Auftrag wird ohne zusätzliche Freigabeschleife weiterbearbeitet; alle neuen Auswahlentscheidungen sind Planungsentscheidungen des Bearbeiters.
Ruling: Ein günstiges Magazin ersetzt keine automatische Spindelspannung. Original-SK30 bleibt, BT30-Option getrennt gekennzeichnet.
Ruling: Bestehende Schrank-Herstellerartikel bleiben; keine erfundenen Fremdscharniere als vermeintlicher Lieferumfang.
Ruling: Normteil-Schnittstellen nach Primärquellen; Gewinde und nicht verfügbare Detailkonturen ausdrücklich vereinfacht.
Ruling: Kein unabhängiger Reviewer verfügbar; Abschlussprüfung als Autoren-Selbstprüfung kennzeichnen.

Regression: Historie_07_3 enthält Tests früherer eigener Dateibäume und wird nicht als aktuelle Testsuite gesammelt. Die erhaltenen tests08 prüfen nun explizit cnc_ansichtsmodell08; aktuelle09-Verträge in tests09. Erste volle Sammlung hatte33 Fehler aus alten Dateipfaden/Versionsvertragsannahmen; Rohprotokoll bleibt erhalten.
Geometrie: Zwei getrennte Griffbeine erzeugten beim zweiten Schritt zwei Solids. Test reproduziert. Aufbau auf Bein–Steg–Bein umgeordnet.

Revision contract: legacy sheetmetal integration test now expects09 output prefix; API behaviour assertions unchanged. Archived07 tests are excluded by explicit pytest.ini scope, not claimed as current passes.

Ruling: AliExpress-Seiten nicht vollständig prüfbar. Vier konkrete Artikel-IDs samt historischen Preisindexwerten als Anfragehinweise getrennt dokumentiert; keine technischen Maße oder Einkaufssummen aus Indexdaten abgeleitet.
ATC: Erste 70-mm-Teilung verursachte16 positive Überschneidungen in der Endpunktauswahl. Nach Erweiterung auf94mm und Kürzung des Rückenschutzes: 1.368 Paarprüfungen ohne positive Überschneidung; nur drei vorhandene Kopfkörper, ausgewählter Halter ausgenommen, keine Bahnfreigabe. Fußplatte wächst auf620×100mm.
BOM: Selbstprüfung entdeckte eine falsche 2-mm-Materialangabe für den 4-mm-Magazinträger. Regression erst rot, Namenszuordnung korrigiert, Test grün; CSV und Arbeitsmappe aus derselben Quelle abgeglichen.
Review: Autoren-Selbstprüfung über Verbindungsketten, Quellenstatus, Artikelmengen, Tapergrenze, Native-NX-Einstieg, Teileerhaltung und Berichtskonsistenz. Kein unabhängiger Reviewer oder Siemens-NX-Lauf verfügbar.
Review: Browserprüfung um die bislang nicht explizit ausgelöste Konfliktansicht ergänzt; jetzt alle neun Modi tatsächlich aufgerufen. Formulierung „abgedichtet“ durch „Dichtungsreserve“ ersetzt, da keine Dichtheitsprüfung vorliegt.
Abschluss lokal:112 Tests +91 Unterfälle bestehen.55 Python-Dateien erfüllen Python3.10-Grammatik.13 Dokumentseiten vollständig gerendert und visuell geprüft.78 Arbeitsmappenformeln, keine gespeicherten Excel-Fehlerzellen. Echte Hersteller-STEP-Dateien nicht beschafft.
