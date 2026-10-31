# -*- coding: utf-8 -*-
"""NX 2406: neue09-Teile + vier geänderte Anschlusskörper; keine ATC-Funktionsfreigabe."""
import os,sys
HERE=os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:sys.path.insert(0,HERE)
if 'NX_CNC_Gesamtansicht' in sys.modules:del sys.modules['NX_CNC_Gesamtansicht']
import NX_CNC_Gesamtansicht as journal
parts=[d['id'] for d in journal.model.recipe() if d.get('revision_added')=='09' or d['name'] in {'Staender_Blechschuerze_links','Staender_Blechschuerze_rechts','KSS_Serviceklappe_hinten','Schaltschrank_Hohlschale'}]
if __name__=='__main__':journal.main(parts_only=True,part_filter=parts)
