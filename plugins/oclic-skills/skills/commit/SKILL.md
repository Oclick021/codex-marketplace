---
name: commit
description: Review and categorize repository changes, create focused Git commits, optionally push them, or follow the repository's established deployment/versioning procedure. Use when the user invokes Commit, CommitAndPush, or CommitAndDeploy, or asks to organize current changes into meaningful commits.
---

# Commit

Turn the current repository changes into safe, meaningful commits. Treat the three command names below as invocation modes.

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

## `Commit`

Create the categorized local commit or commits using the shared workflow. Do not push.

## `CommitAndPush`

Create the categorized commit or commits, then push the current branch to its configured upstream.

- Inspect the remote and upstream before pushing.
- If no upstream exists, use the appropriate non-destructive `--set-upstream` push after confirming the intended remote from repository context.
- Never force-push.
- Report the branch, remote, and pushed commit range.

## `CommitAndDeploy`

Discover and follow the current project's established deployment procedure. Inspect applicable repository instructions, CI workflows, build/pack scripts, manifests, release configuration, and recent deployment commits before changing versions or composing the message.

- Use the project's existing version source and increment policy. Do not invent a versioning scheme.
- Update all coupled version declarations required by that procedure, and no unrelated versions.
- Include the deployment trigger marker required by the project. When the project has no different case-sensitive convention, include `[Deploy]` in the commit message.
- Categorize the functional change in the same message, for example `feat: add export workflow [Deploy]` or `fix: handle empty filters [Deploy]`.
- Run the deployment procedure's required validation, such as restore, build, tests, package validation, or changelog checks.
- Push or publish only when the established deployment procedure requires it and the `CommitAndDeploy` invocation authorizes that deployment step. State the external effect before performing it and use the normal non-force path.
- If no deployment/versioning procedure can be verified, stop after reporting what was inspected and ask the user for the missing release convention. Do not guess a version bump or trigger marker.

Finish with a compact summary of created commits, verification results, and any push or deployment action performed.
