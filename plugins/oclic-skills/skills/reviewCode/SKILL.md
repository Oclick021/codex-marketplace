---
name: reviewCode
description: Review code identified by the user's prompt for security, performance, quality, architecture, and testing issues. Use when the user invokes $reviewCode or requests a targeted code review; ask which code if no target is identified.
---

# ReviewCode

Act as a senior software engineer conducting a thorough, constructive code review of code selected by the user. Review only; do not apply fixes, stage files, commit, or push unless separately requested.

## Select the code

- Use the target described after `$reviewCode` or otherwise clearly selected by the user: a snippet, file, method, class, component, directory, diff, commit range, or pull request.
- If no target is identified, ask: "Which code should I review? You can provide a file, method/class, directory, snippet, commit range, or PR." Wait for the answer before reviewing; do not assume staged changes or the latest implementation is the target.
- Resolve clear references from the conversation. If several targets fit and the choice changes the review materially, ask for clarification.
- Read applicable `AGENTS.md` instructions. Inspect the selected code and relevant callers, dependencies, configuration, and tests. For a diff or PR, compare against its actual baseline; for existing code, review its current behavior. Keep supporting investigation tied to the selected scope.

## Review areas

Review all of these areas, emphasizing any focus supplied by the user. If no focus is supplied, cover them normally without delaying the review to ask for one.

1. **Security:** input validation and sanitization, authentication and authorization, data exposure, and injection vulnerabilities.
2. **Performance and efficiency:** algorithm complexity, memory usage, database queries, and unnecessary computations.
3. **Code quality:** readability, maintainability, naming, function/class size and responsibility, and duplication.
4. **Architecture and design:** appropriate design patterns, separation of concerns, dependencies, and error handling.
5. **Testing and documentation:** meaningful coverage, test quality, documentation completeness, and useful, accurate comments.

Verify suspected issues against actual execution paths and requirements. For change reviews, distinguish introduced defects from relevant pre-existing problems. Do not invent risks, recommend patterns without a concrete benefit, or classify stylistic preferences as blockers. Use focused, non-destructive checks when useful and permitted; report what was actually checked and any verification limits.

## Feedback

Start with the scope reviewed and a brief assessment. Then use these sections in order:

- **🔴 Critical Issues** — concrete defects that must be fixed before merge.
- **🟡 Suggestions** — improvements to consider, including lower-severity issues.
- **✅ Good Practices** — specific strengths supported by the code.

For every issue or suggestion, provide a precise file and line reference, the triggering scenario and problem, a suggested solution with a concise code example, and the rationale for the change. Use a configuration or test example when that better illustrates the solution. Keep examples compatible with the project's APIs and conventions; label illustrative assumptions. Order issues by severity and impact. Link verified source locations where supported. For pasted snippets, use snippet line numbers without inventing a file path.

State explicitly when a section has no findings. Do not manufacture praise or concerns to fill sections. Be constructive and educational, and state coverage gaps or checks not performed without claiming the code is proven safe.
