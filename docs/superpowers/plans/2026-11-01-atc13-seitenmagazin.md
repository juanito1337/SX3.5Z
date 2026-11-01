# ATC13: zwoelf Plaetze, seitlicher Speicher und einzelner Uebergabearm

Nutzerauftrag01.11.2026: besten plausiblen Ansatz direkt in NX umsetzen und
zur Ansicht liefern;8 ausreichend,12 bevorzugt. Ausfuehrung ist beauftragt.
Basis e8a0029; bestehende PRT und Quellen nicht ueberschreiben.

## Entwurf und Abgrenzung

Gewaehlter Bearbeiteransatz: festes12er-Magazin rechts/hinten auf einem mit
dem Untergestell verbundenen Zusatzrahmen. Einzelner vertikal hebbarer
Schwenkarm mit kurzer radialer Zustellung, formschluessigem Greifer und
definierten/verriegelten Endlagen. Langsamer sequenzieller Wechsel ist
akzeptiert als Entwurfsentscheidung, keine Nutzerforderung nach Taktzeit.
Ring um den Kopf verworfen wegen zusaetzlicher Z-Masse und bleibender
Zustellnotwendigkeit; gesamtes Magazin schwenken bewegt unnoetig viel Masse.
RATTM8er bleibt historische Kaufoption; neuer12er Eigenbau ist keine
behauptete12er-Ausfuehrung dieses Kaufteils.

Grundmaschine und Achshuebe erhalten. Keine Annahme unbegrenzter Werkstuecke:
Parkstellung gegen vollstaendige Maschinen-Verfahrhuelle pruefen, Wechsel
gegen einen explizit benannten freizuhaltenden Raum. Werkstuecke/Spannmittel
in diesem Raum bleiben Wechselhindernisse. SK30-Bestand bleibt Referenz;
BT30-Spindel/Orientierung/Spannpaket fuer Betrieb noch auszulegen.

## Arbeitspakete

1. Ausgangsstand sichern, Geometrie/Mechanik unabhaengig pruefen. Parameter,
   Quellen und Grenzen dokumentieren. Eigenen Konzeptzweig im vorhandenen
   Arbeitsverzeichnis verwenden, keine gemeinsamen NX-Fenster anfassen.
2. Neue Variante `projekt/atc13_modell.py` auf erhaltenem12er Grundmodell:
   alte ATC-Konsole entfernen,12erMagazin, Hebe-/Schwenk-/Zustellmechanik,
   Zusatzrahmen und passende Schutzverkleidung. Produktionsstand12 bleibt
   reproduzierbar;13 wird als neue Konzeptvariante benannt.
3. Zuerst Tests fuer zwoelf Plaetze, Erreichen beider Uebergaben,
   unveraenderte Achshuebe, keine alten ATC-Bauteile, Parameterfehler und
   Parkabstand. Offline Weg-/Volumenpruefung inklusive Greifer/Traeger und
   Beispielwerkzeug; echte Kontakte getrennt von ungewollten Schnitten.
4. Native NX-Journale fuer neue parametrische Einzelteile/Gesamtbaugruppen
   PARK und SPINDEL, frisches Wiedereroeffnen und STEP-Export. Pflichtblech
   weiterhin required. Keine Erfolgsbehauptung aus Offline-Geometrie.
5. Stueckliste, Kauf-/Fertigungsstatus, Bewegungsfolge, Greifer-/Spindel-
   Schnittstellen und offene Detailarbeit gemeinsam liefern. CAD-Vorschau
   mit Park- und Wechselraum, Protokolle mit Datum/Revision/Befehl/Exitcode.
6. Unabhaengiger Abschlussreview, wichtige Befunde beheben, passende Tests,
   Git sichern und sichtbare NX/STEP-Dateien zum Nutzer zurueckgeben.

## Review-Schwerpunkte

- Arm/Tool kollidieren auf dem Schwenkbogen mit Saeule oder Kopf.
- Parkmechanik oder neues Gehaeuse beschneiden X/Y/Z-Verfahrraum.
- Werkzeugrichtung im Magazin stimmt nach Armschwenk nicht mit Spindel
  ueberein; notwendige Orientierung explizit definieren.
- Uebergabe doppelt belegter/leerer Tasche und Klemmreihenfolge plausibel.
- Tragwerk, Fuehrungen und Verriegelungen nicht nur frei schwebende Huellen.
- Herstellermaße und bewusst angenommene Konstruktion nicht vermischen.

## Fortschritt

- Arbeitspakete1–6 abgeschlossen: Reviews mit Korrekturen,201/99 Offline-Tests,62 Wegstichproben, beide nativen Stellungen frisch geoeffnet und STEP geprueft. Dokumentation/Katalog/Stueckliste gemeinsam aktualisiert. Fertigungs-/Betriebsdetails bleiben laut Konzeptdokument offen.
