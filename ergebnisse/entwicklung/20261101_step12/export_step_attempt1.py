"""One-off read-only NX2406 export of the verified revision12 assembly.
API source: installed UGOPEN/pythonStubs/NXOpen/__init__.pyi.
Never saves or modifies source PRT files.
"""
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
import NXOpen

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / 'cad/nx/SX35Z_CNC_UMSETZUNG_12_BT30_KONSOLE_WECHSEL_20261101_130001_853869_fdd87de5a7ba'
OUT = ROOT / 'cad/step/SX35Z_12_Wechselstellung.step'

def main():
    assert not OUT.exists(), 'Do not overwrite an existing export'
    OUT.parent.mkdir(parents=True, exist_ok=True)
    originals = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in RUN.rglob('*.prt')}
    session = NXOpen.Session.GetSession()
    assert not list(session.Parts), 'Fresh background session required'
    opt = session.Parts.LoadOptions
    opt.ComponentsToLoad = NXOpen.LoadOptions.LoadComponents.All
    opt.UsePartialLoading = False
    opt.UseLightweightRepresentations = False
    opt.AllowSubstitution = False
    opt.AbortOnFailure = True
    opt.ComponentLoadMethod = NXOpen.LoadOptions.LoadMethod.SearchDirectories
    opt.SetSearchDirectories([str(RUN), str(RUN/'Teile'), str(RUN/'Unterbaugruppen')], [False]*3)
    source = RUN / (RUN/'HAUPTBAUGRUPPE.txt').read_text(encoding='utf8').strip()
    part, status = session.Parts.OpenBaseDisplay(str(source))
    try:
        assert status.NumberUnloadedParts == 0
    finally:
        status.Dispose()
    groups = part.ComponentAssembly.RootComponent.GetChildren()
    leaves = [c for g in groups for c in g.GetChildren()]
    assert len(leaves) == 461
    assert all(c.Prototype.IsFullyLoaded for c in leaves)
    builder = session.DexManager.CreateStepCreator()
    try:
        builder.SettingsFile = 'C:/Siemens/nx2406/STEP214UG/ugstep214.def'
        builder.ExportAs = NXOpen.StepCreator.ExportAsOption.Ap214
        builder.ExportFrom = NXOpen.StepCreator.ExportFromOption.DisplayPart
        builder.OutputFile = str(OUT)
        builder.ObjectTypes.Solids = True
        builder.ObjectTypes.Surfaces = False
        builder.ObjectTypes.Curves = False
        builder.ColorAndLayers = True
        builder.LayerMask = '1-256'
        builder.ExportExtRef = False
        builder.FileSaveFlag = False
        builder.ProcessHoldFlag = True
        builder.Commit()
    finally:
        builder.Destroy()
    assert OUT.is_file() and OUT.stat().st_size > 1000
    assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p,h in originals.items())
    result = dict(date=datetime.now().astimezone().isoformat(), source_revision='346934ac2d1be35b0ba68bb5fde998e00d3d3431',
        environment='NX2406 / '+sys.version, source=str(source), output=str(OUT), source_parts=461,
        source_prt_unchanged=True, bytes=OUT.stat().st_size, sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),
        manufacturing_released=False, atc_operational=False)
    (Path(__file__).parent/'export_result.json').write_text(json.dumps(result, indent=2), encoding='utf8')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
