"""Independent offline readback of NX-generated STEP, not native reimport."""
from pathlib import Path
import cadquery as cq
import json,hashlib,shutil,sys
from datetime import datetime
root=Path(__file__).resolve().parents[3]
runs=json.loads((Path(__file__).parent/'lieferlaeufe.json').read_text(encoding='utf-8-sig'))
results=[]
for pose,directory in runs.items():
 run=Path(directory);reports=list(run.glob('NX_Wiederoeffnung13_*.json'))
 report=json.loads(reports[-1].read_text(encoding='utf8'));assert report['journal_completed']
 source=Path(report['step_export']['file']);target=root/'cad/step'/('SX35Z_13_'+pose.capitalize()+'.step')
 if target.exists():raise FileExistsError(target)
 shutil.copy2(source,target)
 shape=cq.importers.importStep(str(target));solids=shape.solids().vals()
 assert len(solids)==532,len(solids)
 invalid=[i for i,s in enumerate(solids) if not s.isValid()];assert not invalid,invalid
 b=shape.val().BoundingBox()
 results.append(dict(pose=pose,file=str(target),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),date=datetime.now().astimezone().isoformat(),solids=len(solids),invalid=invalid,bounds_mm=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax],native_nx_reimport=False,manufacturing_released=False))
 print(pose,len(solids),'valid solids',flush=True)
(Path(__file__).parent/'step_readback.json').write_text(json.dumps(results,indent=2),encoding='utf8')
