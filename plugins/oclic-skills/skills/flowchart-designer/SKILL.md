---
name: flowchart-designer
description: Map an existing class, method, component, or application process as an editable Mermaid flowchart, or design a proposed change with the user and trace each node to its code location.
---

# flowChartDesigner

Use this skill to explain an existing application flow or design a new one with the user. Keep one `.mmd` file as the source of truth for the diagram, step IDs, code targets, and node feedback. Render the displayed diagram and any interactive preview from that file. Preserve the user's edits, annotations, and established step IDs when revising it.

## Choose the approach

### Map existing code

Inspect the implementation before drawing. Use the relevant analysis workflows from [analyze-class](../analyze-class/SKILL.md), [analyze-component](../analyze-component/SKILL.md), and [method-analyze](../method-analyze/SKILL.md):

- For a named class, component, or method, start there and follow only callers, dependencies, branches, and effects needed to explain its flow. Do not turn a focused request into a repository-wide inventory.
- For a system or process such as payments, discover its entry points and trace the relevant UI, handlers, services, registrations, persistence, external calls, and failure paths across classes and methods. Show meaningful boundaries in the chart.
- Distinguish confirmed behavior from inference or unknowns. Verify each decision, code location, and connection before presenting it as current behavior.

The flowchart is this skill's deliverable. Reuse the analysis skills' tracing methods without automatically creating their separate reports or invoking their deep modes unless the user requests those outputs.

### Design a change

For a requested feature or process change, first map the relevant current flow from code. Then propose the changed flow in the same diagram. For example, adding PayPal support requires locating the current payment entry point, provider selection, payment execution, persistence, callbacks, and error handling before placing PayPal steps.

Interview the user through the diagram: show the current flow and a concrete proposal, then ask focused questions about behavior the code cannot settle, such as routing, success and failure outcomes, refunds, or provider-specific policy. Record answers and node edits against stable step IDs. Revise and redisplay the same `.mmd` file as decisions become clear. Proceed with known parts while questions are pending; do not invent business rules.

Use yellow for existing nodes whose behavior is proposed to change and green for proposed new nodes. Keep unchanged nodes in the app theme. Include a small legend. The colors describe the proposed change relative to the inspected code, not implementation status. If the user asks to implement the design, recheck mapped code locations, translate the accepted node edits and connections into code changes, verify them, and update the chart to reflect the resulting implementation.

## Diagram

- Give every node a visible step ID and label, such as `C: Signed and registered?`.
- Label outgoing decision paths with the decision's letter: `C1: No`, `C2: Yes`, or `C1`, `C2`, `C3` for switch cases.
- Put a source reference on a second line inside every existing-code node, in the form `FileName.cs · MethodName`. Render it smaller than the main label and in readable blue against the current app theme. For a proposed node, label its intended code target as planned; never present a nonexistent method or line as verified.
- Verify each cited method, branch, full file path, and line. Make the full path and line available when the source reference is hovered. For a planned target, show the intended file/type and `planned` rather than a fabricated line.
- Use the app's background and foreground colors for nodes and text; dark mode needs dark nodes and light text.
- Keep a node-to-code map in `.mmd` comments keyed by the visible step ID. Record every relevant verified path and line for existing behavior, or the intended files/types/methods and unresolved decisions for proposed behavior. This map connects later node feedback to implementation work without changing the rendered labels.

## Interactive preview

When the display supports interaction, highlight a node's outgoing connections on hover. Right-clicking a node should open an annotation editor beside the click. Persist annotations in the `.mmd` source by the visible step ID, never by a Mermaid-generated SVG ID. Include the step ID and its annotation when sending feedback to Codex. Treat changes to connections as feedback too; resolve their affected code targets before implementation.

If the display supports opening local source files, open the referenced file at its cited line. Otherwise provide a working Codex file link or clearly label an action that requests Codex to open it. Do not present an `Open file` control that only sends an unexplained message.

If the display cannot support a requested interaction, keep the diagram usable and provide the corresponding source references and annotations in a readable fallback. Do not claim that unavailable interactions work.

## Workflow

1. Select the focused-code, system-process, or change-design approach and trace the relevant current behavior.
2. Write or update the `.mmd` source, preserving user edits and stable step IDs. Mark proposed edits yellow and additions green when designing a change.
3. Render from that same source. Add the supported interactive behavior above.
4. Compare rendered labels with the `.mmd` file; check annotation-to-step and step-to-code mappings, and confirm that existing-code references point to real lines.
5. Show the diagram and link its editable `.mmd` source. Apply later feedback to that same file and render it again.
