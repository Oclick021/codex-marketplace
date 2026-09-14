---
name: delegate-sub-continue
description: Delegate the current request to a child subagent and continue without waiting for its report.
metadata:
  short-description: Delegate to a child agent and continue
---

# delegate-sub-continue

When the user invokes `delegate-sub-continue`, delegate the current actionable request in the conversation. Do not implement the delegated work in the caller unless separately asked. Preserve the user's requirements, context, acceptance criteria, and constraints in the handoff prompt. Require the delegate to report changes or findings, validation performed, and blockers back to the caller.

Use the collaboration subagent capability to create a child of the current task; do not create a separate Codex task. The child inherits the caller's project. Return control without waiting for the report, and retain the subagent identifier for later follow-up. The child must report its outcome to the caller.

Choose model settings by complexity without exceeding `gpt-5.6-sol` at medium reasoning. Use `gpt-5.6-luna` with low or medium reasoning for narrow work when available; use `gpt-5.6-sol` with medium reasoning for complex work. If a task appears to need more, keep this cap and divide it into bounded work or state the limitation. If the tool offers no model override, use its default and bound the scope.

For multiple items, delegate concurrently only when they do not overlap in files, state, or dependent decisions. Otherwise sequence them and pass the required outputs forward. If there is no clear actionable request, ask a concise clarification.
