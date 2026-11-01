from pathlib import Path
import subprocess, json, hashlib, datetime, sys

root = Path(__file__).resolve().parents[3]
audit = Path(__file__).resolve().parent
records = []
for name, args, cwd, scope in [
    ('pytest_final', ['-m', 'pytest', '-q', '-p', 'no:cacheprovider'], root/'projekt', 'Active offline suite; no native NX proof'),
    ('handoff_final', ['-m', 'unittest', 'discover', '-s', 'tools_handoff', '-p', 'test_*.py', '-v'], root, 'Handoff helper tests'),
    ('package_original_final', ['tools_handoff/verify_package.py'], root, 'Original handoff manifest, deliberate subsequent changes expected'),
]:
    command = [sys.executable] + args
    start = datetime.datetime.now().astimezone().isoformat()
    result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (audit/f'{name}.stdout.txt').write_bytes(result.stdout)
    records.append(dict(name=name, date=start, command=command, cwd=str(cwd),
        environment=f'Windows {sys.version}', source_base='e87f522', source_snapshot='native_source_hashes.json',
        scope=scope, exitcode=result.returncode, raw_log=f'{name}.stdout.txt'))
    print(name, 'exit=', result.returncode, flush=True)
    if name != 'package_original_final' and result.returncode:
        raise SystemExit(result.returncode)

sources = json.loads((audit/'native_source_hashes.json').read_text(encoding='utf-8-sig'))
for row in sources:
    assert hashlib.sha256((root/row['path']).read_bytes()).hexdigest().upper() == row['sha256'].upper(), row['path']
parameters = json.loads((audit/'parameter_vorher.json').read_text(encoding='utf-8-sig'))
print('Source snapshot matches active native input files.', flush=True)
(audit/'verification_final.meta.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
