---
name: commit-and-push
description: Review and categorize repository changes, create focused Git commits, and push the current branch safely to its upstream. Use when the user invokes CommitAndPush or explicitly asks to commit current changes and push them.
---

# CommitAndPush

Create meaningful commits from the current repository changes and push them safely.

## Workflow

1. Read applicable `AGENTS.md` files. Inspect `git status`, the current branch, staged and unstaged diffs, remotes, upstream configuration, and recent commit-message conventions.
2. Exclude generated files, build outputs, secrets, customer data, and unrelated user changes. Never assume every dirty-worktree change belongs to the requested work.
3. Group changes by functional purpose and dependency. Keep tightly coupled implementation, tests, and required configuration together; separate work that can be reviewed or reverted independently.
4. Follow the repository's commit convention. If none exists, categorize each group with an appropriate Conventional Commit type such as `feat`, `fix`, `docs`, `refactor`, `test`, `perf`, `build`, `ci`, `style`, or `chore`.
5. Stage only each group's files or patch hunks. Review the staged diff and run `git diff --cached --check` before committing.
6. Run proportionate repository-required verification. Report failures and do not conceal them with an unrelated commit.
7. Create concise imperative commit subjects. Add a body only for important motivation, compatibility, migration, or non-obvious behavior.
8. Verify the created commits, then push the current branch to its configured upstream.

## Push safety

- Inspect the remote and upstream immediately before pushing.
- If no upstream exists, determine the intended remote from repository context and use a normal `--set-upstream` push.
- Never force-push, rewrite history, bypass hooks, amend, rebase, or reset unless the user explicitly requests it.
- If the remote advanced and rejects the push, fetch and inspect the divergence. Do not merge or rebase automatically when doing so could affect another contributor's work.

Finish by reporting commit hashes and subjects, verification results, the remote branch, and the pushed commit range.
