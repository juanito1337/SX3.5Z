"""Independent offline STEP readback, not a native NX reimport claim."""
import json
from datetime import datetime
from pathlib import Path
import cadquery as cq

root = Path(__file__).resolve().parents[3]
path = root / 'cad/step/SX35Z_12_Wechselstellung.step'
shape = cq.importers.importStep(str(path))
solids = shape.solids().vals()
assert len(solids) == 461, len(solids)
invalid = [i for i, solid in enumerate(solids) if not solid.isValid()]
assert not invalid, invalid
box = shape.val().BoundingBox()
result = dict(date=datetime.now().astimezone().isoformat(), environment='isolated repository .venv CadQuery/OCP',
    check='independent offline STEP reimport', solids=len(solids), invalid_solids=invalid,
    bounds_mm=dict(xmin=box.xmin,xmax=box.xmax,ymin=box.ymin,ymax=box.ymax,zmin=box.zmin,zmax=box.zmax),
    native_nx_reimport=False, manufacturing_released=False)
(Path(__file__).parent/'readback_result.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))
