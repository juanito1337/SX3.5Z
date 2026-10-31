"""Offline diagnosis only: no NX imports, geometry builds, or source changes.

Only writes evidence beside this script. UCRT/math overrides are process-local.
The Decimal series is a diagnostic reconstruction, NOT a production replacement.
"""
import ctypes
import decimal
import hashlib
import json
import math
import platform
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
sys.path.insert(0, str(ROOT / 'projekt'))
import cnc_ansichtsmodell as model

EXPECTED_NX = 'da8b4b123b93dd0e12e8f57e95840b7dbff4217d9a8fdba7264465747d356e14'
EXPECTED_HISTORY = '6790b57cc581b5db29ade50241cbb2b86e11dd1f8df444d2959ffb5a6d7f3824'
EXPECTED_PARAMETER = 'cd9a5dd5a7e224dc72ce9618862fd69c7b2536d2cb2944cf704a58e1c95940d0'


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def decimal_trig(value, cosine=False):
    # All model arguments are small; no range reduction is needed for this probe.
    x = decimal.Decimal.from_float(value)
    term = decimal.Decimal(1) if cosine else x
    result = term
    for n in range(1, 1000):
        denom = (2*n-1)*(2*n) if cosine else (2*n)*(2*n+1)
        term = -term*x*x/denom
        updated = result+term
        if updated == result:
            return float(updated)
        result = updated
    raise RuntimeError('Decimal trig failed to converge')


def leaf_diffs(a, b, path=()):
    if isinstance(a, dict):
        assert a.keys() == b.keys(), path
        for key in a:
            yield from leaf_diffs(a[key], b[key], path+(key,))
    elif isinstance(a, (list, tuple)):
        assert len(a) == len(b), path
        for i, (left, right) in enumerate(zip(a, b)):
            yield from leaf_diffs(left, right, path+(i,))
    elif a != b:
        yield path, a, b


def main():
    original_sin, original_cos = math.sin, math.cos
    set_fma = ctypes.CDLL('ucrtbase.dll')._set_FMA3_enable
    set_fma.argtypes = [ctypes.c_int]
    set_fma.restype = ctypes.c_int
    native_path = OUT.parent / 'recipe_nx310.json'
    native = json.loads(native_path.read_text(encoding='utf8'))
    params = model.load_parameters(ROOT / 'projekt/Parameter.json')
    initial = model.recipe()
    set_fma(0)
    fma0 = model.recipe()
    set_fma(1)
    fma1 = model.recipe()
    reconstructions = {}
    try:
        math.sin = lambda x: decimal_trig(x)
        math.cos = lambda x: decimal_trig(x, True)
        for precision in (70, 100):
            with decimal.localcontext() as context:
                context.prec = precision
                reconstructions[str(precision)] = model.recipe()
    finally:
        math.sin, math.cos = original_sin, original_cos
    historical = reconstructions['100']
    values = model.all_values(params)
    differences = []
    for a, b in zip(native, historical):
        assert a['id'] == b['id']
        for path, left, right in leaf_diffs(a, b):
            delta = abs(model.evaluate(left, values)-model.evaluate(right, values))
            differences.append(dict(part_id=a['id'], name=a['name'], path=list(path),
                                    native=left, historical_reconstructed=right,
                                    evaluated_absolute_delta=delta,
                                    unit='unitless' if 'direction' in path else 'mm'))
    hashes = dict(initial=digest(initial), fma0=digest(fma0), fma1=digest(fma1),
                  native_dump=digest(native), decimal70=digest(reconstructions['70']),
                  decimal100=digest(historical), parameters=digest(params))
    assert hashes['native_dump'] == hashes['fma0'] == EXPECTED_NX
    assert canonical(native) == canonical(fma0)
    assert hashes['decimal70'] == hashes['decimal100'] == EXPECTED_HISTORY
    assert hashes['parameters'] == EXPECTED_PARAMETER
    assert all(row['path'][0] == 'ops' for row in differences)
    counts = Counter((row['part_id'], row['name']) for row in differences)
    report = dict(
        date_utc=datetime.now(timezone.utc).isoformat(), baseline='6631f8b',
        current_head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        command=subprocess.list2cmdline([sys.executable, '-B', str(Path(__file__).resolve())]),
        cwd=str(Path.cwd()), environment=dict(python=sys.version, platform=platform.platform()),
        scope='Offline recipe serialization only; actual NX recipe dump compared; no geometry execution',
        exitcode=0, hashes=hashes, expected_native=EXPECTED_NX, expected_history=EXPECTED_HISTORY,
        expected_parameter=EXPECTED_PARAMETER, native_dump_path=str(native_path),
        native_dump_file_sha256=hashlib.sha256(native_path.read_bytes()).hexdigest(),
        native_fma0_canonical_bytes_equal=True, decimal70_decimal100_canonical_bytes_equal=(
            canonical(reconstructions['70']) == canonical(historical)),
        parts=len(native), operations=sum(len(d['ops']) for d in native),
        differing_leaf_count=len(differences), differing_part_count=len(counts),
        all_differences_in_ops=True,
        max_evaluated_mm_delta=max(row['evaluated_absolute_delta'] for row in differences if row['unit']=='mm'),
        max_evaluated_direction_delta=max((row['evaluated_absolute_delta'] for row in differences if row['unit']=='unitless'), default=0),
        affected_parts=[dict(part_id=k[0], name=k[1], leaf_count=v) for k,v in counts.items()],
        differences=differences,
        limitation='Historical Linux runtime not rerun. Matching historical SHA reconstructed with two independent decimal precisions. No native volume, collision, safety or release claim.',
    )
    for filename, data in [('evidence.json', report), ('recipe_historical_reconstructed.json', historical)]:
        (OUT / filename).write_bytes(json.dumps(data, indent=2, ensure_ascii=True).encode('utf8'))
    print(json.dumps({k:v for k,v in report.items() if k not in ('differences','affected_parts')}, indent=2))
    print('AFFECTED_PARTS', json.dumps(report['affected_parts']))
    print('SOURCE_UNCHANGED: no project writes; FMA3 state belongs to this disposable process.')


if __name__ == '__main__':
    main()
