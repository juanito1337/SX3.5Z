import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'projekt'))
import NX_ATC_Konzept13 as journal
journal.main(probe_only=True)
