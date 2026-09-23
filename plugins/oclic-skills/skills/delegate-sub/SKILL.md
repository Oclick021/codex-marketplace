---
name: delegate-sub
description: Delegate the current request to a child subagent and wait for its report.
metadata:
  short-description: Delegate to a child agent and wait
---

# delegate-sub

When the user invokes `delegate-sub`, delegate the current actionable request in the conversation. Do not implement the delegated work in the caller unless separately asked. Preserve the user's requirements, context, acceptance criteria, and constraints in the handoff prompt. Require the delegate to report changes or findings, validation performed, and blockers back to the caller.

Use the collaboration subagent capability to create a child of the current task; do not create a separate Codex task. The child inherits the caller's project. Wait for the child to finish or need input, then relay its report to the user.

Choose the highest available model generation, then use the least expensive model and reasoning level that can complete the task reliably. For the current model family, use `gpt-6-luna`, `gpt-6-sol`, and `gpt-6-astra` only with low or medium reasoning. Use `gpt-6-luna` with low reasoning for straightforward, narrow work; raise to medium only when needed. Use `gpt-6-sol` with low reasoning for routine complex work and medium when the task warrants it. Use `gpt-6-astra` with low or medium reasoning only when Luna or Sol is unlikely to handle the task reliably. Do not choose an older model when a suitable `gpt-6` model is available. If unavailable, choose the newest available Luna or Sol model that can do the job, preferring the more token-efficient option when capability is sufficient. Never exceed medium reasoning; divide work or report the limitation if additional capability is needed. If the tool offers no model override, use its default and bound the scope.

For multiple items, delegate concurrently only when they do not overlap in files, state, or dependent decisions. Otherwise sequence them and pass the required outputs forward. If there is no clear actionable request, ask a concise clarification.
