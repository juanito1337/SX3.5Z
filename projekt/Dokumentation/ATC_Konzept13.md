# ATC-Konzept 13: Zwölfplatz-Seitenmagazin mit Einzelarm

Stand: 01.11.2026 · Modell: `CNC_KONZEPT_13_SEITENMAGAZIN`.
Die genaue Quellrevision und Rezept-/Parameter-Hashes stehen in den
[Berichten](../Konzept13/Parameter_Herkunft_13.json). Native Lieferdateien und
deren tatsächlicher Prüfstand werden im [CAD-Einstieg](../../cad/README.md)
geführt. Dieses Dokument behauptet keinen bereits abgeschlossenen NX-Lauf.

Konzept 13 ist der jetzt bearbeitete Ansatz: Ein fest abgestütztes Magazin
mit zwölf Plätzen steht rechts hinter der Maschine. Ein einzelner Greifer
transportiert jeweils einen Werkzeughalter zwischen Magazin und Spindel.
Das gesamte Magazin fährt nicht zum Kopf. Der Nutzer hat die direkte
Umsetzung des plausibelsten Ansatzes beauftragt; acht Plätze wären ausreichend,
zwölf sind bevorzugt. Eine zusätzliche CAD-Zustimmung ist kein Arbeitsschritt.

Der bisherige Stand 12 bleibt mit seinen eigenen Quellen und Lieferdateien
reproduzierbar. Konzept 13 verwendet dessen Grundmaschine und Fangbleche,
ersetzt aber den bisherigen Wechsler samt störender Konsole. Es ist ein neuer
Eigenbauentwurf und keine behauptete Zwölfplatz-Ausführung des RATTM-Kaufteils.
Maschinenverfahrwege und Tischabmessungen werden erhalten. Automatischer
Spindelzug, Werkzeugorientierung und reale BT30-Schnittstelle bleiben offen.

## Aufbau und maßgebende Entwurfsmaße

Alle folgenden neuen Maße sind Konstruktionsannahmen, keine gemessenen
Maschinenanschlüsse und keine bestätigten Herstellerpassungen. Koordinaten
beziehen sich auf das vorhandene Modellkoordinatensystem, nicht auf den Boden.

| Größe | Konzeptwert |
|---|---:|
| Armdrehpunkt X/Y | 850 / −350 mm |
| Vollständige Reichweite bis zur Spindelachse | 919,239 mm |
| Eingezogene Reichweite | 859,239 mm |
| Kurze radiale Zustellung | 60 mm |
| Magazinmitte X/Y | 850 / 789,239 mm |
| Werkzeugteilkreisradius | 220 mm |
| Zahl der Magazinplätze | 12 |
| Abstand benachbarter Werkzeugachsen auf dem Teilkreis | 113,880 mm |
| Übergabeplatz X/Y | 850 / 569,239 mm |
| Niedrige Werkzeug-Bezugsebene | Z = 440 mm |
| Spindelübergabe bei `head_down = 0` | X/Y/Z = 0 / 0 / 530 mm |
| Vertikaler Hub | 90 mm |
| Öffnungsbewegung pro Greiferbacke | 22 mm, zusammen 44 mm |
| Angenommene Anzugsbolzenhöhe | 28 mm |
| Zusätzliche Fräserprojektion unter dem Halter | 35 mm |

Die normale Parkansicht übernimmt die Ausgangs-Kopfstellung; deren
Spindelfläche muss deshalb nicht bei Z = 530 mm liegen. Erst die definierte
Wechselstellung setzt den Kopf auf die obere Modellstellung. `park` zeigt
den ausgewählten Halter in der Tasche und den leeren, offenen Greifer 60 mm
zurückgezogen. `magazin` zeigt den geschlossenen Greifer am Übergabeplatz.
`wechsel` zeigt den getragenen Halter an der nominellen Spindelachse.

Der Zusatzrahmen wird am Untergestell abgestützt. Hubmast, zwei vertikal
getrennte Drehlager und Hubplatte tragen den Arm; der Magazinständer steht
auf einem eigenen Querträger. Diese Anordnung beschreibt den Kraftfluss,
ersetzt jedoch keine Schrauben-, Lager-, Schweißnaht- und Anschlussauslegung.
Der Schaltschrank wird mit seinen Trägern um 300 mm nach rechts versetzt.

## Platzbedarf und nutzbarer Wechselraum

Die rechte Einhausungsgrenze liegt nominal bei X = 1187 mm, die hintere bei
Y = 1100 mm. Mit der erhaltenen linken Grenze X = −763 mm und Front
Y = −475 mm entsteht ein umschließendes Hauptrechteck von **1950 × 1575 mm**.
Der eigentliche Zusatzraum ist L-förmig: 300 mm weiter rechts und 575 mm
weiter hinten als die bisherige Einhausung. Blechdicken, Kanten und der weiter
außen stehende Schaltschrank vergrößern das reale Gesamtaußenmaß. Auch
Servicezugang und Tür-/Schranköffnung benötigen zusätzliche Fläche.

Die Vorprüfung verwendet für den vollständig verfahrenen Tisch eine
XY-Hülle von **X = ±620 mm und Y = ±190 mm**. Das ergibt sich aus
740 × 180 mm Tischgröße und 500/200 mm X/Y-Verfahrweg. Die Parkmechanik liegt
in der vorläufigen Layoutbetrachtung außerhalb dieser Tischhülle. Das ist
keine abschließende Kollisionsprüfung aller Maschinenkörper, Bauteile und
Schlauchbewegungen. Ein beliebig großes Werkstück ist damit nicht abgedeckt.

Für den niedrigen Werkzeugtransport gilt im betrachteten Bahnraum eine
**maximale Höhe von 140 mm über dem Tisch**, einschließlich Spannmitteln:
440 − 70 − 35 − 180 − 15 = 140 mm. Dabei stehen 70 mm für Halterprojektion,
35 mm für das angenommene Schneidwerkzeug, 180 mm für Tisch-Z und 15 mm für
die angesetzte Reserve. Längere Werkzeuge verringern diese Grenze direkt.
Sie gilt entlang der gesamten Werkzeugbahn und ersetzt keine Prüfung des
breiteren Greifers, Arms oder anderer Hindernisse. Oberhalb dieses Raums
ist ein automatischer Wechsel im vorliegenden Ablauf nicht vorgesehen.

## Werkzeugwechsel als Funktionsfolge

Der Ablauf ist bewusst langsam und sequenziell. Er ist keine ausführbare
LinuxCNC-M6-Datei. Die [Bewegungsfolge](../Konzept13/Bewegungsfolge_13.json)
führt die Bedingungen und Modellstellungen maschinenlesbar zusammen.

1. Bearbeitung und KSS stoppen, freien Wechselraum herstellen, Kopf in
   Wechselhöhe bringen und Spindel passend orientieren.
2. Leeren Arm niedrig und radial eingezogen zur Spindelseite schwenken.
   Nur am Endpunkt zustellen und anheben. Halter formschlüssig greifen.
3. Erst nach bestätigtem Greifen Spindel lösen und den Halter axial absenken.
   Radial einziehen und niedrig zum Magazin schwenken.
4. Einen leeren Magazinplatz indexieren und verriegeln. Zustellen,
   Taschenaufnahme sichern und erst danach den Greifer öffnen.
5. Nach zurückgezogenem Greifer den gewünschten neuen Platz indexieren.
   Neuen Halter greifen; Taschenretention erst nach bestätigtem Halt lösen.
6. Radial einziehen, niedrig zur Spindel schwenken, am Endpunkt zustellen
   und axial anheben. Spindel spannen und Spannzustand bestätigen.
7. Erst danach Greifer öffnen, radial abziehen, absenken und leer parken.
   Bearbeitung erst nach bestätigter Parklage und freier Maschinenhülle.

Der Modellparameter `a13_tool_carried` bedeutet **0 = in der ausgewählten
Tasche, 1 = getragen, 2 = in der Spindel**. Der Name ist historisch kurz;
der Wert ist ein Zustand, kein einfacher Ja/Nein-Schalter. Der aktuelle
Rezeptstand bildet den Transferhalter und zwölf Taschen ab. Eine vollständige
Belegungsverwaltung, alle Indexstellungen und die Fehlerbehandlung sind
noch keine ausgelegte Steuerung.

## Greifer, Werkzeugorientierung und Kaufteilgrenzen

Greifergehäuse und Backen sind eigener Konzeptentwurf. Die Federklemmung ist
eine **CUSTOM-Reserve**, kein maßhaltiges Hersteller-CAD. Die modellierte
Flanschnut und die Haltekontakte müssen an einem bestätigten Halter überprüft
werden. Eine positive Verdrehsicherung in den Backen und eine definierte
Winkellage in jeder Tasche sind erforderlich und noch nicht vollständig
auskonstruiert. Auch die Taschenriegel sind bisher Funktionsreserven.

Zwischen Magazin- und Spindelseite dreht sich der Arm nominal um **67,620°**.
Ein fest gehaltener Halter dreht sich entsprechend um seine Werkzeugachse.
Spindelorientierung, Mitnehmernuten und Taschenindexierung müssen dazu
gemeinsam passen. Runde Raumhüllen allein beweisen diese Orientierung nicht.
Der vorhandene SK30/DIN2080/M12-Spindelstand wird nicht zu BT30 umbenannt.
BT30-Spindel beziehungsweise geeigneter Umbau und automatisches Spannpaket
sind noch auszuwählen und zu belegen.

Als Kaufkandidaten für die weitere Greiferuntersuchung existieren:

- **SMC MHL2-16D1Z**: Der Herstellerkatalog nennt 60 mm gesamten Öffnungsweg
  und 725 g Eigenmasse. Damit ist ein realer Kandidat mit größerem Weg als
  den angesetzten 44 mm bekannt; Backengeometrie, Haltekräfte, Anschlüsse und
  Verhalten bei Druckverlust sind damit nicht passend nachgewiesen.
  [SMC MHL2, Katalog CAT.EUS20-249B-UK, Tabelle auf Seite 4](https://static.smc.eu/pdf/MHL2-B_EU.pdf).
- **SCHUNK PHL**: Langhub-Parallelgreiferfamilie mit optionaler mechanischer
  Greifkrafterhaltung. Eine konkrete Baugröße und Ausführung ist nicht
  ausgewählt. [Herstellerbeschreibung PHL](https://schunk.com/us/en/gripping-systems/parallel-gripper/phl/c/PGR_6331).

Diese Quellen wurden am 01.11.2026 gelesen. Sie begründen Kandidaten,
keine Bestellung oder Einbaufreigabe. Das Modell wurde nicht stillschweigend
auf einen dieser Hersteller umetikettiert. Die zwölf Halter verwenden die
vorhandene Katalogreferenz **K09-BT30ER20, Wondersunm BT30-ER20-70, S09-10**.
Die alte Katalogmenge acht ist historisch; der Bericht 13 leitet zwölf aus
dem Rezept ab. Flansch-/Nutdetails, 28-mm-Anzugsbolzen und Schneidwerkzeug
bleiben gesonderte Entwurfsannahmen.

## Herstellbarkeit und erste Armabschätzung

Vorgesehen ist ein Stahl-Kastenprofil mit 80 mm Höhe, 40 mm Breite und
4 mm Wandstärke. Die nominelle Profillänge ab Drehpunkt bis zum Armende
beträgt 919,239 − 110 = **809,239 mm**. Nabe, Lagerbohrung, Führungsauflage
und Anschlüsse müssen geschweißt beziehungsweise mechanisch verbunden und
anschließend passend bearbeitet werden. Die aktuelle CSG-Geometrie des Arms
ist noch kein fertiger Zuschnitt- oder Schweißplan.

Eine überschlägige Euler-Bernoulli-Rechnung verwendet einen ideal fest
eingespannten, gleichförmigen Kragträger, E = 210000 N/mm² und Stahl mit
ρ = 7850 kg/m³. Für senkrechte Biegung:

`I = [40·80³ − 32·72³]/12 = 711338,667 mm⁴`

Bei einer angenommenen Kraft F = 50 N am Ende dieses **809,239-mm-Profils**
ergibt `δF = F·L³/(3·E·I) = 0,0591 mm`. Die Querschnittsfläche ist 896 mm²,
die rechnerische Profilmasse 5,692 kg. Mit g = 9,81 m/s² beträgt die
Eigengewichtslast q = 0,0690 N/mm und deren Durchbiegung
`δq = q·L⁴/(8·E·I) = 0,0248 mm`; zusammen etwa **0,0839 mm**.

Die 50 N sind ein Rechenansatz, keine bestätigte Nutzlast. Die Werkzeugachse
liegt bei vollständiger Zustellung weiter außen, bei 919,239 mm. Ihre echte
Belastung muss einschließlich dieses Hebelarms neu berechnet werden.
Lagerspiel, Hubführung, Schweißnähte, offene Profilstellen, Radialschlitten,
Greifergewicht, Torsion und Dynamik sind in obigen Zahlen nicht enthalten.
Dies ist ausdrücklich **kein Festigkeits-, Steifigkeits- oder Freigabenachweis**.

Feste Schwenk-Endlagen, lasttragende Verriegelungen und geeignete Haltebremsen
sind weiterhin auszulegen. Unabgestützte Anschlagdarstellungen wurden
entfernt; daraus folgt keine bereits vorhandene Endlagenarretierung.
Federklemmung und Lösebetätigung sind ebenfalls noch nicht ausgewählt.

## Berichte, Fertigung und noch offene Arbeit

Der [Berichtsexporter](../tools/atc13_berichte.py) erzeugt ausschließlich einen
neuen Berichtsordner. Standardziel ist `projekt/Konzept13/`. Er überschreibt
keine vorhandenen Berichte; für einen neuen Stand ist `--output-dir` mit
einem neuen Verzeichnis zu verwenden.

```powershell
.venv/Scripts/python.exe projekt/tools/atc13_berichte.py
```

- [Stückliste 13](../Konzept13/Stueckliste_13.csv): alle Modellteile nach
  Artikelkennung, getrennt nach Bestand, MAKE, BUY und RESERVE.
- [Katalogbindung 13](../Konzept13/Kaufteile_13.json): Artikel, Quellen und
  tatsächliche Mengen. Eine Kaufbaugruppe kann mehrere Modellkörper haben;
  die Menge zählt die eindeutigen Kauf-/Bauinstanzen.
- [Parameterherkunft 13](../Konzept13/Parameter_Herkunft_13.json): Eingabewerte,
  Herkunft, Status sowie abgeleitete Formeln und deren Werte.
- [Bewegungsfolge 13](../Konzept13/Bewegungsfolge_13.json): Stellungen,
  Zustände und erforderliche Übergabebedingungen, ohne Maschinenbefehle.

Alle R13-Artikel sind `UNSELECTED`. MAKE bezeichnet einen Fertigungsentwurf,
keine freigegebene Fertigungszeichnung. Bestätigte Herstellerdaten, Istmaße
und vereinfachte Geometrie bleiben unterscheidbar. Es werden keine
Fertigungs-, Bestell-, Maschinenbetriebs- oder ATC-Freigaben gesetzt.

Noch erforderlich sind insbesondere Istanschlussmaße am Untergestell,
Schraub- und Schweißdetails, vollständiger Last-/Antriebsnachweis, passender
Greifer samt Retention und Verdrehsicherung, Spindel-/Spannpaketentscheidung,
Sensorik und Störungsablauf sowie Hersteller-CAD beziehungsweise bestätigte
Zeichnungen. Servicefugen/-türen, sichere Reinigung und Ablauf des neuen
Tropfbodens sind zu detaillieren. Die bestehenden sechs Maschinenanschluss-
Konflikte werden durch diese Erweiterung nicht als erledigt behandelt.

Die sieben neuen gefalteten Wand-/Dachprofile sind für native
Pflichtblechkonvertierung vorgesehen. Der flache Magazinspritzschutz und
Tropfboden sind separate Blechgeometrien; eine flache Vorform ist keine
behauptete native Blechkonvertierung. Abwicklungen, Zeichnungen,
Fertigungstoleranzen und Montageanleitung für den realen Bau fehlen noch.
Die maschinenlesbaren Offline-Berichte sind kein Ersatz für den gesonderten
nativen Aufbau, frisches Wiederöffnen und die spätere geometrische Abnahme.
