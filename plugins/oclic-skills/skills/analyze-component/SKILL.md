---
name: analyze-component
description: "Analyze Razor components, pages, views, their consumers, methods, and class dependencies. Use `--deep` to inventory and analyze all `.razor` and `.cshtml` UI in the target project."
---

# AnalyzeComponent

Analyze the requested Razor component from source evidence. Cover its `.razor` markup, code-behind/partial class, associated styles, inherited base type, parameters, cascading values, injected services, routes, lifecycle methods, event handlers, and JavaScript interop when present.

## Modes

- Without `--deep`, analyze only the requested Razor component and the application-owned components/classes that materially affect it.
- With `--deep`, inventory and analyze the target project's complete Razor UI surface. Treat invocations such as `AnalyzeComponent --deep` and `$analyze-component --deep` equivalently. Do not require a starting component.

### Deep discovery

When `--deep` is present:

1. Discover all `.razor` and `.cshtml` files in the requested scope, including Blazor pages/components/layouts/router/host files, Razor Pages, MVC views, partial views, layouts, and view components represented by Razor markup.
2. Associate each item with application-owned `.razor.cs`, `.cshtml.cs`, partial/base classes, scoped styles, JavaScript, controllers, PageModels, view components, models, services, and endpoint/route registrations that materially affect it.
3. Classify directive/infrastructure files such as `_Imports.razor`, `_ViewImports.cshtml`, and `_ViewStart.cshtml` separately. List and analyze their shared namespace, tag-helper, layout, authorization, or import effects, but do not mislabel them as routable pages.
4. Discover routes from `@page`, Razor Page conventions, MVC controller/action view selection, areas, and application-owned endpoint mappings. Distinguish explicit routes from convention-based or unresolved routes.
5. Find consumers through component tags, partial/view rendering, layouts, navigation, controller `View`/`PartialView` calls, dynamic components, render fragments, and application-owned code. Mark unresolved dynamic view/component selection **Unknown**.
6. Exclude `bin`, `obj`, generated Razor/compiler output, and vendored/third-party UI. State exclusions and counts so the inventory is auditable.
7. Analyze every discovered UI item using the ordinary component graph and dependency workflow below, with repository-wide visited registries for UI items, classes, and methods.

## Component graph

Find where the component is used: Razor markup/tag references, routed navigation, dynamic component rendering, render fragments, layout/router use, and application-owned code that instantiates or renders it. Record unresolved dynamic usage as unknown rather than claiming full consumer coverage.

Find every nested application-owned component referenced by the markup or render tree and recursively analyze it. Maintain a visited registry keyed by component identity/path. If a component already appears in the active path or registry, record the cycle/reference and do not recurse again.

## Methods and classes

Analyze behaviorally relevant component methods using the `method-analyze` approach, especially lifecycle methods, parameter updates, event handlers, validation, navigation, data loading, state updates, disposal, and interop callbacks.

Analyze injected services, view models, state containers, component base classes, and other application-owned classes using the `analyze-class` approach. Trace only dependencies that materially affect component behavior; do not descend into framework or third-party internals.

For each result distinguish **Confirmed**, **Inferred**, and **Unknown** conclusions. Prevent infinite loops across both the component and class/method registries.

## Deliverable

Create `docs/analysis/components/<component-name>.md` in the target project after verification. Include:

1. Component purpose, route/parameters, and rendering responsibility.
2. A “used by” map and recursive nested-component tree, with cycles marked.
3. Lifecycle/event/method flow and state changes.
4. Injected/dependent classes and their relevant behavior.
5. Data, API, navigation, JavaScript, authorization, error, and async effects where demonstrated.
6. Reuse/extension guidance, source map, risks/observations, and unknowns.

Do not expose secrets or present inference as fact.

### Deep deliverable

For `--deep`, additionally create `docs/analysis/components/index.md` containing:

1. Scope, project breakdown, totals, classifications, and exclusions.
2. A complete table of `.razor` components/pages and `.cshtml` pages/views/infrastructure files, with routes, consumers, source, and analysis links.
3. Separate summaries for routed pages, reusable components/partials, layouts/hosts, MVC views, Razor Pages, and directive infrastructure.
4. Unresolved convention-based, dynamic, reflection-based, or external consumers marked **Unknown**.

Create one verified analysis document per discovered UI item. Use `<component-name>.md` when unique; when names collide, add the smallest stable folder, namespace, view, or project qualifier rather than overwriting another report. For `.cshtml` items, include PageModel/controller action flow, model binding/validation, form handlers, partial/layout relationships, and tag-helper effects where demonstrated.
