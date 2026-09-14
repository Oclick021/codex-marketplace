# Oclic Skills for Codex

This repository is a Codex plugin marketplace containing the `oclic-skills` plugin.

## Included skills

- `analyze-class` — analyze one class or use `--deep` for all classes, endpoints, and controllers.
- `analyze-component` — analyze one Razor item or use `--deep` for all `.razor` and `.cshtml` UI.
- `method-analyze` — recursively trace an application-owned method.
- `commit` — categorize repository changes into focused local commits.
- `commit-and-push` — create categorized commits and push the current branch safely.
- `commit-and-deploy` — version, commit, and deploy through the project's verified release procedure.
- `document` — persist verified application knowledge into the project's documentation store.
- `handoff` — transfer bounded work and context between Codex tasks or projects.
- `delegate` — send the current request to a separate Codex task and wait for its report.
- `delegate-continue` — send the current request to a separate task and continue chatting without waiting.
- `delegate-sub` — assign the current request to a child subagent and wait for its report.
- `delegate-sub-continue` — assign the current request to a child subagent and continue without waiting.

## Install from a cloned repository

```text
git clone https://github.com/Oclick021/codex-marketplace.git
codex plugin marketplace add <path-to-cloned-codex-marketplace>
codex plugin add oclic-skills@oclic-skills
```

Start a new Codex task after installation so the bundled skills are loaded.

## Repository layout

```text
.agents/plugins/marketplace.json
plugins/oclic-skills/.codex-plugin/plugin.json
plugins/oclic-skills/skills/
```
