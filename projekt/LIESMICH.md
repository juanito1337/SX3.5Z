# SX3.5Z – CNC-Umsetzung 09

**Stand 30.10.2026. Vollständiges NX-Journalprojekt mit Normteildetails und einer ausdrücklich nicht betriebsbereiten Werkzeugmagazin-Option.**

Diese Lieferung erweitert 08. Sie ist kein fertig freigegebener Werkzeugwechsler und keine Bestell-/Fertigungsfreigabe. Die Originalspindel ist weiterhin als SK30/M12 nach DIN 2080 modelliert. Eine passende automatische BT30-Spanneinheit ist NICHT eingebaut. Ein Magazin allein ersetzt sie nicht.

## Sofort ansehen

`Ansicht_3D.html` im Browser öffnen; die Datei funktioniert ohne Internet. Neu sind die Ansichten **Magazin-Option** und **Neue Normteile**. Die vorhandene breite Fronttür fährt weiterhin nach unten. Die 49 bewegten Türteile sind gegenüber 08 unverändert. Vorschauen stammen aus dem berechneten Modell, nicht aus einem Bildgenerator.

## Gesamtes Modell in NX erstellen

1. Das gesamte ZIP in einen **neuen lokalen Ordner** entpacken. Nicht mit älteren Modulen mischen. Die Konfigurationsdateien und Unterordner zusammenlassen.
2. In **NX 2406 → Journal wiedergeben / Play Journal** `NX_CNC_Gesamtansicht.py` ausführen. Eine geöffnete Originalbaugruppe ist für diesen rekonstruktiven Aufbau nicht erforderlich. Benötigt werden die vorhandenen Modellierungs-/Blechfunktionen in der NX-Installation.
3. Optional zuvor `NX_Normteile_ATC_Pruefen.py` starten. Dieses Journal erzeugt nur die **125 zusätzlichen und vier geänderten Körper** als native Einzelteile, nach den allgemeinen Schnittstellen- und Blechvortests.
4. Nach einem vollständig erfolgreichen Gesamtaufbau nennt `HAUPTBAUGRUPPE.txt` im Ausgabeordner die Hauptdatei. Alle Teile, Unterbaugruppen und die Hauptdatei zusammenhalten.

Standardausgabe:

```text
%LOCALAPPDATA%\SX35Z\NX_Output\
SX35Z_CNC_UMSETZUNG_09_<Zeitstempel>_<Kennung>\
  Teile\
  Unterbaugruppen\
  FRAESMASCHINE_CNC_UMBAUSTAND_09_NICHT_FREIGEGEBEN__<Kennung>.prt
  HAUPTBAUGRUPPE.txt
  Einkauf_Modellbindung09.json
  ATC_Schnittstellenstatus09.json
```

Die Versionsmeldungen `Journal-Version: 4.8`, `Blechadapter-Patch: 07.2` und `KSS-Formelpatch: 07.3` bleiben absichtlich erhalten. Der neue Geometriestand lautet `CNC_UMSETZUNG_09`. Diese Bibliotheksstände werden nicht allein für die Anzeige umbenannt.

Hier wurde **kein NX-Lauf dieser Revision** ausgeführt. Deshalb liegen keine erzeugten `.prt`-Dateien bei. Python-/Geometrie-/Browsertests außerhalb von NX sind keine native NX-Abnahme. Fehler stoppen den Aufbau; das Journal behauptet bei einem Abbruch keine vollständige Baugruppe. Bestehende NX-Dateien werden nicht überschrieben.

## Neu im Modell

- Drei Ganter GN 425 Edelstahl-Servicegriffe auf den stationären seitlichen Schürzen und der rückseitigen KSS-Serviceklappe; mit Gegenbohrungen, 2-mm-Hinterlegungen, M6-Schrauben und Scheiben. Keine Änderung an der bewegten Tür. Bogenkontur vereinfacht.
- Zwei LAPP M20-Kabelverschraubungen 53111020 mit Gegenmuttern 53119020 auf einer verschraubten 120 × 160 × 2 mm Wechselplattenstudie am trockenen Schrankboden. Die Öffnung ist eine eigene Konstruktion, keine bestätigte Schneider-Serienöffnung. Kabel, Flächendichtungen, EMV und Gesamtschutzart sind noch offen.
- Ein Sechsplatz-Tischmagazin mit 620 × 100 × 8 mm Grundplatte, 4-mm-Kantträger, eigenem 2-mm-Rückenschutz und sechs eigenen POM-Lokatorentwürfen. Vier DIN 508-12-M10-10 T-Nutsteine mit M10-Schrauben nutzen die vorhandenen T-Nuten. Keine neuen Tischbohrungen im Magazinrezept.
- Sechs BT30-ER20-70 Raumreferenzen nach den belegten Halter-Hauptmaßen. Flansch/Greifdetails sind Annahmen, keine bestätigten Hersteller-CAD-Dateien. Keine automatisierte Klemmung, Orientierung, positive Halterretention oder sichere Wechselbahn.

**Umfang:** 560 Einzelkörper / 20 Gruppen; gegenüber 08 zusätzliche 125 Körper (109 Kaufteilkörper, 15 Fertigungsteile, eine Dichtungsreserve). Vier bestehende eigene Verkleidungskörper sind geändert. Die Gusskörper, Werkzeugspindel und bewegte Fronttür bleiben erhalten.

## Werkzeugwechsler: Grenzen und AliExpress-Recherche

Das dargestellte Magazin untersucht eine günstige, achsangefahrene Lösung. Es belegt **620 × 100 mm auf einem 740 × 180 mm Tisch**. Mit realen Spannmitteln muss deshalb die Zweckmäßigkeit erneut entschieden werden. Ein ausfahrbares Seitenmagazin bleibt eine andere, noch nicht ausgelegte Alternative.

Die 94-mm-Teilung entstand nach erkannten Kollisionen des ersten 70-mm-Entwurfs. Die nominelle Rechnung lässt 16,6 mm Höhenreserve für die ausgewiesene Kombination aus Halter, Werkzeug- und Bolzenreserve. Das gilt nicht für beliebige Werkzeuglängen oder einen anderen Spindelkopf. Modellkoordinaten niemals ungeprüft in LinuxCNC übernehmen.

In `Werkzeugwechsler/AliExpress_Suchtreffer_09.json` und im Tabellenblatt `ATC_Suche` stehen vier konkrete Artikel-Links und historische Preisindexbelege. **Direkte Angebote, Varianten, Lieferfähigkeit und Endpreise konnten nicht bestätigt werden.** Die USD-Indexwerte sind keine belastbaren Komplettpreise und werden nicht in die Einkaufs-Kostensumme übernommen. Die englische `Lieferantenanfrage_ATC_09.txt` fragt Zeichnungen, STEP, Schnittstellen, Spann-/Lösedaten, Orientierung und tatsächlichen Lieferumfang ab.

Vor einer ATC-Bestellung müssen Spindel, Halter, Anzugsbolzen, Greif-/Ablageschnittstelle, Löseeinheit, Druckluft, Stillstand/Orientierung, Sensorik und Verhalten nach Störung zusammen festgelegt werden. Es wird bewusst **kein ausführbares M6-Makro** mit geschätzten Positionen geliefert.

## Dokumente und Daten

- `Bauanleitung/Normteile_und_Werkzeugwechsler_09.pdf` und `.docx`: neue 13-seitige Montage-/Beschaffungsergänzung mit Quellen und Grenzen.
- `Einkauf/Einkauf_und_Aufmass_09.xlsx`: konsolidierte 69 Beschaffungspositionen; 13 neue Norm-/Kaufteilkonfigurationen und acht zusätzliche offene Systempakete, 148 Fertigungspositionen, 560 Modellzuordnungen und 35 fehlende Istaufmaße. Preisfelder bleiben bis zum echten Angebot leer.
- Die 08-Anleitung, 08-Arbeitsmappe und 08-Prüfunterlagen bleiben als Basisstand mit eindeutigem 08-Dateinamen erhalten. Die Antriebsrechnungen befinden sich weiterhin in der 08-Arbeitsmappe; die **aktuelle** Stückliste steht in 09.
- `Einkauf/Kaufteile_09.json` ist der gemeinsame Artikelkatalog. `Quellen/Quellen_09.json` trennt Herstellerbelege und Preisindexhinweise.
- `Detail_Parameter_09.json` ergänzt Entwurfsmaße. Katalogmaße sind gegen unbeabsichtigte Änderungen gesperrt. Änderungen der Anschlussdicken/Nutlage benötigen eine neue Verbindungsauslegung.
- `Projekt09_Berichte.py` erzeugt CSV-/JSON-Berichte ohne NX. Für die eigentliche CAD-Erzeugung ausschließlich das NX-Journal innerhalb von NX verwenden.

## Prüfungen – kein Ersatz für reale Auslegung

Der unabhängige Geometrieaufbau hat 560 gültige einzelne Volumenkörper aus 1.829 Operationen erzeugt. Die neuen Körper wurden im Standardzustand gegen die übrigen Körper untersucht: 62.125 Paar-Vorprüfungen, daraus 293 genaue Schnittprüfungen ohne positive Überschneidung. Das ist keine vollständige Bewegungskollisionsermittlung.

An sechs nominellen Aufnahme-Endpositionen wurden drei vorhandene Kopfkörper gegen die Magazinbauteile geprüft (1.368 Paare, keine positive Überschneidung im ausgewiesenen Teilumfang). Der jeweils aufzunehmende Halter wurde wegen der noch inkompatiblen Spindelschnittstelle ausgenommen. Keine vollständige Werkzeugbahn, Werkstückprüfung oder neue ATC-Spindelkontrolle.

Die **sechs bekannten statischen Maschinen-Anschlusskonflikte aus 08 bleiben offen**. Ebenso offen: echte Anschlussmaße, Lager-/Spindelendenfertigung, Antriebsauslegung, XY-Versorgungsschutz, Z-Absturzschutz, Türfang/Gleichlauf, Stromlauf-/Sicherheitskonzept, Dichtheit und fertigungsfreigegebene Zeichnungen/Abwicklungen.

`Pruefung_09/Pruefbericht_09.json` fasst die aktuellen Nachweise zusammen. TDD-Dateien mit `RED` und `vor_Korrektur` sind bewusst erhaltene Entwicklungsevidenz, keine aktuellen bestandenen Prüfungen. Aktuelle Tests: `python -m pytest` mit der mitgelieferten `pytest.ini` (`tests`, `tests08`, `tests09`). `Historie_07_3` wird als Altarchiv nicht mitgezählt. Die Prüfung ist eine Autoren-Selbstprüfung, keine unabhängige technische Abnahme.

### Optionale Entwicklungswerkzeuge

Für das NX-Journal werden keine Fremdpakete außerhalb der NX-Pythonumgebung benötigt. Die optionalen Prüf-/Berichtsskripte unter `tools` benötigen dagegen je nach Aufgabe pytest, CadQuery/OCP, Playwright/Chromium, python-docx oder artifact_tool. Diese Werkzeuge sind nicht in NX zu installieren. Ein optionaler BREP-Testcache kann über `SX35Z_GEOMETRY_CACHE` angegeben werden; ohne Cache wird unabhängig neu aufgebaut. Die neue Produktdaten-/Modellprüfung wird dadurch nicht deaktiviert.
