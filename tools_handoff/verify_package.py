#!/usr/bin/env python3
"""Read-only SHA-256 verification. No NX, installation, network or hardware access.

Python 3.10+. A successful result proves byte identity only, not engineering correctness.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def verify_manifest(root: Path, manifest_path: Path) -> dict:
    """Verify listed files inside root; additional files are not checked."""
    root = Path(root).resolve()
    result = {'ok': False, 'scope': 'Listed file SHA-256 identity only',
              'verified': 0, 'listed': 0, 'errors': [],
              'native_nx_executed': False, 'manufacturing_released': False}
    try:
        manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8-sig'))
        entries = manifest.get('files') if isinstance(manifest, dict) else None
        if not isinstance(entries, dict) or not entries:
            raise ValueError('Manifest needs a nonempty files dictionary')
    except (OSError, ValueError, TypeError) as exc:
        result['errors'].append({'error': 'invalid_manifest', 'detail': str(exc)})
        return result
    result['listed'] = len(entries)
    for name, expected in entries.items():
        if (not isinstance(name, str) or not name or '\\' in name or ':' in name
                or PurePosixPath(name).is_absolute()
                or '..' in PurePosixPath(name).parts):
            result['errors'].append({'path': str(name), 'error': 'unsafe_path'})
            continue
        if not isinstance(expected, str) or re.fullmatch(r'[0-9a-fA-F]{64}', expected) is None:
            result['errors'].append({'path': name, 'error': 'invalid_sha256'})
            continue
        target = root.joinpath(*PurePosixPath(name).parts)
        try:
            if not target.resolve().is_relative_to(root):
                result['errors'].append({'path': name, 'error': 'outside_root'})
            elif not target.is_file():
                result['errors'].append({'path': name, 'error': 'missing_file'})
            elif _sha256(target) != expected.lower():
                result['errors'].append({'path': name, 'error': 'hash_mismatch'})
            else:
                result['verified'] += 1
        except (OSError, RuntimeError) as exc:
            result['errors'].append({'path': name, 'error': 'read_error', 'detail': str(exc)})
    result['ok'] = not result['errors']
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--manifest', type=Path, default=None,
                        help='Relative to root, or an absolute manifest file path.')
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = args.manifest or Path('uebergabe/PAKET_MANIFEST.json')
    if not manifest.is_absolute():
        manifest = root / manifest
    result = verify_manifest(root, manifest)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
