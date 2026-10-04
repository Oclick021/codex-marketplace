"""Build an interactive browser flowchart from one Mermaid source file."""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


NODE_PREFIX = "%% @node "
ANNOTATION_PREFIX = "%% @annotation "
LEGACY_SOURCE = re.compile(r"^%% (?P<id>[A-Za-z][A-Za-z0-9_-]*): (?P<refs>.+)$")
SOURCE_PART = re.compile(r"^(?:(?P<path>.*?):)?(?P<line>\d+)(?:\s*\((?P<method>[^)]*)\))?$")


def project_root(source: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    result = subprocess.run(
        ["git", "-C", str(source.parent), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    return Path(result.stdout.strip()).resolve() if result.returncode == 0 else source.parent


def resolve_code_path(raw: str, root: Path, previous: Path | None) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path.resolve()
    candidates = [root / path]
    if previous:
        candidates.extend(parent / path for parent in previous.parents)
    return next((candidate.resolve() for candidate in candidates if candidate.is_file()), candidates[0].resolve())


def legacy_code(references: str, root: Path) -> list[dict]:
    code = []
    previous = None
    for part in re.split(r"[;,]\s*", references):
        match = SOURCE_PART.fullmatch(part.strip())
        if not match:
            raise ValueError(f"Cannot parse source reference: {part}")
        raw_path = match.group("path")
        if raw_path:
            previous = resolve_code_path(raw_path, root, previous)
        if previous is None:
            raise ValueError(f"Source reference has no file: {part}")
        code.append({"path": str(previous), "line": int(match.group("line")), "method": match.group("method") or ""})
    return code


def parse_source(source: Path, root: Path) -> dict:
    mermaid = source.read_text(encoding="utf-8")
    nodes: dict[str, dict] = {}
    legacy_nodes: dict[str, dict] = {}
    annotations: dict[str, str] = {}
    for line in mermaid.splitlines():
        if line.startswith(NODE_PREFIX):
            item = json.loads(line[len(NODE_PREFIX) :])
            step = item["id"]
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", step) or step in nodes:
                raise ValueError(f"Invalid or duplicate step ID: {step}")
            code = item.get("code", [])
            if not isinstance(code, list) or not code:
                raise ValueError(f"Step {step} needs at least one code target")
            nodes[step] = item
        elif line.startswith(ANNOTATION_PREFIX):
            item = json.loads(line[len(ANNOTATION_PREFIX) :])
            annotations[item["id"]] = item["text"]
        else:
            match = LEGACY_SOURCE.fullmatch(line)
            if match:
                legacy_nodes[match.group("id")] = {"id": match.group("id"), "code": legacy_code(match.group("refs"), root)}
    for step, item in legacy_nodes.items():
        nodes.setdefault(step, item)
    if not nodes:
        raise ValueError("Add %% @node or %% A: path:line metadata for each diagram node")
    for step, item in nodes.items():
        resolved = []
        for target in item["code"]:
            path = resolve_code_path(target["path"], root, None)
            line_number = target.get("line")
            if line_number is not None:
                if not path.is_file() or not 1 <= line_number <= len(
                    path.read_text(encoding="utf-8", errors="replace").splitlines()
                ):
                    raise ValueError(f"Invalid source line for {step}: {path}:{line_number}")
            elif not target.get("planned", False):
                raise ValueError(f"Step {step}: omit line only for a planned target")
            resolved.append({**target, "path": str(path)})
        nodes[step] = {**item, "code": resolved}
    for step in annotations:
        if step not in nodes:
            raise ValueError(f"Annotation has no node: {step}")
    return {"source": mermaid, "sourceHash": hashlib.sha256(mermaid.encode()).hexdigest(), "path": str(source), "nodes": nodes, "annotations": annotations}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Editable .mmd source")
    parser.add_argument("output", type=Path, help="Writable browser HTML page")
    parser.add_argument("--project-root", help="Base directory for relative code paths")
    parser.add_argument("--inline", action="store_true", help="Emit only an HTML fragment when inline display was requested")
    args = parser.parse_args()
    source = args.source.resolve()
    if source.suffix.lower() != ".mmd":
        parser.error("source must be a .mmd file")
    payload = parse_source(source, project_root(source, args.project_root))
    template = (Path(__file__).parent.parent / "assets" / "preview.html").read_text(encoding="utf-8")
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    preview_id = "flowchart-" + hashlib.sha256(str(args.output.resolve()).encode()).hexdigest()[:12]
    fragment = template.replace("__FLOWCHART_PAYLOAD__", data).replace("__FLOWCHART_ID__", preview_id)
    if args.inline:
        document = fragment
    else:
        document = (
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Interactive flowchart</title><style>'
            ':root{color-scheme:light dark;--background:#ffffff;--foreground:#172033;'
            '--muted-foreground:#526174;--border:#bec8d4;--input:#aab6c4;'
            '--popover:#ffffff;--popover-foreground:#172033;--blue:#155eef;'
            '--purple:#7a3de2;--yellow:#eab308;--green:#16a34a}'
            '@media(prefers-color-scheme:dark){:root{--background:#171b24;'
            '--foreground:#edf1f7;--muted-foreground:#b0bdcd;--border:#4b5869;'
            '--input:#64748b;--popover:#242b38;--popover-foreground:#edf1f7;'
            '--blue:#7db0ff;--purple:#bc9aff;--yellow:#facc15;--green:#4ade80}}'
            'body{margin:0;padding:16px;font:14px system-ui,sans-serif;'
            'background:var(--background);color:var(--foreground)}'
            'button{padding:6px 10px;border:1px solid var(--border);border-radius:6px;'
            'background:var(--popover);color:var(--popover-foreground)}'
            '</style></head><body>' + fragment + '</body></html>'
        )
    args.output.write_text(document, encoding="utf-8")
    print(f"Wrote {args.output.resolve()} with {len(payload['nodes'])} mapped steps")


if __name__ == "__main__":
    main()
