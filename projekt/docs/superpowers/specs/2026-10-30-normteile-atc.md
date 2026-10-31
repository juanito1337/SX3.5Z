# Umsetzung 09: Normteile und Werkzeugwechsel-Vorbereitung

## Auftrag und Ausgangspunkt
Die Umsetzung 08 bleibt Grundlage. Mehr reale Normteile mit Gegenanschlüssen im NX-Rezept,
Verkleidung detaillieren, günstige Werkzeugwechseloptionen einschließlich AliExpress recherchieren.
Originalguss und bestehende native NX-API-Korrekturen nicht ändern. Keine Bestell-/Fertigungsfreigabe vortäuschen.

## Ansätze und Entscheidung
1. Nur Magazin zukaufen: günstig, aber kein automatischer Wechsel an manueller SK30/M12-Spindel.
2. Bestehende DIN2080-Spindel automatisieren: Spezial-Spann-/Löse- und Orientierungsentwicklung nötig.
3. BT30-ATC-Spindeleinheit plus einfaches Sechsplatz-Pick-up-Magazin: nachvollziehbare Zielarchitektur,
   aber Austausch-/Kopfadapter, Lastfall und Daten des Anbieters fehlen.
Entscheidung des Bearbeiters: Variante 3 als getrennt markierte Einbaustudie, Originalspindel behalten.
Kein unwiderruflicher Umbau. Keine ausführbare Werkzeugwechselbewegung liefern.
Das Tischmagazin nutzt vorhandene T-Nuten und wird im Modell als Option dargestellt.
Kein behaupteter Original-CAD-Import: verifizierte Schnittstellenmaße und gekennzeichnete Vereinfachungen.

## Umfang der Iteration
Ganter GN425-Griffe mit hinterlegten Blechen und Schrauben, LAPP-M20-Kabeleinführungen mit
Gegenmuttern auf verschraubter neuer Blechplatte, Normschrauben/Scheiben/Muttern,
DIN508-Muttern für eine sechsplätzige Magazin-Grundplatte, Sonderteil-Locator und Spritzschutz.
Geometrie, Artikelliste, Mengen und Bauanleitung werden aus derselben Teileliste abgeglichen.

## Grenzen
AliExpress-Livepreise und Varianten nicht bestätigt. Preisindex kein Liefernachweis.
Keine BT30-Kompatibilitätszusage für DIN2080. Kein M6-Remap und keine reale Aktorfreigabe.
Platzrechnung für sechs Taschen ersetzt weder Kollisionssimulation mit Werkstück noch Spannkraftnachweis.
Türgewichtsausgleich, Sicherheitsfunktionen und sechs Alt-Konflikte bleiben offen.
