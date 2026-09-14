---
name: delegate
description: Delegate the current requested work to another Codex agent when the user invokes a $delegate variant; choose separate-task or subagent execution, bounded model settings, and synchronous or continuing handoff.
metadata:
  short-description: Delegate work to another Codex agent
---

# Delegate

When the user invokes `$delegate`, treat the work currently requested in the conversation as an instruction to hand off. Do not implement that delegated work in the caller unless the user separately asks for caller-side work. Preserve the user's requirements, relevant context, acceptance criteria, and known constraints in the delegate prompt. The delegate must return a concise report to the caller with what it changed or found, validation performed, and anything still blocked or uncertain.

## Invocation modes

Recognize these exact forms, including when followed by a task description:

- `$delegate`: launch a separate Codex task/agent and wait for its report before returning the delegated result.
- `$delegate-continue`: launch a separate task, then return control to the user without waiting. Keep the task identifier so it can be checked or continued later.
- `$delegate-sub`: launch a child subagent within the current task and wait for its report.
- `$delegate-sub-continue`: launch a child subagent and return control without waiting; retain its identifier for later follow-up.

A more specific variant takes precedence over `$delegate`. If the user invokes `$delegate` without a new description, delegate the latest actionable request in the conversation. Ask a concise clarification only if there is no clear work item or essential requirements are missing.

For any separate-task variant, create the task under exactly the same Codex project as the caller by reusing the caller's project ID and the project's standard environment. If the caller is projectless, keep the new task projectless. Never select a different project. Subagent variants stay within the caller's task and therefore inherit its project.

Use the available Codex task/thread creation capability for separate-task variants and the collaboration subagent capability for `-sub` variants. Do not silently substitute one type for the other. Include an explicit instruction in the delegate prompt to report results back to the caller. For waiting variants, wait for completion or a request for input, then relay the report. For `-continue` variants, launch successfully, give the user the task/agent identifier and a brief status, and do not block the user's ongoing conversation; follow up only when the user asks or when the platform delivers a report.

## Model and work allocation

Choose settings by complexity, while never exceeding `gpt-5.6-sol` at medium reasoning:

- Straightforward, narrow work: use `gpt-5.6-luna` with low or medium reasoning when available.
- Multi-file implementation, nuanced analysis, or work with meaningful integration concerns: use `gpt-5.6-sol` with medium reasoning.
- If the task appears to need more capability, still cap it at `gpt-5.6-sol` and medium reasoning; divide it into bounded work items or identify the limitation in the handoff. Never select a higher model or reasoning effort.
- If a tool offers only a default model and no supported override, use that tool's default rather than inventing an unsupported setting, and keep the prompt/task scope appropriately bounded.

For several independent work items, delegate them concurrently when they do not touch overlapping files, shared state, or dependent decisions. Give each agent a clear ownership boundary. If work has dependencies or likely collisions, sequence it: tell later agents what output to wait for and pass along the necessary result before they proceed. Avoid parallel work that would cause conflicting edits. The caller remains responsible for integrating reports and identifying conflicts; do not redo delegated implementation unless the user requests it or integration requires a specific caller-side fix.

When the available platform cannot create the requested agent type, explain that limitation and use the closest available delegation mechanism only if it preserves the requested distinction; otherwise report the block rather than doing the work yourself.
