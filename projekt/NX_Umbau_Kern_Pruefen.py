"""Run in NX: revised drive-chain and cabinet parts only. New output, no source writes."""
import os,sys
HERE=os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:sys.path.insert(0,HERE)
for name in ('NX_CNC_Gesamtansicht',):
    sys.modules.pop(name,None)
import NX_CNC_Gesamtansicht as app
selected=[p['name'] for p in app.model.recipe() if p['group'] in ('11_CNC_X','12_CNC_Y','13_CNC_Z','16_Schaltschrank','18_Prueffeld')]
app.main(parts_only=True,part_filter=selected)
