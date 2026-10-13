# Coordinate Git mutations between agents

Use this protocol for `commit`, `commit-and-push`, `commit-and-deploy`, and `stage`, including the commit step of `DocumentCommitAndArchive`. The lock is shared in Git's common directory, so agents in the same checkout or linked worktrees coordinate without tracked lock files. It protects cooperating agents; it cannot stop editors or Git clients that do not use this protocol.

## Acquire before preparing a commit

Before modifying release/version files, staging or unstaging anything, or preparing the final commit from the index, acquire the repository lock using [commit_lock.py](../scripts/commit_lock.py). Initial read-only inspection can happen before acquiring, but refresh it after acquisition.

Generate a fresh UUID token for this workflow and retain it until release. Give `--owner` the current chat/agent identifier when available. Resolve the script relative to this skill's installed location; do not assume the target repository contains the plugin.

```text
python <commit-skill>/scripts/commit_lock.py acquire --repo <repository> --token <uuid> --owner <chat-or-agent> --wait-seconds 50
```

Only exit code 0 authorizes entering the protected section. Exit code 2 means busy: wait for the owner, give concise progress updates, and retry acquisition in bounded intervals. Do not stage or commit while waiting. Exit code 1 means a failure to resolve or operate the lock: report it and do not proceed without coordination. Pass `--git <executable>` if the environment requires a specific Git binary.

The lock uses atomic exclusive file creation, rather than a check-then-create sequence. Do not treat a repeated acquisition with your token as success; a nested workflow should reuse a lock already known to be held by its caller, without acquiring or releasing it independently.

## Protected section

- Re-read HEAD, branch, status, staged and unstaged diffs after acquiring. Another agent may have completed a commit during the wait. Recalculate the intended groups from the current state rather than using stale patches or commit assumptions.
- Hold the lock through staging, staged-diff review, required checks, all commits in the workflow, and post-commit verification. For commit-and-push/deploy, also hold it through the push or synchronous release command, so another agent cannot change the branch being published. Release after dispatch rather than holding it for remote asynchronous deployment monitoring.
- For `stage`, hold it through index changes and final verification. Staging does not reserve those changes for a later commit: the next agent must inspect and preserve unrelated staged work.
- Never include another agent's staged hunks in your commit, or unstage them to make your commit convenient. If unrelated staged work cannot be safely preserved with a precise commit, stop and resolve the scope instead of committing the whole index.
- Respect Git's own locks as well. If an uncoordinated Git operation is active, wait and refresh the state before retrying; never delete Git's `index.lock` or other native locks.

## Release and recovery

Release in cleanup after success or failure, once your Git operations have stopped:

```text
python <commit-skill>/scripts/commit_lock.py release --repo <repository> --token <same-uuid>
```

Only the owning token may release the lock. If pausing for user input, finish or stop your Git operation and release first; reacquire and refresh state when resuming. Release before archiving the chat.

Never remove another agent's lock based on age alone. The recorded owner and creation time are diagnostic information; the helper process exits after acquiring, so its process lifetime cannot establish that the owning agent finished. If the owner appears interrupted, establish that it has stopped and no Git operation remains active before arranging an explicit recovery. Otherwise leave the lock intact and report the blocker. Do not automatically steal a lock or bypass this protocol because acquisition is slow.
