# Referenzgrundlage des neuen NX-Sheet-Metal-Pfads

Abgerufen 2026-10-29. Keine lokale Siemens-NX-Laufzeit vorhanden.
Die Siemens-verfasste ältere C++-NXOpen-Referenz ist auf einem öffentlichen Spiegel
zugänglich. Das ist KEINE verifizierte aktuelle NX-2406-Python-Referenz. Die verwendeten
Python-Eigenschaften entsprechen dem dokumentierten Klassen-/Methodenvertrag; ihre
konkrete Verfügbarkeit, Nullobjektbindung und Lizenz müssen in NX 2406 bestehen.

- ConvertToSheetmetalBuilder: BaseFace, MaintainZeroBendRadius, CommitFeature.
  https://www.ugapi.com/doc/nxopen/a03085.html
- SheetmetalManager: CreateConvertToSheetmetalFeatureBuilder(Feature),
  IsSheetmetalBody, GetBodyThickness. Factory nennt NX Sheet Metal Lizenz.
  https://www.ugapi.com/doc/nxopen/a03114.html
- PartSheetmetal: SetThickness, SetBendRadius, SetNeutralFactor und Commit.
  https://www.ugapi.com/doc/nxopen/a04631.html

Der Adapter erfindet keine Alternativaufrufe, wenn ein Vertrag fehlt. Insbesondere
kein automatisch gewählter Ganzzahl-Tag statt Face, kein blindes erstes Flächenobjekt
und kein stilles Umschalten auf Volumenansicht. Einfache U-Probe vor dem Gesamtaufbau.

Das nominale K-Modell und die Federkraftstudie sind eigene Entwurfsannahmen;
die Renderbilder belegen weder Herstellergeometrie noch Federdaten.
