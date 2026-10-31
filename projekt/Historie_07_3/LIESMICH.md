# Korrekturstand 07.3 – zuerst lesen

Der KSS-Formelpatch 07.3 behebt den Einheitenkonflikt am linken/rechten/vorderen/
hinteren KSS-Trichter. Geometrie und Maße bleiben auf Stand 07. Der nachweislich
im Nutzerlauf funktionierende Blechadapter **07.2 bleibt unverändert**.

**Zuerst `NX_KSS_Pruefen.py`, nach vollständigem Erfolg
`NX_CNC_Gesamtansicht.py` innerhalb von NX starten.**

Einbau, Versionszeilen, Prüfgrenzen und neuer Ausgabeordner:
**[LIESMICH_FIX_07_3.md](LIESMICH_FIX_07_3.md)**.
Kein automatisches Fortsetzen alter Teilläufe; vorhandene Dateien bleiben erhalten.
Keine hier erzeugten PRTs und kein eigener NX-Lauf des neuen Patches.

Die Anleitungen 07.1/07.2 sind historische Dokumentation. Maßgeblich ist 07.3.

---

## Unveränderte fachliche Dokumentation des Geometriestands 07

Die nachfolgenden Ausgabenamen mit `_07_` sind historisch. Aktuell gilt
`SX35Z_CNC_ANSICHT_07_3_<Zeitstempel>_<Kennung>` gemäß obiger Anleitung.

# SX3.5Z CNC – Gesamtansicht 07
## Geschlossene Schrankseite, direkt anliegender Schaltschrank, Späne-/KSS-Rücklauf

Vollständiges Paket für **Siemens NX 2406 / NX Open Python 3.10**.
Der native Ablauf wurde hier NICHT in Siemens NX ausgeführt. Keine fertigen PRTs
im Paket. Vorhandene Originaldateien werden nicht überschrieben.

## Änderungen gegenüber 06

- Rechte Seitenscheibe hinter dem Schrank entfällt; der Ausschnitt im Kantblech ist
  geschlossen. Linkes Seitenfenster und beide Türscheiben bleiben erhalten.
- Schrankrückseite liegt nominell direkt an der äußeren Seitenwand. `cab_gap=0`.
  Eigene Ausleger und Stützbeine bleiben als Lastpfad erhalten. Die Schranktür ist
  weiterhin ein geschlossenes Blech und öffnet zur Außenseite. Dichtung, Kabelwege
  und Wärmemanagement sind noch nicht fertig konstruiert.
- Neue 2-mm-Leitbleche um die unveränderte Maschineninsel, hinterer Trichter,
  350 x 60 mm Späneschacht (Außenmaß, nominal 346 x 56 mm frei), entnehmbarer
  420 x 160 x 70 mm Grobkorb und eigener Rücklaufkasten vor dem KSS-Tank.
- Korb: 50 tatsächlich modellierte 28 x 3 mm Schlitze. Das ist ein GROBSIEB,
  kein Feinfilter. Für einen Feinfilter ist nur ein offener Halterahmen vorhanden.
- Korbentnahme NACH HINTEN, nach Abnehmen der rückseitigen Serviceklappe.
  220 mm Auszugsweg untersucht; etwa 500 mm Servicefreiraum als Planungsannahme.
- Tank gegenüber 06 um 80 mm nach vorn versetzt, damit er nicht den unteren
  hinteren Rahmenholm durchdringt. Außenmaße/Volumenhülle unverändert.
- Tür, Türhub, Federstudien, Maschinenbauteile und CNC-Antriebe bleiben unverändert.
  Nur die stationäre vordere Tropfkante ist für die neue Wanne um 7 mm gekürzt.

## Gesamtes Modell in NX erzeugen

1. ZIP vollständig in einen **neuen lokalen Ordner** entpacken, z.B.
   `C:\NX_Projekte\SX35Z_Gesamtansicht_07`. Keine Module aus älteren Paketen beimischen.
2. In NX: **Journal wiedergeben / Play Journal → `NX_CNC_Gesamtansicht.py`**.
3. Das Journal prüft Ausdrucks-/Feature-/Speicherfunktionen, eine geneigte
   Blechvorform und die Blechkonvertierung, dann baut es die gesamte Maschine.
4. Nach vollständigem Erfolg nennt `HAUPTBAUGRUPPE.txt` die Hauptdatei.
   **Den gesamten Ausgabeordner mit Teilen und Unterbaugruppen zusammenhalten.**

Standardausgabe:

```text
%LOCALAPPDATA%\SX35Z\NX_Output\
  SX35Z_CNC_ANSICHT_07_<Zeitstempel>_<Kennung>\
    Teile\
    Unterbaugruppen\
    FRAESMASCHINE_CNC_BLECHENTWURF_07__<Kennung>.prt
    HAUPTBAUGRUPPE.txt
    Erzeugte_Teile.json
    Blech_Nachweis.json
    Spaene_KSS_Entwurfsdaten.json
```

`Geometriestand: CNC_ANSICHT_07`; der wiederverwendete Grundadapter heißt separat 4.8.
`NX_Ausgabe.json` erlaubt einen anderen absoluten Ausgabeordner. NX braucht weder
CadQuery noch den Browser noch einen zuvor ausgeführten Bestandsaudit für diesen Aufbau.

## Blechteile

`Blech_Optionen.json` bleibt auf `"mode": "required"`. 19 U-/Kantprofile sind zur
nativen NX-Blechkonvertierung vorgesehen. Geneigte ebene Zuschnittplatten werden
als separate konstante 2-mm-Volumenkörper aufgebaut. Ihre NORMALE Dicke bleibt
2 mm, nicht lediglich ihre vertikale Ausdehnung. Die Formel verwendet `sqrt`;
diese Formel wird zuerst an einer echten NX-Testvorform versucht.

Keine neuen NX-Featuretypen gegenüber 06. Die Blechbindung/Lizenz und der neue
Gesamtlauf sind hier trotzdem nicht in NX getestet. Fehler werden nicht übersprungen.
Explizit gewählter Modus `"solid"` erzeugt nur parametrische scharfkantige Vorformen,
keine bestätigten NX-Blechkörper. Keine geprüften Abwicklungen enthalten.

## Ansehen ohne NX

`Ansicht_3D.html` lokal im Browser öffnen. **Späne/KSS (Schnittansicht)** blendet
Maschine, Verkleidung, hintere Serviceklappe und Tankdeckel zur Betrachtung aus.
Diese ausgeblendeten Teile fehlen NICHT in der erzeugten Baugruppe.
Die Tür kann im Browser weiterhin nach unten bewegt werden.

## Parameter

`Ausbau_Parameter.json`: `cab_gap`, `chip_outlet_w`, `chip_outlet_d`, `chip_outlet_y`
und wie bisher `door_open` (0 geschlossen, 1 abgesenkt). Nach Änderungen neu
aufbauen. Kein Rückimport manueller PRT-Änderungen. Alle Maße sind Millimeter.
Ungültige Schachtlage/Abmessungen werden vor dem Aufbau zurückgewiesen.

## Grenzen

Das ist ein Anschauungs-/Konstruktionsentwurf. Kein automatischer Späneförderer:
lange oder verklemmte Späne können manuelle Reinigung benötigen. Feinfilter,
Schweißnähte, Dichtungen, Verstopfung/Überlauf und KSS-Durchsatz sind nicht ausgelegt.
Der Schrank hat keine zur Nassraumseite offene Lüftung; die Wärmelast bleibt zu prüfen.
Frühere sechs Maschinen-Anschlusskonflikte bleiben bestehen. Keine Fertigungs-,
Bestell-, Sicherheits- oder Inbetriebnahmefreigabe.

Bei Abbruch: neues `NX_Fehlerprotokoll.txt`, ggf. `NX_Geometriediagnose.json` sichern.
Einzelteil-Zwischenstände sind keine erfolgreiche Gesamtbaugruppe.
