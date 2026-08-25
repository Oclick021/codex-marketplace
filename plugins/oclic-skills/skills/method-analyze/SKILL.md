---
name: method-analyze
description: "Trace an application-owned method recursively and produce evidence-based flow documentation. Use when the user asks to analyze a method, class method, or project/class/method execution flow."
---

# AnalyzeMethod

Produce an evidence-based, recursive code-flow analysis for the requested entry point. Work from source and configuration actually inspected; label conclusions as **Confirmed**, **Inferred**, or **Unknown**.

## Invocation

Accept these input forms, treating `/MethodAnalyze`, `/MethodAnaylze`, `MethodAnalyze`, and `AnalyzeMethod` as equivalent requests:

- `method name` — locate it in the current project; disambiguate only if more than one candidate materially fits.
- `class then method name` — locate the method in that class.
- `project name then class then method name` — start in the named project.

Method names may include parentheses. If the supplied name remains ambiguous after searching source, ask for the namespace or signature before tracing.

Append `--full` to any form to enable Full mode. For example: `/MethodAnalyze Silver.Services ControllerService GetSbelAsync --full`.

## Analysis workflow

1. Read the entry method, containing type, constructor dependencies, relevant interfaces/base types/attributes, registrations, configuration, and callers needed for context.
2. Build a call tree of relevant application-owned methods and recursively inspect meaningful branches. Keep a visited-method registry; document cycles rather than re-entering them.
3. Trace dependencies through dependency-injection registrations. If the concrete implementation cannot be established, say so.
4. Record database reads/writes, external calls, file/cache/session/static-state changes, security checks, configuration, errors, retries, timeouts, cancellation, and asynchronous or queued handoffs.
5. Stop at framework and third-party internals unless their implementation is necessary to establish application behavior. Do not invent database names, integrations, or business rules.

Use a maximum depth of 12 and 500 unique application methods in normal mode. If either limit is reached, record exactly what remains unexplored.

When independent branches are substantial, delegate their analysis in parallel when subagents are available. Consolidate their findings into one coherent flow rather than concatenating reports.

## Full mode (`--full`)

In Full mode, trace every reachable, relevant application-owned child method and configuration/runtime item that materially affects the entry point. Do not stop at the normal depth or method-count safeguards; still detect cycles, avoid framework and third-party implementation internals, and state any unavoidable platform or source-access limit.

Use the available subagent capacity to analyze independent child methods and branches. A parent agent must:

1. Assign each independently traceable child branch to a child agent where capacity permits.
2. Require that child to recursively delegate its own independent descendants in the same manner.
3. Receive structured child reports, verify their source evidence, synthesize them, and report the synthesized result to its parent.
4. Queue remaining independent branches as agents become available rather than silently omitting them. Analyze a branch directly only when it cannot be independently delegated or subagent capacity is unavailable.

Each agent report to its parent must include: method/type, purpose, callers, inputs/outputs, application-owned calls, dependencies, database reads/writes, external calls, state changes, branches, error paths, async/concurrency, security, configuration, source evidence, explored descendants, cycles, and unresolved unknowns. Parents must reconcile duplicates and shared descendants before reporting upward.

After the main parent completes its final synthesis and creates the flow document, ask the user whether they want to use the `document` skill to persist the confirmed architectural knowledge. Do not invoke that skill or write to the project's durable knowledge store unless the user explicitly agrees.

## Deliverable

After a final verification pass against the entry method and major branches, create `docs/flows/<flow-name>.md` in the target project. Use a clear flow-name derived from the entry point.

Include:

1. Executive summary and entry-point context (route/event, inputs, output, authorization when applicable).
2. An ASCII high-level flow diagram and complete relevant call tree.
3. Chronological detailed flow and a decision tree for behavior-changing branches.
4. Database interactions, external integrations, and background/asynchronous boundaries.
5. Error handling, security, configuration, and dependency mappings.
6. A source map with file and method references.
7. Code-supported risks/observations, clearly separated from factual flow documentation.
8. Unknowns and analysis limits.

Avoid copying source wholesale. Cite exact files, types, and methods so every factual conclusion can be verified. Never expose secret values.
