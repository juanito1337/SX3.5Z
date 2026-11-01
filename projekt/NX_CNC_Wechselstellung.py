"""Create a separate native change-position assembly. No motion or machine IO."""
import os,sys
HERE=os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:sys.path.insert(0,HERE)
if 'NX_CNC_Gesamtansicht' in sys.modules:del sys.modules['NX_CNC_Gesamtansicht']
import NX_CNC_Gesamtansicht as journal
if __name__=='__main__':journal.main(pose='wechsel')
