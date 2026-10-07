import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import package_maintenance


class MaintenancePackageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.patch = patch.object(package_maintenance, 'ROOT', self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        (self.root / '.local/autonomy').mkdir(parents=True)
        (self.root / 'integration').mkdir()
        (self.root / 'data').mkdir()
        (self.root / 'integration/repository-updates.md').write_text('# Public notes\n')
        (self.root / 'data/table-dispositions.json').write_text('{}\n')
        (self.root / '.local/autonomy/private-packets.json').write_text('private evidence')
        self.manifest = self.root / '.local/autonomy/changed-files.json'

    def test_only_public_files_and_manifest_cross_the_job_boundary(self):
        self.manifest.write_text(json.dumps(['integration/repository-updates.md']))
        count = package_maintenance.package(Path('.local/maintenance-candidate'), True)
        self.assertEqual(count, 2)
        output = self.root / '.local/maintenance-candidate'
        self.assertEqual(sorted(p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()), [
            '.local/autonomy/changed-files.json', 'data/table-dispositions.json', 'integration/repository-updates.md'])

    def test_private_and_unmanaged_paths_are_rejected_before_copying(self):
        for value in ['.local/autonomy/private-packets.json', 'server/autonomy.mjs', '../private.md', '/tmp/private.md']:
            with self.subTest(value=value):
                self.manifest.write_text(json.dumps([value]))
                with self.assertRaises(ValueError):
                    package_maintenance.package(Path('.local/maintenance-candidate'))
                self.assertFalse((self.root / '.local/maintenance-candidate').exists())

    def test_symlinks_cannot_turn_public_paths_into_private_exports(self):
        (self.root / 'integration/leak.md').symlink_to(self.root / '.local/autonomy/private-packets.json')
        self.manifest.write_text(json.dumps(['integration/leak.md']))
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            package_maintenance.package(Path('.local/maintenance-candidate'))

    def test_staging_cannot_replace_the_ledger_or_another_directory(self):
        self.manifest.write_text('[]')
        for output in ['.local/autonomy', '.local/autonomy/maintenance-packets', 'integration/maintenance-notes', '../maintenance-outside']:
            with self.subTest(output=output), self.assertRaises(ValueError):
                package_maintenance.package(Path(output))
        self.assertTrue((self.root / '.local/autonomy/private-packets.json').exists())
