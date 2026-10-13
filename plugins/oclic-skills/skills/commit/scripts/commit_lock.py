"""Coordinate cooperating agents across a repository and its linked worktrees."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def lock_path(repo, git):
    common = subprocess.check_output(
        [git, "-C", str(repo), "rev-parse", "--git-common-dir"], text=True
    ).strip()
    return (Path(repo).resolve() / common).resolve() / "codex-agent-commit.lock"


def acquire(path, token, owner, wait):
    deadline = time.monotonic() + wait
    while True:
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            if time.monotonic() >= deadline:
                print("BUSY: another agent owns the repository commit lock.")
                return 2
            time.sleep(min(0.5, max(0, deadline - time.monotonic())))
            continue
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump({"token": token, "owner": owner, "created_at": time.time()}, stream)
                stream.flush()
                os.fsync(stream.fileno())
        except BaseException:
            path.unlink()
            raise
        print(f"ACQUIRED: {path}")
        return 0


def release(path, token):
    try:
        metadata = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("ERROR: no commit lock exists to release.", file=sys.stderr)
        return 1
    if metadata.get("token") != token:
        print("ERROR: this token does not own the commit lock.", file=sys.stderr)
        return 1
    path.unlink()
    print("RELEASED: repository commit lock.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["acquire", "release"])
    parser.add_argument("--repo", default=".")
    parser.add_argument("--git", default="git", help="Git executable or absolute path")
    parser.add_argument("--token", required=True, help="Fresh UUID retained by the owning agent")
    parser.add_argument("--owner", default="Codex agent", help="Chat/agent label for recovery")
    parser.add_argument("--wait-seconds", type=float, default=50)
    args = parser.parse_args()
    if not args.token.strip() or not 0 <= args.wait_seconds <= 55:
        parser.error("token must be nonempty and wait-seconds must be between 0 and 55")
    try:
        path = lock_path(args.repo, args.git)
        if args.action == "acquire":
            return acquire(path, args.token, args.owner, args.wait_seconds)
        return release(path, args.token)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
