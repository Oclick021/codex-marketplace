---
name: review_staged
description: Review staged Git changes for bugs, regressions, security issues, and missing coverage. Use when the user invokes review_staged or asks for a review of staged changes.
---

# ReviewStaged

Review the current Git index for concrete defects and risks in the changes that would be included in the next commit. This is a read-only code review. Do not edit, stage, unstage, commit, or push anything.

## Workflow

1. Read applicable `AGENTS.md` files. Inspect `git status`, the staged file list, and the staged diff (`git diff --cached`). Review unstaged or untracked changes only when needed to understand context, and never treat them as part of the staged change.
2. Read relevant surrounding code, callers, configuration, and tests to verify how the staged changes behave. Trace consequential paths far enough to establish each suspected issue.
3. Look for demonstrable bugs, behavior regressions, security or data-integrity problems, compatibility risks, and important missing test coverage introduced by the staged changes. Ignore purely stylistic preferences and pre-existing issues unless the staged diff makes them relevant.
4. Validate findings against the exact staged patch and source. Report only actionable issues with a clear failure scenario, affected location, and concise explanation. Include severity when useful, using P1 for urgent, P2 for normal priority, and P3 for lower priority.
5. Do not modify files or run tests unless the user separately asks for fixes or testing. If a read-only check helps confirm a finding, state what was checked and its result.

## Response

List findings first, ordered by severity. For each finding, include a short title, severity, file and line, the triggering conditions, and the resulting problem. If no actionable issues are found, state that clearly and mention any meaningful scope or verification limits. Do not pad the review with speculative concerns.
