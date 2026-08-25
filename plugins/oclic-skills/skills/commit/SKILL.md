---
name: commit
description: Review and categorize repository changes and create focused local Git commits without pushing or deploying. Use when the user invokes Commit or asks to organize current changes into meaningful local commits.
---

# Commit

Turn the current repository changes into safe, meaningful local commits. Do not push or deploy.

## Shared workflow

1. Read the repository's applicable `AGENTS.md` files and inspect `git status`, the current branch, staged and unstaged diffs, and recent commit-message conventions.
2. Identify generated files, build outputs, credentials, tokens, connection strings, customer data, and unrelated user changes. Never commit secrets or generated artifacts that the repository excludes. Preserve unrelated work.
3. Group changes by functional purpose and dependency. Prefer separate commits when changes can be reviewed or reverted independently; keep tightly coupled implementation, tests, and required configuration together.
4. Categorize each group with the repository's convention. If none exists, use an appropriate Conventional Commit type:
   - `feat`: new user-visible or developer-facing functionality
   - `fix`: bug correction
   - `docs`: documentation-only changes
   - `refactor`: behavior-preserving restructuring
   - `test`: test-only additions or corrections
   - `perf`: performance improvement
   - `build`: build system, dependencies, packaging, or versioning
   - `ci`: continuous-integration or delivery configuration
   - `style`: formatting-only changes
   - `chore`: maintenance that fits no more specific category
5. Use a concise imperative subject that describes the outcome. Add a body only when motivation, compatibility, migration, or non-obvious behavior needs explanation.
6. Stage only the files or patch hunks belonging to the current group. Review the staged diff and run `git diff --cached --check` before committing.
7. Run proportionate verification before the final commit or push. Follow repository-specific build and test instructions. Report failures; do not conceal them with an unrelated commit.
8. After each commit, verify its contents and show the user the resulting commit hash and subject. Never amend, rebase, reset, force-push, or bypass hooks unless the user explicitly requests it.

If changes overlap so heavily that safe grouping requires a product decision, explain the ambiguity and ask before staging. Do not assume that every dirty-worktree change belongs to the requested work.

Finish with a compact summary of created commits and verification results.
