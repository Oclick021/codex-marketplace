---
name: stage
description: Review current Git changes, group related files or hunks by purpose, and stage coherent changes without committing. Use when the user invokes Stage or asks to prepare related changes for a commit.
---

# Stage

Review the current repository changes, identify which pieces belong together, and stage each coherent group. Do not create a commit, push, or deploy.

## Workflow

1. Read applicable `AGENTS.md` files. Inspect the repository root, current branch, `git status`, staged and unstaged diffs, and recent history when it helps explain the changes.
2. Review changed files and hunks to understand their purpose and dependencies. Group changes that implement the same feature, fix, documentation update, or other purpose. Keep tightly coupled changes together and separate independently reviewable work.
3. Preserve changes already staged by the user. Do not unstage, overwrite, discard, or modify existing staged or unstaged changes.
4. Exclude unrelated user work, generated artifacts, build outputs, and files that appear to contain credentials, tokens, connection strings, or customer data. Do not stage suspicious or ambiguous content; report it.
5. Stage only the intended files or patch hunks for each group. Use interactive patch staging or an equivalent precise method when a file contains both related and unrelated edits.
6. Review the staged diff and run `git diff --cached --check`. Confirm that every staged file or hunk belongs to a group and that unrelated changes remain unstaged.
7. Report the groups staged, their files or hunks, any related changes left unstaged and why, and the final staged/unstaged status. If changes cannot be grouped safely without a product decision, explain the ambiguity and ask before staging the uncertain portions.

Do not commit, push, deploy, amend, rebase, reset, or bypass hooks.
