---
name: delegate-continue
description: Delegate the current request to a separate Codex task in the caller project and continue without waiting for its report.
metadata:
  short-description: Delegate to a separate task and continue
---

# delegate-continue

When the user invokes `delegate-continue`, delegate the current actionable request in the conversation. Do not implement the delegated work in the caller unless separately asked. Preserve the user's requirements, context, acceptance criteria, and constraints in the handoff prompt. Require the delegate to report changes or findings, validation performed, and blockers back to the caller.

Create a separate Codex task using exactly the caller's project ID and the project's standard environment. If the caller is projectless, keep the task projectless; never use a different project. Return control without waiting for the report. Give the user the new task identifier and status. The task prompt must ask the agent to report its result to the caller. Do not create a child subagent for this mode.

Choose model settings by complexity without exceeding `gpt-5.6-sol` at medium reasoning. Use `gpt-5.6-luna` with low or medium reasoning for narrow work when available; use `gpt-5.6-sol` with medium reasoning for complex work. If a task appears to need more, keep this cap and divide it into bounded work or state the limitation. If the tool offers no model override, use its default and bound the scope.

For multiple items, delegate concurrently only when they do not overlap in files, state, or dependent decisions. Otherwise sequence them and pass the required outputs forward. If there is no clear actionable request, ask a concise clarification.
