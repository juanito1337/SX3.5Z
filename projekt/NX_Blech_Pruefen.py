# -*- coding: utf-8 -*-
"""Optional short test: just the wide upper door frame, no whole machine."""
import os,sys,runpy
HERE=os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:sys.path.insert(0,HERE)
ns=runpy.run_path(os.path.join(HERE,'NX_CNC_Gesamtansicht.py'),run_name='nx06_sheet_test')
ns['main'](parts_only=True,part_filter=['Senktuer_UPPER_Rahmen'])
