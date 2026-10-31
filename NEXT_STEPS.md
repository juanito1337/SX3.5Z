# Priorisierte Fortsetzung

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
