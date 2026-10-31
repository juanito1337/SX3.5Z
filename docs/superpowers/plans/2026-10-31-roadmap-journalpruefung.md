# Roadmap, Detailaudit und native Journalpruefung

Auftrag 31.10.2026: Entwicklungsroadmap mit ausfuehrbaren Prompts erstellen,
fehlende Detailausarbeitung am realen Projekt pruefen, NX-Journale ausfuehren
und reproduzierte Fehler mit Superpowers beheben. Basis: Commit 6631f8b.

## Vorgehen und Umfang

Bestehende Struktur und neu erzeugten Git-CAD-Stand verwenden. Keine alten
CAD-Dateien vom PC. Arbeit im vorhandenen Git-Projekt; keine Umstrukturierung
oder zusaetzlicher Checkout. Die Nutzeranweisung zur Roadmap und Fehlerbehebung
ist der Ausfuehrungsauftrag fuer den ersten Software-/Pruefblock.

- [x] Iststand anhand Code, Katalog, Fertigungsliste und Nachweisen erfassen.
  Unabhaengige read-only Teilpruefungen: technische Luecken und Rezept-Hash.
- [x] Lokale `.venv` mit separater vorhandener Standard-Python-Laufzeit erstellen;
  requirements-offline.txt installieren. Kein Paket in NX-Python installieren.
- [x] Paketpruefer, Hilfstests und vollstaendige aktive pytest-Suite ausfuehren.
  Erwartete Manifestabweichungen seit Uebergabe einzeln dokumentieren.
- [x] Alle sieben aktiven NX-Journale in frischen Prozessen pruefen; Metadaten,
  Blech, KSS, Achskern, Normteile/ATC, Gesamtaufbau und Wiedereroeffnung.
  Neue Laufordner und Rohprotokolle mit Revision/Umgebung/Befehl/Exitcode.
- [x] Fehler systematisch reproduzieren, minimale Regression vor Korrektur,
  keine toleranz- oder freigabeveraendernden Umgehungen. Gezielte native
  Nachpruefung fuer NX-Code; Offline-Suite nach Aenderungen.
- [x] Roadmap in docs/superpowers/plans/2026-10-31-entwicklungsroadmap.md ablegen:
  Quelle, Detaildefizit, Prioritaet, Abhaengigkeit, Entwicklungsprompt,
  Lieferumfang und messbare Abnahme je Arbeitspaket. Status ehrlich markieren.
- [x] Neue Nachweise unter ergebnisse/ erhalten, kompakte Nachweise gezielt
  versionieren, Review, Git-Diff und abschliessende Synchronisation pruefen.

## Abnahme und Grenzen

Fertig fuer diesen Auftrag: belegte Roadmap und abgearbeiteter erster
Journal-/Softwareblock. Mechanische Pakete mit fehlenden Istmassen oder
Spindelauswahl bleiben explizit offen; keine geschaetzten Freigaben.
Native Dateiverarbeitung beweist keine reale Passung, Kollisionsfreiheit,
Tragfaehigkeit, Maschinen-/ATC-Sicherheit oder Beschaffungsfreigabe.

## Review-Fokus

Keine alten CAD-Eingaben; native und Offline-Nachweise getrennt; keine
silent skips; historisches Paketmanifest und historische Berichte erhalten;
Pruefung verwendet denselben aktiven Quellstand wie die Ergebnisse.

## Ergebnis der Diagnose

Keine neue native Laufzeitfehlfunktion in sieben Journallaeufen. Keine
spekulative Produktionskorrektur; deshalb kein neuer TDD-Codezyklus erforderlich.
Die Hashabweichung wurde mit identischem Code und zwei exakt reproduzierten
Zielhashes erklaert, nicht durch Abschalten einer Pruefung verdeckt.
Die Roadmap enthaelt die verbleibende produktive Referenzmigration gesondert.

## Abschlussreview

Unabhaengiges schreibgeschuetztes Review am 31.10.2026: keine kritischen oder
wichtigen Befunde. Tabellenzahlen, Journalmatrix, Wiedereroeffnung, Blechstatus,
Offline-Ergebnisse und Diagnose gegen Rohprotokolle abgeglichen. Keine erneute
NX-Ausfuehrung durch den Reviewer. Aktiver Quellstand und versioniertes CAD
unveraendert. Die beiden kanonischen Rezept-Hashes separat nachgerechnet.
Nur Dokumentation und ausgewaehlte Pruefnachweise versioniert; `.venv/` und
`NX_Laeufe/` bleiben lokal. Rohprotokolle behalten ihre Originalzeilenenden;
der abschliessende Whitespace-Check umfasst die bearbeitete Dokumentation und
Diagnoseskripte, nicht unveraenderte Laufzeitausgaben.
