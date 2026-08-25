---
name: document
description: Persist durable application knowledge learned or implemented in the current chat into the current project's established knowledge store. Use when the user invokes /document or $document, or explicitly asks to synchronize architectural, flow, component, entity, API, integration, infrastructure, security, or decision knowledge. Do not use for ordinary code comments, API-reference generation, or broad analysis from scratch.
---

# Project Knowledge Persistence

Treat the current chat as working memory and the current repository's documented knowledge location as persistent application memory.

When invoked, read [references/workflow.md](references/workflow.md) completely, then execute it. The workflow discovers and respects repository-local conventions, performs targeted verification, updates indexes when the project uses them, and preserves safety boundaries.

Core boundary: synchronize durable knowledge already acquired in the current chat. Do not perform exhaustive repository analysis, modify application source code, or commit.
