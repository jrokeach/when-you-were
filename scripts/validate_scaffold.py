#!/usr/bin/env python3
"""Lightweight validation for the public When You Were scaffold.

This intentionally uses only the Python standard library so a fresh clone can
run it before installing any product- or host-app-specific tooling. It is not a
full YAML or JSON Schema validator; it checks the invariants that protect the
public template contract.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class ValidationError:
    message: str
    path: Path | None = None
    line: int | None = None


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def fail(errors: list[ValidationError], message: str, path: Path | None = None, line: int | None = None) -> None:
    errors.append(ValidationError(message=message, path=path, line=line))


def format_error(error: ValidationError) -> str:
    if error.path is None:
        return error.message
    location = rel(error.path)
    if error.line is not None:
        location = f"{location}:{error.line}"
    return f"{location}: {error.message}"


def escape_command_value(value: str) -> str:
    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def escape_command_property(value: str) -> str:
    return escape_command_value(value).replace(":", "%3A").replace(",", "%2C")


def emit_github_annotation(error: ValidationError) -> None:
    props: list[str] = []
    if error.path is not None:
        props.append(f"file={escape_command_property(rel(error.path))}")
    if error.line is not None:
        props.append(f"line={error.line}")
    prop_text = f" {','.join(props)}" if props else ""
    print(f"::error{prop_text}::{escape_command_value(error.message)}", file=sys.stderr)


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def parse_simple_manifest(path: Path) -> dict[str, dict[str, list[str]]]:
    """Parse the path-set portions of UPSTREAM.manifest.yml.

    The manifest is deliberately simple: top-level sections contain `exact:`
    and/or `globs:` lists. This parser is strict enough to catch drift while
    avoiding a runtime PyYAML dependency.
    """

    result: dict[str, dict[str, list[str]]] = {}
    section: str | None = None
    bucket: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if re.match(r"^[A-Za-z0-9_]+:", raw_line):
            key = raw_line.split(":", 1)[0]
            section = key
            bucket = None
            result.setdefault(section, {})
            continue
        if section and re.match(r"^  (exact|globs):", raw_line):
            bucket = raw_line.strip().split(":", 1)[0]
            result[section].setdefault(bucket, [])
            continue
        if section and bucket and raw_line.startswith("    - "):
            value = raw_line.split("- ", 1)[1].strip()
            result[section][bucket].append(value)
    return result


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def parse_inline_list(value: str) -> list[str]:
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return []
    inner = value[1:-1].strip()
    if not inner:
        return []
    return [item.strip().strip('"').strip("'") for item in inner.split(",")]


def parse_simple_yaml_scalars(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line.startswith(" "):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def check_json_schemas(errors: list[ValidationError]) -> None:
    for path in sorted((ROOT / "schema").glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report parser detail
            line = getattr(exc, "lineno", None)
            fail(errors, f"is not valid JSON: {exc}", path, line)


def check_manifest(errors: list[ValidationError]) -> dict[str, dict[str, list[str]]]:
    path = ROOT / "UPSTREAM.manifest.yml"
    if not path.exists():
        fail(errors, "UPSTREAM.manifest.yml is missing")
        return {}
    text = path.read_text(encoding="utf-8")
    for required in ("schema_version:", "scaffold_version:", "upstream_tracked:"):
        if required not in text:
            fail(errors, f"missing {required}", path)
    manifest = parse_simple_manifest(path)
    for tracked in manifest.get("upstream_tracked", {}).get("exact", []):
        if not (ROOT / tracked).exists():
            fail(errors, f"lists missing upstream path: {tracked}", path)
    return manifest


def check_frontmatter(errors: list[ValidationError]) -> None:
    for path in sorted((ROOT / "wiki").rglob("*.md")):
        data = parse_frontmatter(path)
        if not data:
            fail(errors, "missing YAML frontmatter", path, 1)
            continue
        for key in ("title", "type", "subjects", "status"):
            if key not in data:
                fail(errors, f"missing frontmatter key: {key}", path, 1)
        subjects = parse_inline_list(data.get("subjects", ""))
        if not subjects:
            fail(errors, "subjects must be an inline non-empty list", path, 1)
        status = data.get("status", "")
        in_reference = rel(path).startswith("wiki/children/_template/") or rel(path).startswith(
            "wiki/family/_examples/"
        )
        if status == "example" and not in_reference:
            fail(errors, "has status: example outside reference trees", path, 1)
        if in_reference and status != "example":
            fail(errors, "is in a reference tree but is not status: example", path, 1)


LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md)(?:#[^)]+)?\)")


def mask_markdown_code(text: str) -> str:
    text = re.sub(r"```.*?```", lambda match: "\n" * match.group(0).count("\n"), text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]+`", "", text)
    return text


def check_links(errors: list[ValidationError]) -> None:
    for path in sorted((ROOT / "wiki").rglob("*.md")):
        text = mask_markdown_code(path.read_text(encoding="utf-8"))
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            line = line_number_for_offset(text, match.start(1))
            if re.match(r"^[a-z]+://", target) or target.startswith("#"):
                continue
            if target.startswith("/"):
                fail(errors, f"uses absolute markdown link: {target}", path, line)
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(errors, f"link escapes repo: {target}", path, line)
                continue
            if not resolved.exists():
                fail(errors, f"has broken markdown link: {target}", path, line)


def check_raw_manifests(errors: list[ValidationError]) -> None:
    required = {"storage", "provider", "bucket", "key", "sha256", "bytes", "media_type"}
    for path in sorted((ROOT / "raw").rglob("*.manifest.yml")):
        data = parse_simple_yaml_scalars(path)
        missing = sorted(required - data.keys())
        if missing:
            fail(errors, f"missing required raw manifest keys: {', '.join(missing)}", path)
        sha = data.get("sha256", "")
        if sha and not re.match(r"^[A-Fa-f0-9]{64}$", sha):
            fail(errors, "sha256 must be 64 hex characters", path)
        bytes_value = data.get("bytes", "")
        if bytes_value and not bytes_value.isdigit():
            fail(errors, "bytes must be a non-negative integer", path)


def check_ignored_paths(errors: list[ValidationError]) -> None:
    samples = [
        "AGENTS.local.md",
        "AGENTS.overlay.md",
        ".agents-last-lint",
        ".agents-local-last-prompt",
        ".agents/hooks.overlay/example.sh",
        ".agents/settings.local.json",
        ".agents/skills.overlay/example/SKILL.md",
        ".claude/hooks.overlay/example.sh",
        ".claude/settings.local.json",
        ".claude/skills.overlay/example/SKILL.md",
        ".local/PRODUCT_TODO.md",
        ".scaffold-upstream",
    ]
    for sample in samples:
        proc = subprocess.run(
            ["git", "check-ignore", "-q", sample],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if proc.returncode != 0:
            fail(errors, f"{sample} should be ignored by .gitignore")


def check_skill_mirrors(errors: list[ValidationError]) -> None:
    pairs = [
        (ROOT / ".agents/skills/lint/SKILL.md", ROOT / ".claude/skills/lint/SKILL.md"),
        (ROOT / ".agents/skills/sync-scaffold/SKILL.md", ROOT / ".claude/skills/sync-scaffold/SKILL.md"),
    ]
    for canonical, mirror in pairs:
        if not canonical.exists():
            fail(errors, "canonical skill missing", canonical)
            continue
        if not mirror.exists():
            fail(errors, "Claude compatibility skill missing", mirror)
            continue
        if canonical.read_text(encoding="utf-8") != mirror.read_text(encoding="utf-8"):
            fail(errors, f"must mirror {rel(canonical)}", mirror)


def main() -> int:
    errors: list[ValidationError] = []
    check_json_schemas(errors)
    check_manifest(errors)
    check_frontmatter(errors)
    check_links(errors)
    check_raw_manifests(errors)
    check_ignored_paths(errors)
    check_skill_mirrors(errors)
    if errors:
        print("Scaffold validation failed:", file=sys.stderr)
        for error in errors:
            if os.environ.get("GITHUB_ACTIONS") == "true":
                emit_github_annotation(error)
            print(f"- {format_error(error)}", file=sys.stderr)
        return 1
    print("Scaffold validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
