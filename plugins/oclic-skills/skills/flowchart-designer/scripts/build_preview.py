"""Build an interactive Codex visualization from one Mermaid source file."""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


NODE_PREFIX = "%% @node "
ANNOTATION_PREFIX = "%% @annotation "


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


def parse_source(source: Path, root: Path) -> dict:
    mermaid = source.read_text(encoding="utf-8")
    nodes: dict[str, dict] = {}
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
            resolved = []
            for target in code:
                path = Path(target["path"])
                path = (path if path.is_absolute() else root / path).resolve()
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
        elif line.startswith(ANNOTATION_PREFIX):
            item = json.loads(line[len(ANNOTATION_PREFIX) :])
            annotations[item["id"]] = item["text"]
    if not nodes:
        raise ValueError("Add %% @node metadata for each diagram node")
    for step in annotations:
        if step not in nodes:
            raise ValueError(f"Annotation has no node: {step}")
    return {"source": mermaid, "sourceHash": hashlib.sha256(mermaid.encode()).hexdigest(), "path": str(source), "nodes": nodes, "annotations": annotations}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Editable .mmd source")
    parser.add_argument("output", type=Path, help="Writable HTML fragment")
    parser.add_argument("--project-root", help="Base directory for relative code paths")
    args = parser.parse_args()
    source = args.source.resolve()
    if source.suffix.lower() != ".mmd":
        parser.error("source must be a .mmd file")
    payload = parse_source(source, project_root(source, args.project_root))
    template = (Path(__file__).parent.parent / "assets" / "preview.html").read_text(encoding="utf-8")
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    preview_id = "flowchart-" + hashlib.sha256(str(args.output.resolve()).encode()).hexdigest()[:12]
    args.output.write_text(
        template.replace("__FLOWCHART_PAYLOAD__", data).replace("__FLOWCHART_ID__", preview_id),
        encoding="utf-8",
    )
    print(f"Wrote {args.output.resolve()} with {len(payload['nodes'])} mapped steps")


if __name__ == "__main__":
    main()
