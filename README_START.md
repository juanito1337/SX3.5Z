# SX3.5Z CNC – Übergabe an Codex

**Produktauswahl01.11.2026:** Der Nutzer hat AliExpress1005009887984460 gewaehlt
und sechs Mass-/Detailbilder geliefert. Direkte Befestigung an der Fraese ist
erlaubt. [Bildauswertung und offene Anschluesse](projekt/Werkzeugwechsler/RATTM_1005009887984460_Bildauswertung.md).
Die folgenden nativen CAD-Dateien11 zeigen noch den bisherigen Eigenentwurf,
nicht diesen Kaufwechsler. Katalog/Einkaufsliste kennzeichnen diese Abweichung.

**Aktuell: Stand11 vom01.11.2026.** Rechter Teller mit eigener Park- und
Wechselbaugruppe bis zur nominellen Spindelachse; vier beidseitige Fangbleche,
61 entfallene Originalanbauten. Beide nativen NX-Stellungen neu gespeichert
und frisch wieder geoeffnet, jeweils454 Einzelteile und17 Unterbaugruppen.
[CAD-Einstieg mit beiden Dateien](cad/README.md) und
[aktuelle Anleitung/Grenzen](projekt/Dokumentation/Entwicklungsstand_11.md).
Aktuelle Tabellen tragen `_11`. Spannpaket/BT30-Passung und elektrische
Ersatzfunktionen bleiben offen. HTML-Ansichten10/09 sind historisch.
Die folgenden Stand10/09-Angaben sind durch diese Fortschreibung ueberholt.

**Aktuell: Tellerentwurf10, 01.11.2026.** Der seitliche8er-Teller ersetzt das
Tischmagazin. Neue native511 Einzelteile und20 Unterbaugruppen sind in NX2406
erzeugt und erneut vollstaendig geladen. Einstieg: [native Dateien](cad/README.md),
[3D-Vorschau](projekt/Ansicht_Teller_10.html),
[Entwicklungsstand und Anleitung](projekt/Dokumentation/Entwicklungsstand_Teller_10.md).
Die HTML-Vorschau ist neu erzeugt, aber noch nicht visuell im Browser geprueft.
**Spannpaket weiterhin nur Bauraum, keine funktionsfaehige automatische Spannung.**
Aktuelle Tabellen tragen `_10`; alte09-Berichte und `Ansicht_3D.html` sind historisch.
Die folgenden Angaben zur unveraenderten Paketuebernahme gelten fuer31.10.,
nicht fuer den inzwischen erweiterten aktiven Programmstand.

**Entwicklungsfortsetzung:** Die [Roadmap mit Entwicklungsprompts](docs/superpowers/plans/2026-10-31-entwicklungsroadmap.md)
ordnet die offenen Detailarbeiten. Der [aktuelle Journalpruefbericht](docs/superpowers/plans/2026-10-31-journalpruefbericht.md)
belegt sieben erfolgreiche native Journallaeufe und die jetzt lauffaehige Offline-Suite.

**Aktueller Zusatz vom 31.10.2026:** Neue native Stand09-Dateien liegen jetzt
unter `cad/nx/`, ausschliesslich aus dem aktuellen Projektcode erzeugt. Der
vollstaendige NX-Aufbau und das erneute Oeffnen sind nachgewiesen. Einstieg und
Pruefgrenzen: [`cad/README.md`](cad/README.md). Die untenstehende Beschreibung
dokumentiert das urspruengliche Uebergabepaket vor dieser Neuerzeugung.

**Übergabe: 31.10.2026 · Maschinenbasis: Umsetzung 09 vom 30.10.2026**

Dies ist ein vollständiges Arbeits- und Quellenpaket für die Fortsetzung. Es ist **keine neue
Maschinenrevision**, kein betriebsbereiter Werkzeugwechsler und keine Fertigungs-/Bestellfreigabe.
Die 335 Dateien des letzten vollständigen Quellpakets liegen unverändert unter `projekt/`.

## Start auf dem NX-Rechner

1. Das ZIP in einen neuen lokalen Ordner entpacken, z. B. `C:\Projekte\SX35Z_Codex_Projekt`.
   Nicht über einen bestehenden Arbeitsordner entpacken. Alle relativen Unterordner erhalten.
2. In Codex diesen **Paketstamm** als lokalen Projektordner öffnen: den Ordner mit `AGENTS.md`,
   nicht nur `projekt/`. Superpowers in der verwendeten Codex-Umgebung auswählen bzw. erkennen lassen.
3. Den Inhalt von `CODEX_STARTPROMPT.txt` als ersten Auftrag verwenden.

Ein bloßer ZIP-Anhang ist nicht in jeder Codex-Oberfläche gleichbedeutend mit einem bearbeitbaren
lokalen Repository. Das entpackte Verzeichnis ist der gemeinsame Ausgangspunkt. Bei einer
Cloud-Ausführung stehen die lokale Windows-/NX-Installation und Lizenz nicht automatisch bereit.
Die aktuellen OpenAI-Quellen dazu stehen in `uebergabe/CODEX_QUELLEN.json`.

## Die wichtigsten Dateien

| Datei/Ordner | Bedeutung |
|---|---|
| `AGENTS.md` | Dauerhafte Arbeitsregeln: NX, Quellen, Originalschutz, Superpowers, Prüfgrenzen |
| `PROJECT_STATUS.md` | Was vorhanden ist und was NICHT fertig oder bestätigt ist |
| `NEXT_STEPS.md` | Priorisierte Aufgaben mit konkreten Abnahmekriterien |
| `NX_ENVIRONMENT.md` | Beobachtete NX-2406-Umgebung und sichere Testfolge |
| `uebergabe/SPANNPAKET_ATC.md` | Letzter Diskussionsstand zu Zugstange, Federpaket und ATC-Patrone |
| `projekt/` | Vollständiger, unveränderter Quellstand09 einschließlich Modell, Tests und Dokumenten |
| `referenzen/` | Originalprompt, 72 Fotos, Handbücher/OCR, BF20-ZIPs, Logs und getrennte historische Zweige |
| `eingaben/` | Platz für eigene NX-Originalkopien, bestätigte Maße und Lieferanten-CAD |
| `ergebnisse/` | Platz für künftige Prüfläufe; keine Hardwareausführung beim Öffnen |

## Sofort ansehen oder nativ erzeugen

`projekt/Ansicht_3D.html` zeigt den vorhandenen Entwurf offline im Browser.
Das Gesamtjournal lautet `projekt/NX_CNC_Gesamtansicht.py` und gehört **in Siemens NX**, nicht in
gewöhnliches Python. Die Einzeltests heißen `NX_Blech_Pruefen.py`, `NX_KSS_Pruefen.py`,
`NX_Umbau_Kern_Pruefen.py` und `NX_Normteile_ATC_Pruefen.py`.
Details und benötigte NX-Funktionen stehen in `projekt/LIESMICH.md`.

## Was du noch lokal ergänzen musst

Deine tatsächlich erzeugten oder manuell geänderten `.prt`-Dateien sind hier nicht vorhanden.
Eine **Kopie der vollständigen Originalbaugruppe mitsamt allen referenzierten Teilen** gehört nach
`eingaben/original_nx/`. Deine lokal geänderten Parameter erst vergleichen, nicht blind durch die
mitgelieferten Standardparameter ersetzen. Lieferantendaten und bestätigte Messwerte haben eigene
Ordner. Keine fehlenden Maße durch Schätzungen als "gemessen" eintragen.

## Nachweise dieser Übergabe

Neu ausgeführt: 112 bestehende Offline-Tests und 91 Untertests; 10 Tests des neuen
Integritätsprüfers. Die genaue Umgebung und die ZIP-/Dateiprüfung stehen unter
`uebergabe/pruefung/`. Diese Prüfungen sind **kein Siemens-NX-Lauf** und keine mechanische Abnahme.

Der neue Helfer liest nur Dateien:

```powershell
python tools_handoff/verify_package.py
```

Er prüft die enthaltenen SHA-256-Werte. Nach absichtlichen Änderungen sind Abweichungen erwartbar;
zum Arbeiten Git-Diffs verwenden und den ursprünglichen Nachweis nicht stillschweigend ersetzen.

## Datenschutz und Umfang

Fotos, Handbücher und Logs sind unverändert enthalten. Logs enthalten lokale Nutzernamen/Pfade;
Fotos können Metadaten und Werkstattdetails enthalten. Kein Repository automatisch veröffentlichen.
Superpowers, Siemens NX, Lizenzen, Hersteller-CAD und Codex selbst werden durch das ZIP nicht installiert.
