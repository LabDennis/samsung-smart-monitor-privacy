import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'scripts/debloat.sh'

class DebloatTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = SOURCE.read_text()
        self.packages = re.search("packages='([^']+)'", source)[1].splitlines()
        self.assertEqual(len(self.packages), 17)
        # Only the fixture copy redirects device paths; the shipped script has no test bypass.
        self.script = self.root / 'debloat.sh'
        self.script.write_text(source.replace('/opt', str(self.root / 'opt')))
        self.apps = self.root / 'opt/usr/apps'
        for package in self.packages:
            (self.apps / package).mkdir(parents=True)
            (self.apps / package / 'fixture').write_text('test')
        (self.root / 'opt/usr/share/systemd/system').mkdir(parents=True)
        self.backup = self.root / 'opt/usr/share/smart-monitor-privacy/phase2'
        binpath = self.root / 'bin'
        binpath.mkdir()
        commands = {
            'id': 'echo 0',
            'systemctl': 'exit 0',
            'vconftool': 'echo "value = 1 (Int32)"',
            'pkgcmd': '''[ "$1" = -u ] || exit 0
 echo "$3" >> "$CALLS"
 [ "${FAIL_REMOVE:-}" != 1 ] || exit 1
 [ "${NO_CALLBACK:-}" != 1 ] || exit 0
 echo "pkgid[$3] key[end] val[ok]"''',
        }
        for name, body in commands.items():
            p = binpath / name
            p.write_text('#!/bin/sh\n' + body + '\n')
            p.chmod(0o755)
        self.env = dict(os.environ, PATH=str(binpath)+':'+os.environ['PATH'], CALLS=str(self.root/'calls'))

    def run_script(self, *args, **env):
        return subprocess.run(['sh', str(self.script), *args], env=dict(self.env, **env), capture_output=True, text=True)

    def apply(self, **env):
        return self.run_script('--apply', 'LS32BM700UUXEN-1720.7', **env)

    def test_preview(self):
        for args in [(), ('--apply',), ('--apply', 'wrong'), ('--apply', 'LS32BM700UUXEN-1720.7', 'extra')]:
            result = self.run_script(*args)
            self.assertEqual(result.returncode, 0)
            self.assertIn(self.packages[0], result.stdout)
            self.assertFalse(self.backup.exists())

    def test_success_and_rerun(self):
        result = self.apply()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual((self.root/'calls').read_text().splitlines(), self.packages)
        self.assertEqual(len(list(self.backup.glob('*.tar.gz'))), 17)
        self.assertEqual(len((self.backup/'SHA256SUMS').read_text().splitlines()), 17)
        self.assertEqual(len((self.backup/'created-markers.txt').read_text().splitlines()), 3)
        self.assertNotEqual(self.apply().returncode, 0)
        self.assertEqual(len((self.root/'calls').read_text().splitlines()), 17)

    def test_missing_package_stops_before_backup(self):
        folder = self.apps/self.packages[-1]
        (folder/'fixture').unlink(); folder.rmdir()
        self.assertNotEqual(self.apply().returncode, 0)
        self.assertFalse(self.backup.exists())
        self.assertFalse((self.root/'calls').exists())

    def test_archive_failure_prevents_all_removals(self):
        p = self.root/'bin/tar'; p.write_text('#!/bin/sh\nexit 1\n'); p.chmod(0o755)
        self.assertNotEqual(self.apply().returncode, 0)
        self.assertFalse((self.root/'calls').exists())

    def test_uninstall_failure_stops_after_first(self):
        self.assertNotEqual(self.apply(FAIL_REMOVE='1').returncode, 0)
        self.assertEqual((self.root/'calls').read_text().splitlines(), self.packages[:1])
        self.assertEqual(len(list(self.backup.glob('*.tar.gz'))), 17)

    def test_zero_exit_without_callback_is_failure(self):
        self.assertNotEqual(self.apply(NO_CALLBACK='1').returncode, 0)
        self.assertEqual((self.root/'calls').read_text().splitlines(), self.packages[:1])

if __name__ == '__main__':
    unittest.main()
