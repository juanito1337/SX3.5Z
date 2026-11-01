# Belegfortschreibung RATTM,01.11.2026

Ausgangsrevision:2b83f2c. Gepruefter Aenderungsstand: die mit diesem Protokoll
versionierte Bild-/Katalogfortschreibung; keine Aenderung am Modellcode oder an
Geometrieparametern. Umgebung Windows10Build19045, separate Projekt-.venv,
CPython3.12.14. Keine Aenderung an NX oder globalen Installationen.

| Pruefung | Befehl / Arbeitsverzeichnis | Ergebnis | Rohprotokoll |
|---|---|---|---|
| Katalogexport |`.venv/Scripts/python.exe ergebnisse/entwicklung/20261101_rattm_bildmasse/arbeitskopie/projekt/Projekt09_Berichte.py`, Paketstamm|Exit0;70 Katalogzeilen,454 Modellkoerper; nur Einkaufsliste11 und Kataloghash des Abgleichs in aktiven Stand uebernommen|[export.log](export.log)|
| Beleg-/Konsistenzpruefung |`.venv/Scripts/python.exe ergebnisse/entwicklung/20261101_rattm_bildmasse/verify_evidence.py`, Paketstamm|Exit0;6 bytegleiche Bildkopien,21 Beschriftungen,1Wechslerpaket; Modellcode/Parameter/Rezept unveraendert|[verification.log](verification.log),[Metadaten](verification.json)|
| Bestehende Offline-Suite |`../.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider`, projekt/|Exit0;173 Tests und99 Untertests bestanden|[pytest.log](pytest.log)|
| Patchformat |`git -c core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol diff --check`, Paketstamm|Exit0; vorhandene CRLF-Zeilenenden der Exporte zugelassen|[diff_check.log](diff_check.log)|

Der Berichtsexport wurde ausschliesslich in einer Arbeitskopie ausgefuehrt.
Das neue Einkaufsblatt aendert genau die PositionO10-TELLER. Das neue Abgleich-
JSON aendert nur `catalog_sha256`; Rezept-/Parameterhash und alle Mengen bleiben
gleich. Die Original-Screenshots sind perSHA256 gegen ihre Quellen aufW:
verglichen. SHA256 prueft Byteidentitaet, nicht die technische Richtigkeit der
Lieferantenangaben. Die Pruefung kennzeichnet nicht bestaetigte Masse weiterhin
als solche. Ausfuehrungsskript und Ausgangshashes sind beigefuegt.

Frischer unabhaengiger Review: `/root/review_rattm_evidence`,gpt-6-astra,
01.11.2026. Alle sechs Bilder visuell geprueft; keine inhaltlichenP1/P2-Befunde.
Kleine Abschlussnotiz: Link auf dieses Pruefprotokoll war waehrend des Reviews
noch nicht aufloesbar; durch diese Datei ergaenzt und anschliessend geprueft.

Bewusst nicht beurteilt: reale Passung, Gussanschluss/Tragfaehigkeit,
Betriebsorientierung, effektiver Magazinweg, Spindelspannung und ATC-Betrieb.
**Kein neuer nativer NX-Lauf in diesem Paket.** Die vorhandenen nativen
Lieferstaende und ihre Nachweise bleiben unveraendert. Kein Hardwareaufruf.

Arbeitsweise: Quellen/Katalog/Dokumentation im bestehenden Git-Ordner auf
`codex/rattm-bildmasse` bearbeitet; Ausgangsarchiv lokal gesichert. Fuer diese
reine Datenfortschreibung keine neue Implementierungs-Testdatei angelegt.
Die weitere konstruktive Integration ist im Plan getrennt als offen gefuehrt.
