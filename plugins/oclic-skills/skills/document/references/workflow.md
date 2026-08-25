# `/document` workflow

## Outcome

Persist durable project knowledge already acquired in the current chat. This is knowledge synchronization, not a new exhaustive analysis and not a conversation transcript.

Use the entire available current conversation as the primary source. Knowledge can be valuable even when no corresponding source file appears in `git diff`.

## 1. Discover the project's knowledge system

Read the repository's applicable `AGENTS.md` files and inspect only likely documentation locations and indexes. Prefer an explicitly documented knowledge store, taxonomy, templates, naming rules, and validation commands.

If the repository defines a knowledge system, follow it exactly. For example, a repository may use `Silver.Knowledge/`, architecture decision records, or another indexed documentation tree.

If no knowledge system is defined:

- Reuse an existing `docs/knowledge/`, `docs/architecture/`, or ADR structure when its purpose is clear.
- Otherwise use `docs/knowledge/` and maintain a concise `index.md` linking the documents created by this skill.
- Use descriptive kebab-case filenames. Do not invent a complex ID taxonomy, schema, or template merely for consistency with another project.

Do not create a second competing knowledge store.

## 2. Extract durable knowledge

Identify what the chat established, created, changed, or clarified, including meaningful execution flows, method relationships, persistence, integrations, background processing, authentication, configuration, errors and retries, infrastructure, and architectural roles.

Do not persist brainstorming, rejected approaches, temporary guesses, casual discussion, transient command output, reverted attempts, syntax questions, or speculation. Compilation failures belong only when they establish durable architectural behavior.

## 3. Consult existing knowledge progressively

Read the relevant index or navigation file first when one exists. Locate documents by titles, IDs, paths, and tags. Do not load the entire documentation tree. Read only documents that may need updating.

Classify every durable finding as:

- `EXISTING-CORRECT`: already accurate; do nothing.
- `EXISTING-NEEDS-UPDATE`: make a targeted update to affected sections.
- `NEW-KNOWLEDGE`: create an appropriate document or knowledge node.
- `NO-DOCUMENTATION-NEEDED`: too trivial, temporary, or implementation-specific; do nothing.
- `UNCERTAIN`: verify narrowly when practical; otherwise omit it or preserve uncertainty explicitly if the project's conventions support that.

Preserve correct human-written content. Never regenerate whole documents merely to change wording.

## 4. Verify important claims

Use targeted source inspection only when needed to verify exact source references or important claims such as method relationships, database writes, external calls, dependency-injection resolution, security, background work, branches, retries, or newly implemented behavior. Do not redo a complete trace when the conversation already established it.

Source code is the current implementation truth. If it conflicts with knowledge, trust the code and follow the project's convention for stale or unresolved documentation. If none exists, state the discrepancy explicitly.

## 5. Classify and organize knowledge

Use the repository's established taxonomy. When none exists, choose the smallest useful category: architecture, flows, components, important entities, APIs, integrations, infrastructure, security, or established architectural decisions.

Recursive method traces normally become one flow document covering the entry point, chronological execution, relevant call tree and branches, data operations, integrations, async boundaries, errors, retries, configuration, risks, and source map. Do not create one document per method.

For implemented features, document the code's architectural role and behavioral effect rather than merely listing changed files or classes. Never invent historical rationale for a decision.

## 6. Maintain metadata and navigation

Follow the project's conventions and matching templates. Search existing navigation before creating anything. Reuse established IDs and choose new IDs only when the project requires them.

Update the project's indexes, source indexes, relationship metadata, and navigation only where its conventions require them. For the fallback `docs/knowledge/` structure, add each created document to `docs/knowledge/index.md` with a one-sentence description.

Add only established relationships. Include exact source paths and symbols whenever practical so future readers can navigate from knowledge to implementation.

## 7. Boundaries

This operation may modify only the discovered knowledge/documentation store and its navigation or indexes. It must not modify application source code. If source inconsistencies are found, document what can safely be established and report the inconsistency without fixing it.

Never write secrets, credentials, tokens, connection strings, customer data, large source dumps, or speculative claims. Do not commit.

## 8. Validate before finishing

Run any repository-defined documentation validation that is relevant and safe. Also check that:

1. New filenames or IDs are unique.
2. Frontmatter and indexes use valid syntax when present.
3. Every new document is reachable from the relevant index or navigation.
4. Referenced documents and source files exist.
5. Relative links resolve.
6. No secret or speculative content was added.
7. Existing correct documentation was preserved.
8. Application source was not modified by this operation.

## 9. Completion response

Respond concisely with the documents created or updated, navigation/index changes, and the durable knowledge captured. State that application code was not modified and no commit was created.

If nothing needs persistence, state that the project's durable documentation is already consistent with the knowledge from this conversation and that no documentation changes were necessary.
