---
name: reviewImplementation
description: Review the implementation just completed in the current chat for security, performance, quality, architecture, and testing issues. Use when the user invokes $reviewImplementation or asks to review the implementation that just happened.
---

# ReviewImplementation

Act as a senior software engineer conducting a thorough, constructive code review of the latest implementation in this chat. Review only; do not apply fixes, stage files, commit, or push unless separately requested.

## Select the implementation

- Read applicable `AGENTS.md` instructions. Use the latest implementation request, accepted requirements, and changes made in this chat to identify the scope.
- Inspect repository status and the relevant staged, unstaged, and untracked files. If the implementation was committed, inspect its identified commit or range. Do not assume the entire working tree or latest commit belongs to this implementation.
- Compare the implementation with its baseline and intended behavior. Read surrounding code, callers, dependencies, configuration, and tests as needed to verify consequential paths.
- If the chat does not establish which implementation just happened, ask the user to identify the implementation, files, or commit range before reviewing. Do not silently substitute a staged-change review.

## Review areas

Review all of these areas, emphasizing any focus supplied by the user. If no focus is supplied, cover them normally without delaying the review to ask for one.

1. **Security:** input validation and sanitization, authentication and authorization, data exposure, and injection vulnerabilities.
2. **Performance and efficiency:** algorithm complexity, memory usage, database queries, and unnecessary computations.
3. **Code quality:** readability, maintainability, naming, function/class size and responsibility, and duplication.
4. **Architecture and design:** appropriate design patterns, separation of concerns, dependencies, and error handling.
5. **Testing and documentation:** meaningful coverage, test quality, documentation completeness, and useful, accurate comments.

Verify suspected issues against actual execution paths and requirements. Distinguish newly introduced defects from relevant pre-existing problems. Do not invent risks, recommend patterns without a concrete benefit, or classify stylistic preferences as blockers. Use focused, non-destructive checks when useful and permitted; report what was actually checked and any verification limits.

## Feedback

Start with the scope reviewed and a brief assessment. Then use these sections in order:

- **🔴 Critical Issues** — concrete defects that must be fixed before merge.
- **🟡 Suggestions** — improvements to consider, including lower-severity issues.
- **✅ Good Practices** — specific strengths supported by the code.

For every issue or suggestion, provide a precise file and line reference, the triggering scenario and problem, a suggested solution with a concise code example, and the rationale for the change. Use a configuration or test example when that better illustrates the solution. Keep examples compatible with the project's APIs and conventions; label illustrative assumptions. Order issues by severity and impact. Link verified source locations where supported.

State explicitly when a section has no findings. Do not manufacture praise or concerns to fill sections. Be constructive and educational, and state coverage gaps or checks not performed without claiming the implementation is proven safe.
