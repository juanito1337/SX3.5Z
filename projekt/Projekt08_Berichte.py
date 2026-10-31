# -*- coding: utf-8 -*-
"""Refresh current model/BOM/measurement-status CSV+JSON reports. No NX dependency."""
from umbau_daten08 import export
import json
if __name__ == '__main__':
    print(json.dumps(export(), ensure_ascii=False, indent=2))
