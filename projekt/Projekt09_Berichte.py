"""Normal Python3.10+, no NX needed: update CSVs and blocked release report."""
from umbau_daten09 import export
if __name__=='__main__':
    import json
    print(json.dumps(export(),ensure_ascii=False,indent=2))
