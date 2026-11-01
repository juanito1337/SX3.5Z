# -*- coding: utf-8 -*-
"""07.3: build only the ten sloped KSS sheets after the normal API probes.

Play this journal INSIDE Siemens NX. A fresh output folder is used. It does
not resume or change a previous 406-part run, nor create the whole assembly.
Native saved solids are checked by the existing geometry path. These flat
sloped precursors do not claim a sheet-metal conversion or a flat pattern.
"""
import os
import runpy
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
ns = runpy.run_path(os.path.join(HERE, 'NX_CNC_Gesamtansicht.py'), run_name='nx073_kss_test')
selected = [d['name'] for d in ns['model'].recipe() if 'plate_normal_thickness' in d]
if len(selected) != 14:
    raise RuntimeError('KSS-Test11 erwartet zehn Leit-/Trichterbleche und vier Fangbleche.')
ns['main'](parts_only=True, part_filter=selected)
