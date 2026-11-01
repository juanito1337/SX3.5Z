# Konzept13 â€“ Entwicklung und Nachweise,01.11.2026

12er Seitenmagazin rechts/hinten und einzelner Hub-/Schwenk-/Zustellarm.
Neue eigene Variante auf erhaltenem Maschinenstand12. Nutzer hat Auswahl
und NX-Umsetzung beauftragt; keine Bestellung oder Maschinenfreigabe.
[CAD-Einstieg](../../../cad/README.md), [Konzept/Anleitung](../../../projekt/Dokumentation/ATC_Konzept13.md).

Quellbasis e8a0029, Geometriecommit dbfd4e1, finale Journalquellen feaf395.
[Matrix](native_matrix.json) dokumentiert native Befehle/Umgebung/Exitcodes;
[weitere Pruefmetadaten](verification.meta.json) die Offline-Pruefungen.
Native Wiederoeffnungsberichte, exakte Quellen-/PRT-Hashes liegen je CAD-Lauf.
Vier finale NX-Laeufe Exit0: beide Stellungen gespeichert und frisch
geoeffnet, je532 Teile/17 Gruppen/24 native Blechteile;6244 Ausdruecke
geprueft. Native Werkzeuglage0/0/530mm mit1e-5mm Toleranz nachgewiesen.
STEP wird direkt aus NX exportiert und getrennt offline eingelesen
(step_readback.json); Offline-Einlesen ist kein nativer NX-Reimport.

201 Tests und99 Untertests bestanden.532 gueltige Einzelkoerper,62
Bewegungsstichproben mit421 ausgefuehrten BRep-Vergleichen ohne ungewollte
Ueberschneidung im definierten Umfang. Baelge, reale Ersatzspindel,
beliebige Werkstuecke und kontinuierliche Bahn nicht nachgewiesen.
Interne Mechanikkontakte nur fuer benannte Paarungen geprueft; kein globales
Nullkollisionsversprechen. Sechs bekannte Maschinenanschluss-Konflikte offen.
Historische Paketidentitaet449/477;28 bereits bekannte Fortschreibungen.
Hilfstests9 bestanden,1 Windows-Symlinktest uebersprungen.

[Reviews und Korrekturen](review.md): Arm-/Saeulenweg, Werkzeugbolzen und
Schneidwerkzeug, Greifer-Oeffnung, Radialantrieb/Schienen, Hubmotor sowie
Magazin/Index/Tropfboden nachgebessert. Wechselraum konservativ125mm ueber
Tisch, nachdem die Arm-Unterkante als tiefster Punkt erkannt wurde.
Testfehler vor Korrektur und finale Protokolle separat erhalten.

Erster NX-Vollaufbau: OSError22 beim erneuten Schreiben der Manifestdatei;
Rohlog und Matrix unter attempt1/. NX-Schreibprobe1000 Wiederholungen
bestand. Ursache nicht reproduziert, keine spekulative Adapteraenderung.
Unvollstaendige native Laeufe und Ausgangsarchiv bleiben lokal im ignorierten
Auditbereich, nicht Teil der CAD-Lieferung. Keine fremden Prozesse beendet.

Plausibilitaetsgrenzen: Armreichweite919,24mm, Zusatzgehaeuse nominal1950x1575mm;
12er Eigenbau statt behauptetem RATTM-Kaufteil. R13-Antriebe/Greifer/Lager
sind unbestaetigte Bauraumreserven. Retention, Orientierung, Endlagenbremse,
Spindel/Spannpaket, reale Anschluesse, Lasten, Fertigungsdetails und volle
Bahn bleiben offen. Bearbeitungswege im Modell erhalten, Wechsel nur bei
freier Bahn. Keine Fertigungs-, Kauf-, Betriebs- oder ATC-Freigabe.
