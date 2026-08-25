---
name: handoff
description: Transfer context or delegate bounded work between Codex tasks and projects. Use when the user asks to hand a matter to a new task, a named task or task ID, or a specialist task such as documentation, with optional asynchronous completion and reporting back to the origin.
---

# Handoff

Transfer enough verified context for another Codex task to act without rediscovering the work. Use the Codex task-coordination tools available in the current session.

## Interpret the Request

Identify:

- **destination:** a new task, exact task ID, or existing task described by project/purpose;
- **purpose:** context only, continue work, investigate, implement, review, document, or another bounded outcome;
- **return behavior:** report back, no report, wait, or dispatch asynchronously;
- **scope:** repositories, files, systems, and mutations the destination may perform.

Preserve the user's wording when it answers these points. Infer only low-risk details. If an ambiguous destination could send sensitive context to the wrong task, ask for clarification.

## Select the Coordination Mode

### New task

When the user explicitly says to hand off to a **new task**, create it in the appropriate project/workspace. Include the origin task identifier and reporting instructions in its opening message.

Creating a new task is authorized by that explicit request. Do not create one when the user merely names a role or project if a suitable existing task may be intended.

### Existing task or task ID

When the user supplies a task ID, resolve and use that exact task. When the user describes an existing task by project or purpose, list or inspect tasks and verify the destination from metadata or content. Do not rely only on a similar title. Ask the user to choose if multiple plausible tasks remain.

### Specialist task

For a destination such as a documentation, testing, security, or release task, package the current work in the form that specialty needs. Distinguish clearly between:

- documenting completed work;
- reviewing or recommending changes; and
- implementing changes in a repository the destination task owns.

Do not broaden “document this” into unrelated implementation. If the user explicitly asks the destination to document and implement what is needed, state both outcomes and their authorization boundary.

## Build the Handoff Packet

Use raw evidence and concrete references rather than unsupported conclusions. Include only fields relevant to the request:

```text
Origin task/project:
Destination task/project:
Purpose and requested outcome:
Current state and completed work:
Problem, evidence, and reproduction:
Decisions and rationale:
Relevant files, diffs, commands, artifacts, or links:
Verification already performed:
Constraints, permissions, and out-of-scope actions:
Known risks, open questions, and next step:
Return instructions and origin task ID:
```

Remove secrets, credentials, license keys, tokens, and unnecessary personal data. Do not claim unverified work is complete. Mention relevant dirty-worktree state when it could affect the destination.

The destination prompt must be self-contained and instruct the destination to report its outcome to the origin task when requested. A completion report should include outcome, evidence, changes, verification, remaining work, and blockers.

## Dispatch and Return

- **“Do not wait,” “in the background,” or equivalent:** dispatch successfully, provide the destination task reference, and return immediately. Do not call a wait mechanism. Reporting back remains the destination's responsibility if requested.
- **“Wait,” “bring back the answer,” or equivalent:** use the task wait mechanism and relay the result. Avoid busy polling.
- **No return behavior stated:** dispatch and briefly tell the user where it went. Do not wait by default.
- **Context-only handoff:** send the packet without inventing a work assignment. Confirm delivery.

When creating a user-owned task, emit the app's created-task directive in the final response if required by the task-creation tool.

## Boundaries and Failure Handling

A handoff transfers context and the user's stated authorization; it does not grant broader filesystem, deployment, publishing, messaging, or external-system permissions. Each destination task must operate within its own workspace and available tools.

If the destination cannot be found, tools are unavailable, or delivery fails, do not imply that the handoff occurred. State what failed and give the smallest action needed to proceed. If reporting back is impossible, say so in both the handoff packet and the response to the user.
