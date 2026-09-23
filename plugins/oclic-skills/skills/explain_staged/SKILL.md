---
name: explain_staged
description: Explain what is currently staged in Git, how each change works, and how staged pieces relate. Use when the user invokes explain_staged or asks for an explanation of staged changes.
---

# ExplainStaged

Explain the current Git index: the changes that would be included in the next commit. This is a read-only analysis. Do not stage, unstage, edit, commit, or push anything.

## Workflow

1. Read applicable `AGENTS.md` files. Inspect `git status`, the staged file list, and the staged diff (`git diff --cached`). Keep unstaged and untracked changes out of the explanation unless they clarify context; label them clearly as unstaged.
2. Read the relevant surrounding source and configuration so the explanation describes behavior, not just line-by-line edits. Follow directly related call paths or dependencies where needed to explain how a change works.
3. Group staged files and hunks by feature, behavior, or dependency. Explain how the groups fit together and identify the likely entry point and resulting behavior when supported by the source.
4. For each group, describe the purpose, important changes, how data or control flows, and any observable side effects or configuration. Link claims to file and line locations where available.
5. Separate confirmed behavior from inference and unknowns. Do not claim execution or runtime outcomes that source inspection does not establish.
6. If the index is empty, say that no staged changes are present and offer a brief summary of the unstaged changes only if useful.

## Response

Start with a concise summary of what the staged change accomplishes. Then explain the related groups in a logical order, from entry point through important behavior and dependencies. End with relevant limitations or open questions. Keep the explanation proportionate to the size of the staged diff.
