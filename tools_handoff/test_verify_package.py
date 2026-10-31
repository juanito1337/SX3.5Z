"""Tests only the handoff checker, NOT the machine or NX."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from verify_package import verify_manifest


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.payload = self.root / 'projekt' / 'probe.txt'
        self.payload.parent.mkdir()
        self.payload.write_text('Original\n', encoding='utf-8')
        self.manifest = self.root / 'manifest.json'
        self.data = {'files': {'projekt/probe.txt': hashlib.sha256(self.payload.read_bytes()).hexdigest()}}
        self.save()

    def tearDown(self):
        self.tmp.cleanup()

    def save(self):
        self.manifest.write_text(json.dumps(self.data), encoding='utf-8')

    def test_identical_file_passes(self):
        result = verify_manifest(self.root, self.manifest)
        self.assertTrue(result['ok'])
        self.assertEqual(result['verified'], 1)
        self.assertFalse(result['native_nx_executed'])

    def test_changed_file_fails(self):
        self.payload.write_text('geändert', encoding='utf-8')
        self.assertFalse(verify_manifest(self.root, self.manifest)['ok'])

    def test_missing_file_fails(self):
        self.payload.unlink()
        self.assertFalse(verify_manifest(self.root, self.manifest)['ok'])

    def test_unsafe_paths_fail(self):
        for path in ('../outside.txt', '/tmp/outside.txt', 'C:/outside.txt', 'projekt\\x.txt'):
            with self.subTest(path=path):
                self.data = {'files': {path: '0' * 64}}
                self.save()
                self.assertFalse(verify_manifest(self.root, self.manifest)['ok'])

    def test_bad_hash_fails(self):
        self.data['files']['projekt/probe.txt'] = 'NOT_A_SHA256'
        self.save()
        self.assertFalse(verify_manifest(self.root, self.manifest)['ok'])

    def test_invalid_json_fails(self):
        self.manifest.write_text('{', encoding='utf-8')
        self.assertFalse(verify_manifest(self.root, self.manifest)['ok'])

    def test_empty_manifest_fails(self):
        self.data = {'files': {}}
        self.save()
        self.assertFalse(verify_manifest(self.root, self.manifest)['ok'])

    def test_directory_instead_of_file_fails(self):
        self.payload.unlink()
        self.payload.mkdir()
        self.assertFalse(verify_manifest(self.root, self.manifest)['ok'])

    def test_checker_does_not_change_payload(self):
        before = self.payload.read_bytes()
        verify_manifest(self.root, self.manifest)
        self.assertEqual(before, self.payload.read_bytes())

    def test_symlink_outside_root_fails(self):
        with tempfile.TemporaryDirectory() as other:
            p = Path(other) / 'target.txt'
            p.write_text('Original\n', encoding='utf-8')
            self.payload.unlink()
            try:
                self.payload.symlink_to(p)
            except OSError:
                self.skipTest('Symlinks unavailable on this platform')
            self.assertFalse(verify_manifest(self.root, self.manifest)['ok'])


if __name__ == '__main__':
    unittest.main()
