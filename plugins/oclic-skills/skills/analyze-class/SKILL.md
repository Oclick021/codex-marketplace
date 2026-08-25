---
name: analyze-class
description: "Analyze an application class, service, handler, endpoint, or controller: its behavior, consumers, dependencies, and reuse opportunities. Use `--deep` to inventory and analyze the complete application-owned class and endpoint surface."
---

# AnalyzeClass

Analyze the requested application-owned class, service, handler, interface, or implementation from source evidence. The purpose is to establish what already exists before creating a new class, so the user can safely extend an appropriate existing type rather than duplicate behavior.

## Modes

- Without `--deep`, analyze only the requested type and the application-owned dependencies that materially affect its behavior.
- With `--deep`, inventory and analyze the target project's complete application-owned class and endpoint surface. Treat invocations such as `AnalyzeClass --deep` and `$analyze-class --deep` equivalently. Do not require the user to name a starting class.

### Deep discovery

When `--deep` is present:

1. Discover all source projects in the requested scope. If none is named, use the current repository and identify production, library, sample, and test projects separately.
2. List every application-owned class, record class, interface, service, handler, hosted/background worker, middleware type, controller, endpoint module, and endpoint-bearing type. Include nested and partial types; merge partial declarations under one fully qualified identity.
3. Discover the endpoint surface independently of type names: MVC/API controllers and action attributes, minimal-API `Map*` registrations, endpoint-route-builder extensions, Razor Page handlers, hubs, and other application-owned HTTP/RPC entry points demonstrated by source.
4. Record routes, verbs, authorization/anonymous attributes or policies, request/response types, registrations, and handler targets where confirmed.
5. Exclude `bin`, `obj`, vendored/third-party code, generated designer output, and generated migration/model snapshots from behavioral analysis. List important exclusions and counts so the scope is auditable. Analyze tests when they are in the repository, but classify them separately from production code.
6. Analyze every discovered application-owned type using the ordinary workflow below. Use a repository-wide visited registry so dependencies and cycles are referenced rather than repeatedly expanded.

Do not infer that a route is externally reachable merely because a method resembles an endpoint. Distinguish **Confirmed** registrations from convention-based or possible registrations.

## Discovery

Locate the requested type and inspect its complete declaration, partial declarations, base type/interfaces, constructors, injected dependencies, attributes, registrations, configuration, and all application-owned usages. For interfaces, resolve concrete registrations and implementations; distinguish established registrations from possible-but-unproven implementations.

Build both dependency directions:

- **Uses:** methods, classes, services, handlers, configuration, state, external integrations, and data stores the type depends on.
- **Used by:** direct callers/consumers, DI consumers, endpoint/component/event entry points, registrations, inheritance, and implementations.

## Recursive analysis

Maintain a visited registry keyed by fully qualified type and member signature. Before following a class or method, check the registry. On a repeat, reference the existing finding and record the cycle; never recurse indefinitely.

Analyze each behaviorally relevant method using the `method-analyze` approach: purpose, inputs/outputs, branches, side effects, error/async/security/configuration paths, and application-owned descendants. Analyze each relevant dependent class using this class-analysis approach. Do not descend into framework or third-party implementation internals.

Identify reuse candidates only from inspected evidence. For each candidate, state the overlap, the extension point or limitation, and whether reuse is **Confirmed**, **Inferred**, or **Unknown**. Do not recommend changing a class without showing why it fits the requested responsibility.

## Deliverable

Create `docs/analysis/classes/<class-name>.md` in the target project after verification. Include:

1. Purpose and responsibility.
2. Type shape: inheritance, interfaces, constructors, public API, and DI/configuration context.
3. “Used by” and “uses” maps.
4. A recursive dependency/call tree with cycles marked.
5. Method and dependent-class findings, including persistence, external systems, state, error, async, and security effects where established.
6. Reuse/extension assessment for the requested capability.
7. Source map, risks/observations, and unknowns.

Do not expose secrets or present inference as fact.

### Deep deliverable

For `--deep`, additionally create `docs/analysis/classes/index.md` containing:

1. Scope, project breakdown, totals, and exclusions.
2. A dedicated endpoint/controller table with route, verb, authorization, handler/type, source, and analysis link.
3. A complete type inventory with classification, fully qualified identity, source, and per-type analysis link.
4. Unresolved dynamic/reflection/framework-discovered usage marked **Unknown**.

Create one verified analysis document per discovered type. Use `<class-name>.md` when unique; when names collide, add the smallest stable namespace or project qualifier rather than overwriting another report.
