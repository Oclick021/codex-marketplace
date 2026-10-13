---
name: DocumentCommitAndArchive
description: Run the oclic-skills document workflow, then create local commits with the commit workflow, then archive the current chat after successful completion. Use when the user invokes $DocumentCommitAndArchive or requests this complete sequence. Creating or editing this skill does not invoke the sequence.
---

# DocumentCommitAndArchive

Complete the current chat's work in this order: document, commit, archive. Invoking this skill authorizes all three steps for the current chat and its requested repository work; do not ask for the same authorization again. Do not push or deploy.

## Workflow

1. Read and execute the bundled [document skill](../document/SKILL.md), including its referenced workflow. Persist durable knowledge from the current chat into the project's established documentation store and complete its validation. Its prohibition on committing applies to this documentation step; the next step performs the commits.
2. After documentation succeeds, read and execute the bundled [commit skill](../commit/SKILL.md). Include documentation changes and the implementation changes belonging to the current chat's requested work, grouped according to that skill. Preserve unrelated changes. Verify the resulting commits and complete the required checks.
3. Confirm that no in-scope documentation, commit work, or required verification remains incomplete. A successful documentation no-op or an already committed implementation is acceptable; do not create an empty commit. Unrelated worktree changes do not prevent archiving.
4. Give a concise progress update with documentation results, commit hashes and subjects (or why no new commit was needed), and verification results. Then archive the calling chat using `mcp__codex_app__set_thread_archived` with `{"archived": true}` and no `threadId`, so it targets this chat. Discover the tool if it is deferred. Do not archive other chats or remove worktrees.
5. Check the archive tool result. Report the completed sequence and archive status concisely; claim archiving succeeded only when the tool confirms it.

## Incomplete steps

If documentation or committing fails, a required check fails, or a material scope question needs an answer, stop before archiving and report what completed and what remains. Keep the chat available for resolving the issue. If a required skill or the archive tool is unavailable, report the missing capability; do not invent a replacement operation or claim success. If archiving fails after the commits succeeded, preserve those commits and report the archive failure without repeating the preceding steps.
