# Priorisierte Fortsetzung

## Vorrang nach RATTM-Auswahl und Bildlieferung01.11.2026

1. BT30 ist vom Nutzer bestaetigt. Lieferantenzeichnung der BT30-Ausfuehrung
   zuordnen und reale SK30/BT30-Spindelschnittstelle pruefen.
2. Greiferteilkreis, aeussere Huellen, Schlitten-/Tellerbezuege, effektiven Hub
   und Betriebsorientierung belegen. Scheibe280mm ist kein Werkzeugteilkreis.
3. Direkte rechte Saeulenkonsole als Bearbeitervorschlag pruefen; Lasten und
   Istanschlussflaeche bestimmen. Keine Gussbohrungen nach Fotoannahme.
4. Produktmodell und Park-/Wechselweg neu erstellen und nativ pruefen. Die
   alten389,33mm sind kein Sollhub des ausgewaehlten Artikels. Eine groessere
   Zustellung nicht ungeprueft an das Produkt anbauen.

[Belege und Arbeitspaket](docs/superpowers/plans/2026-11-01-rattm-bildmasse.md).
Die nachfolgende Liste beschreibt den Stand vor der konkreten Produktauswahl.

## Nach Stand11

Rechte Tellerlage, sichtbare native Wechselstellung, vier seitliche Fangbleche
und Demontagestand umgesetzt. Vor weiterer Detaillierung bleiben:

1. Reale Spindel-/Spannpaketzeichnung und Kopfaufmass; SK30/BT30-Kopplung klaeren.
2. Zustellmechanik389,33mm, Retention, Indexierung und gesamte Wechselbahn mit
   realen Werkzeugen/Werkstuecken auslegen; jetzige Wegstichproben sind begrenzt.
3. Fangblechhalter/Reinigung/Fugen, Tankwartung und Sensorhalter detaillieren.
4. Entfernte Originalfunktionen (Not-Halt, Endlagen, XMT-Treiber, PE-Verteilung)
   im neuen Elektrokonzept ersetzen und pruefen; keine Betriebsfreigabe.

Aktuelle Anleitung: projekt/Dokumentation/Entwicklungsstand_11.md.
Plan: docs/superpowers/plans/2026-11-01-wechselstellung-spaenefang11.md.
Die folgenden Aufgabenlisten dokumentieren fruehere Arbeitsstaende.

## Naechste Schritte nach Tellerentwurf10 (01.11.2026)

1. Nutzerartikel1005009887984460 anhand Titel, Variante und Preis identifizieren.
   Mit vollstaendigem Spann-/Loesesystem und Eigenbau-Teller vergleichen; keine
   Kaufentscheidung anhand historischer Indexpreise.
2. Kopf/Pinole/Spindeldurchgang und Bezugsflaechen messen; passende gemeinsame
   Herstellerzeichnung beschaffen. Spannpaket inklusive Lastabstuetzung auslegen.
3. Zustellung419mm, Retention, Schutzverschluss und ganze Wechselbahn aus der
   ausgewaehlten Spindel ableiten; jetzige552 Endpunktchecks sind nur eine Teilpruefung.
4. Tankwartung trotz hinterem Holm, Tuerentwaesserung und sechs unmontierte
   Sensorreferenzen bearbeiten; sechs echte Maschinenanschluss-Konflikte separat.
5. Revisionsgleiche Fertigungszeichnungen/Abwicklungen und Montageunterlagen
   nach den Istmassen ausarbeiten. R02/R07/R11/R13 teilweise bearbeitet, nicht freigegeben.

Aktueller Arbeitsnachweis: `docs/superpowers/plans/2026-11-01-teller-spannpaket-kss.md`.
Neue Daten und Grenzen: `projekt/Dokumentation/Entwicklungsstand_Teller_10.md`.
Nachfolgende Priorisierung ist der vorherige Stand.

## Aktuelle Roadmap mit Entwicklungsprompts

Siehe `docs/superpowers/plans/2026-10-31-entwicklungsroadmap.md` (R00–R14).
R00 Journal-/Offline-Pruefung ist erledigt; R01-Hashdiagnose abgeschlossen,
produktive Referenzmigration bleibt offen. Naechstes begrenztes Softwarepaket:
R02 Fertigungsmetadaten/Nachweisregister; danach Messvorbereitung R03 und
nativer Zeichnungs-/Exportpilot R08. Mechanische Detailpakete erst mit ihren
Istwerten und dokumentierten Kaufteil-/Spindelentscheidungen.
Keine alten CAD-Dateien vom PC verwenden. Die folgende Tabelle ist die
historische Priorisierung der Uebergabe; Original-PRT-Uebernahme ist ueberholt.

## Fortschritt 31.10.2026

Neuerzeugung09 im Git-Projekt und erneutes natives Oeffnen sind erledigt;
siehe `cad/README.md`. Alte CAD-Dateien werden nach neuer Nutzerentscheidung
fuer diesen Lieferstand nicht uebernommen. P0 ist damit teilweise erfuellt:
Offline-Tests in separatem Standard-Python und die Ursache der Rezept-Hashabweichung
bleiben offen. Als naechste konstruktive Arbeit bleiben belegte Istmasse,
Anschlusskonflikte und der Spannpaket-/Patronenvergleich. Native Dateierzeugung
allein bestaetigt weder reale Maschinenpassung noch Betriebsbereitschaft.

Die Reihenfolge ist ein Übergabevorschlag. Kein Punkt wird durch die Paketübernahme als erledigt markiert.

| Priorität | Arbeitspaket | Fertig, wenn … |
|---|---|---|
| P0 | Vorhandenen Stand reproduzieren | Paket-/Quellhashes, neue Offline-Protokolle, lokal tatsächlich vorhandene NX-Version/Dateien und Abhängigkeiten erfasst; keine Geometrieänderung |
| P0 | Nutzer-NX-Ausgangsbaugruppe sichern und analysieren | Vollständige Komponenten/Referenzen/Koordinaten als Bericht, Originale unverändert, Unterschiede zur Rezeptrekonstruktion bekannt |
| P1 | Spannpaket / komplette ATC-Patrone vergleichen | Lieferantenzeichnung und Istmaßbedarf, Halter-/Bolzenschnittstelle, Kraftfluss, Bauraum und Risiken gegenübergestellt; Entscheidung nicht vorgetäuscht |
| P1 | X-/Y-/Z-Anschlüsse fertig auslegen | 35 Messaufgaben abgeglichen, alle sechs Konflikte konstruktiv gelöst oder als echte Foto-Modellabweichung belegt; erreichbare Hübe geprüft |
| P2 | Spindelsätze und Halter fertig bestellen/fertigen können | Lieferantenbestätigte Endenbearbeitung, Lagerbezüge, Kupplungseingriffe, Zeichnungen mit Material/Passungen/Toleranzen und Bestellnummern |
| P2 | Elektrik und Antriebe abschließen | Exakte Revisionen, Versorgung inkl. Brems-/Rückspeiseenergie, Motor-/Treiberkompatibilität, Schutzkonzept und fachlich geprüfter Stromlaufplan |
| P2 | Tür/Einhausung/KSS fertigungsgerecht machen | Tatsächliche Blechfeatures/Abwicklungen, Fertigungsverfahren, Lager/Führungen, Gewichtsausgleich/Fangsicherung, Verriegelung, Dicht-/Spänerücklaufdetails belegt |
| P3 | ATC nach festgelegter Spindel integrieren | Nutzbare Tischfläche mit Spannmitteln bewertet, Magazin/Retention/Schutzhaube/Orientierung, gesamte Wechselbahn und Fehlerzustände geprüft |
| P3 | Gesamtpaket zur praktischen Umsetzung | Modell, reale Stückliste, Fertigungszeichnungen, Bauanleitung, Elektrik und Prüfprotokolle auf derselben freigegebenen Revision |

## Erster überschaubarer Codex-Auftrag

Übernahmebericht statt neuer Geometrie: Inputs lesen, Hashes prüfen, Offline-Suite ausführen,
NX-Umgebung und vorhandene Originaldateien erfassen. Den Bestandsanalysecode aus
`referenzen/archiv/CNC_UMBAU_NXOPEN_Entwicklung_10.zip` zuerst lesen; ihn nicht ungeprüft in
`projekt/` verschieben. Nur in separater Arbeitskopie und mit neuer Ausgabe testen.

## Danach: Spannpaket-Machbarkeit

Lese `uebergabe/SPANNPAKET_ATC.md`, das vorhandene Lieferantenanschreiben und
`projekt/Werkzeugwechsler/ATC_Schnittstellenstatus_09.json`. Bestimme minimal notwendige
Messungen an Kopf, Pinole und Spindel. Für Kandidaten Hersteller-/Lieferantenzeichnungen
beschaffen, keine Auswahl allein nach dem niedrigsten AliExpress-Variantenpreis.

## Abnahme jeder Änderung

Plan + Quelldaten → gezielter Test → kleine Änderung → Offline-Test → realer NX-Lauf →
Geometrie-/Bewegungsprüfung → Stückliste/Anleitung/Zeichnung synchronisieren.
Nicht ausgeführte Schritte offen lassen. Kein Maschinenbetrieb durch Codex während der CAD-Entwicklung.
