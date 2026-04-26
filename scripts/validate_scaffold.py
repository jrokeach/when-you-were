#!/usr/bin/env python3
"""Lightweight validation for the public When You Were scaffold.

This intentionally uses only the Python standard library so a fresh clone can
run it before installing any product- or host-app-specific tooling. It is not a
full YAML or JSON Schema validator; it checks the invariants that protect the
public template contract.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


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


def check_json_schemas(errors: list[str]) -> None:
    for path in sorted((ROOT / "schema").glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report parser detail
            fail(errors, f"{rel(path)} is not valid JSON: {exc}")


def check_manifest(errors: list[str]) -> dict[str, dict[str, list[str]]]:
    path = ROOT / "UPSTREAM.manifest.yml"
    if not path.exists():
        fail(errors, "UPSTREAM.manifest.yml is missing")
        return {}
    text = path.read_text(encoding="utf-8")
    for required in ("schema_version:", "scaffold_version:", "upstream_tracked:"):
        if required not in text:
            fail(errors, f"UPSTREAM.manifest.yml missing {required}")
    manifest = parse_simple_manifest(path)
    for tracked in manifest.get("upstream_tracked", {}).get("exact", []):
        if not (ROOT / tracked).exists():
            fail(errors, f"UPSTREAM.manifest.yml lists missing upstream path: {tracked}")
    return manifest


def check_frontmatter(errors: list[str]) -> None:
    for path in sorted((ROOT / "wiki").rglob("*.md")):
        data = parse_frontmatter(path)
        if not data:
            fail(errors, f"{rel(path)} missing YAML frontmatter")
            continue
        for key in ("title", "type", "subjects", "status"):
            if key not in data:
                fail(errors, f"{rel(path)} missing frontmatter key: {key}")
        subjects = parse_inline_list(data.get("subjects", ""))
        if not subjects:
            fail(errors, f"{rel(path)} subjects must be an inline non-empty list")
        status = data.get("status", "")
        in_reference = rel(path).startswith("wiki/children/_template/") or rel(path).startswith(
            "wiki/family/_examples/"
        )
        if status == "example" and not in_reference:
            fail(errors, f"{rel(path)} has status: example outside reference trees")
        if in_reference and status != "example":
            fail(errors, f"{rel(path)} is in a reference tree but is not status: example")


LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md)(?:#[^)]+)?\)")


def strip_markdown_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]+`", "", text)
    return text


def check_links(errors: list[str]) -> None:
    for path in sorted((ROOT / "wiki").rglob("*.md")):
        text = strip_markdown_code(path.read_text(encoding="utf-8"))
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if re.match(r"^[a-z]+://", target) or target.startswith("#"):
                continue
            if target.startswith("/"):
                fail(errors, f"{rel(path)} uses absolute markdown link: {target}")
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(errors, f"{rel(path)} link escapes repo: {target}")
                continue
            if not resolved.exists():
                fail(errors, f"{rel(path)} has broken markdown link: {target}")


def check_raw_manifests(errors: list[str]) -> None:
    required = {"storage", "provider", "bucket", "key", "sha256", "bytes", "media_type"}
    for path in sorted((ROOT / "raw").rglob("*.manifest.yml")):
        data = parse_simple_yaml_scalars(path)
        missing = sorted(required - data.keys())
        if missing:
            fail(errors, f"{rel(path)} missing required raw manifest keys: {', '.join(missing)}")
        sha = data.get("sha256", "")
        if sha and not re.match(r"^[A-Fa-f0-9]{64}$", sha):
            fail(errors, f"{rel(path)} sha256 must be 64 hex characters")
        bytes_value = data.get("bytes", "")
        if bytes_value and not bytes_value.isdigit():
            fail(errors, f"{rel(path)} bytes must be a non-negative integer")


def check_ignored_paths(errors: list[str]) -> None:
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


def check_skill_mirrors(errors: list[str]) -> None:
    pairs = [
        (ROOT / ".agents/skills/lint/SKILL.md", ROOT / ".claude/skills/lint/SKILL.md"),
        (ROOT / ".agents/skills/sync-scaffold/SKILL.md", ROOT / ".claude/skills/sync-scaffold/SKILL.md"),
    ]
    for canonical, mirror in pairs:
        if not canonical.exists():
            fail(errors, f"canonical skill missing: {rel(canonical)}")
            continue
        if not mirror.exists():
            fail(errors, f"Claude compatibility skill missing: {rel(mirror)}")
            continue
        if canonical.read_text(encoding="utf-8") != mirror.read_text(encoding="utf-8"):
            fail(errors, f"{rel(mirror)} must mirror {rel(canonical)}")


def main() -> int:
    errors: list[str] = []
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
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Scaffold validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
