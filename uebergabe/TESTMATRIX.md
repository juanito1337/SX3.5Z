# Welche Prüfung beweist was?

| Prüfung | Umgebung | Belegt | Belegt NICHT |
|---|---|---|---|
| Paketmanifest | Standard-Python, nur lesen | Bytes stimmen mit dieser Lieferung überein | Inhalt technisch korrekt oder sicher |
| Python-3.10-AST | Standard-Python | Syntax im gewählten Grammatikstand | Code unter NX erfolgreich ausgeführt |
| pytest | Separate Python-/CadQuery-Umgebung | Ausgewiesene Programmlogik und Teilgeometrie | Gesamte Maschine, reale Passungen, Sicherheitsfunktionen |
| Unabhängiger Kernelaufbau | CadQuery/OCP | Analytische Vorformen im angegebenen Umfang | NX-Blech-Endzustand, reale Fertigung oder Kraftauslegung |
| Native Einzelteilprobe | NX2406 | Genutzte API, einzelne Features und Speichern | Vollständige Hauptbaugruppe |
| Nativer Gesamtaufbau | NX2406 | Erzeugung/Speichern referenzierter Teile | Durchgehende Bewegungskollision oder Fertigungsfreigabe |
| Aufmaß/Lieferantenprüfung | Reale Maschine/Herstellerunterlagen | Bestimmte Maße/Schnittstellen/Lieferumfänge | Alle noch offenen Eigenschaften |
| Technische Abnahme | Realer Aufbau mit Fachprüfung | Genau spezifizierte Prüfmerkmale | Alles außerhalb des dokumentierten Umfangs |

Die sechs bekannten Grundmaschinenkonflikte bleiben sichtbar; sie werden nicht durch eine
Nullmeldung der neuen Normteile oder durch die eingeschränkte Magazin-Endpunktprüfung aufgehoben.

Neue Protokolle nach `ergebnisse/offline/` bzw. `ergebnisse/nx/`. Alte Berichte nicht überschreiben.
Zu jedem Lauf Revision, Parameterhashes, Befehle, Umgebung, Zeitpunkt, Ergebnis und Ausschlüsse erfassen.
