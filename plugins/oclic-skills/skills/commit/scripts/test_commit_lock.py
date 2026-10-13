"""Exercise lock ownership and contention using separate Python processes."""

from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


SCRIPT = Path(__file__).with_name("commit_lock.py")
GIT = os.environ.get("COMMIT_LOCK_TEST_GIT", "git")


class CommitLockTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name) / "repo"
        subprocess.run([GIT, "init", str(self.repo)], check=True, capture_output=True)

    def command(self, action, token, wait=0, repo=None):
        return [sys.executable, str(SCRIPT), action, "--repo", str(repo or self.repo),
                "--git", GIT, "--token", token, "--wait-seconds", str(wait)]

    def run_lock(self, action, token, wait=0, repo=None):
        return subprocess.run(self.command(action, token, wait, repo),
                              capture_output=True, text=True, timeout=10)

    def test_atomic_contention_and_owner_release(self):
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(lambda token: self.run_lock("acquire", token),
                                        ["a", "b", "c", "d"]))
        self.assertEqual(sorted(result.returncode for result in results), [0, 2, 2, 2])
        owner = ["a", "b", "c", "d"][next(i for i, r in enumerate(results) if r.returncode == 0)]
        self.assertEqual(self.run_lock("release", "not-owner").returncode, 1)
        self.assertEqual(self.run_lock("acquire", "other").returncode, 2)
        self.assertEqual(self.run_lock("release", owner).returncode, 0)
        self.assertEqual(self.run_lock("acquire", "other").returncode, 0)

    def test_waiter_acquires_after_release(self):
        self.assertEqual(self.run_lock("acquire", "first").returncode, 0)
        waiter = subprocess.Popen(self.command("acquire", "second", wait=5),
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            time.sleep(0.5)
            self.assertIsNone(waiter.poll())
            self.assertEqual(self.run_lock("release", "first").returncode, 0)
            waiter.communicate(timeout=8)
            self.assertEqual(waiter.returncode, 0)
            self.assertEqual(self.run_lock("release", "second").returncode, 0)
        finally:
            if waiter.poll() is None:
                waiter.kill()
                waiter.communicate()

    def test_linked_worktrees_share_lock(self):
        subprocess.run([GIT, "-C", str(self.repo), "-c", "user.name=Test",
                        "-c", "user.email=test@example.invalid", "commit", "--allow-empty",
                        "-m", "initial"], check=True, capture_output=True)
        linked = Path(self.temporary.name) / "linked"
        subprocess.run([GIT, "-C", str(self.repo), "worktree", "add", "--detach", str(linked)],
                       check=True, capture_output=True)
        self.assertEqual(self.run_lock("acquire", "main").returncode, 0)
        self.assertEqual(self.run_lock("acquire", "linked", repo=linked).returncode, 2)
        self.assertEqual(self.run_lock("release", "main", repo=linked).returncode, 0)

    def test_independent_repository_is_not_blocked(self):
        other = Path(self.temporary.name) / "other"
        subprocess.run([GIT, "init", str(other)], check=True, capture_output=True)
        self.assertEqual(self.run_lock("acquire", "first").returncode, 0)
        self.assertEqual(self.run_lock("acquire", "second", repo=other).returncode, 0)


if __name__ == "__main__":
    unittest.main()
