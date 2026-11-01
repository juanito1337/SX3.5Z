"""Retired09 generators must stop before touching historical outputs."""
import subprocess,sys
from pathlib import Path
import pytest

@pytest.mark.parametrize('script',['arbeitsmappe09_erzeugen.py','bauanleitung09_erzeugen.py',
                                   'atc_anschlusspruefung09.py'])
def test_historical_generator_stops_with_clear_version_error(script):
    root=Path(__file__).resolve().parents[1]
    result=subprocess.run([sys.executable,'-B',str(root/'tools'/script)],
                          cwd=root,capture_output=True,text=True,timeout=120)
    assert result.returncode!=0
    assert 'Historischer09-Generator' in result.stderr
