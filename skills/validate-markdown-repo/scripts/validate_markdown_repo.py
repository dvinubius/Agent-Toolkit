#!/usr/bin/env python3
"""Validate Markdown links, skill frontmatter, and template pairs."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote


DEFAULT_EXCLUDES = [
    ".git/**",
    ".hg/**",
    ".svn/**",
    "node_modules/**",
    ".venv/**",
    "venv/**",
    "__pycache__/**",
    ".mypy_cache/**",
    ".pytest_cache/**",
    ".next/**",
    "dist/**",
    "build/**",
    "coverage/**",
]

INLINE_LINK_RE = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
REFERENCE_DEF_RE = re.compile(r"^\s{0,3}\[[^\]\n]+\]:\s*(\S+)", re.MULTILINE)
SCHEME_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)


@dataclass(frozen=True)
class LinkRoot:
    scope: Path | None
    base: Path


@dataclass(frozen=True)
class TemplatePair:
    template: Path
    live: Path


def load_json_config(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"Config must be a JSON object: {path}")
    return data


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def resolve_under(root: Path, value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return root / path


def relative_posix(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def is_under(path: Path, maybe_parent: Path) -> bool:
    try:
        path.relative_to(maybe_parent)
        return True
    except ValueError:
        return False


def split_mapping(raw: str, option_name: str) -> tuple[str | None, str]:
    if "=" not in raw:
        return None, raw
    left, right = raw.split("=", 1)
    if not left or not right:
        raise SystemExit(f"{option_name} must use SCOPE=BASE or BASE: {raw}")
    return left, right


def parse_link_roots(root: Path, config_items: Iterable[Any], cli_items: Iterable[str]) -> list[LinkRoot]:
    parsed: list[LinkRoot] = []
    for item in config_items:
        if isinstance(item, dict):
            base_value = item.get("base")
            if not base_value:
                raise SystemExit("Each config link_roots item must include base")
            scope_value = item.get("scope")
        elif isinstance(item, str):
            scope_value, base_value = split_mapping(item, "link_roots")
        else:
            raise SystemExit(f"Unsupported link_roots item: {item!r}")
        parsed.append(
            LinkRoot(
                scope=resolve_under(root, scope_value).resolve() if scope_value else None,
                base=resolve_under(root, base_value).resolve(),
            )
        )
    for item in cli_items:
        scope_value, base_value = split_mapping(item, "--link-root")
        parsed.append(
            LinkRoot(
                scope=resolve_under(root, scope_value).resolve() if scope_value else None,
                base=resolve_under(root, base_value).resolve(),
            )
        )
    return parsed


def parse_template_pairs(root: Path, config_items: Iterable[Any], cli_items: Iterable[str]) -> list[TemplatePair]:
    pairs: list[TemplatePair] = []
    for item in config_items:
        if isinstance(item, dict):
            template = item.get("template")
            live = item.get("live")
            if not template or not live:
                raise SystemExit("Each config template_pairs item must include template and live")
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            template, live = item
        elif isinstance(item, str) and "=" in item:
            template, live = item.split("=", 1)
        else:
            raise SystemExit(f"Unsupported template_pairs item: {item!r}")
        pairs.append(TemplatePair(resolve_under(root, template), resolve_under(root, live)))
    for item in cli_items:
        if "=" not in item:
            raise SystemExit(f"--template-pair must use TEMPLATE=LIVE: {item}")
        template, live = item.split("=", 1)
        if not template or not live:
            raise SystemExit(f"--template-pair must use TEMPLATE=LIVE: {item}")
        pairs.append(TemplatePair(resolve_under(root, template), resolve_under(root, live)))
    return pairs


def strip_code(text: str) -> str:
    stripped_lines: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines():
        marker = re.match(r"^\s*(```+|~~~+)", line)
        if marker:
            current = marker.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_marker = current
            elif current == fence_marker:
                in_fence = False
            stripped_lines.append("")
            continue
        if in_fence:
            stripped_lines.append("")
            continue
        stripped_lines.append(re.sub(r"`[^`\n]*`", "", line))
    return "\n".join(stripped_lines)


def parse_markdown_destination(raw: str) -> str:
    value = raw.strip()
    if not value:
        return ""
    if value.startswith("<"):
        end = value.find(">")
        if end != -1:
            value = value[1:end]
    else:
        value = value.split(None, 1)[0]
    value = value.split("#", 1)[0].split("?", 1)[0]
    return unquote(value.strip())


def should_skip_target(target: str) -> bool:
    return (
        not target
        or target.startswith("#")
        or target.startswith("//")
        or SCHEME_RE.match(target) is not None
    )


def iter_markdown_files(root: Path, markdown_roots: list[Path], includes: list[str], excludes: list[str]) -> list[Path]:
    files: set[Path] = set()
    for markdown_root in markdown_roots:
        for pattern in includes:
            for path in markdown_root.glob(pattern):
                if path.is_file():
                    files.add(path.resolve())
    result: list[Path] = []
    for path in sorted(files):
        rel = relative_posix(path, root)
        if any(path.match(pattern) or rel == pattern or Path(rel).match(pattern) for pattern in excludes):
            continue
        result.append(path)
    return result


def candidate_paths(root: Path, source: Path, target: str, link_roots: list[LinkRoot]) -> list[Path]:
    if target.startswith("/"):
        candidates = [(root / target.lstrip("/")).resolve()]
    else:
        candidates = [(source.parent / target).resolve()]
    for link_root in link_roots:
        if link_root.scope is None or is_under(source, link_root.scope):
            candidates.append((link_root.base / target.lstrip("/")).resolve())
    return candidates


def validate_links(root: Path, files: list[Path], link_roots: list[LinkRoot]) -> list[dict[str, str]]:
    missing: list[dict[str, str]] = []
    for path in files:
        text = strip_code(path.read_text(encoding="utf-8"))
        raw_targets = [match.group(1) for match in INLINE_LINK_RE.finditer(text)]
        raw_targets.extend(match.group(1) for match in REFERENCE_DEF_RE.finditer(text))
        for raw in raw_targets:
            target = parse_markdown_destination(raw)
            if should_skip_target(target):
                continue
            candidates = candidate_paths(root, path, target, link_roots)
            if not any(candidate.exists() for candidate in candidates):
                missing.append({"file": relative_posix(path, root), "target": raw.strip()})
    return missing


def validate_frontmatter(
    root: Path,
    frontmatter_roots: list[Path],
    required_fields: list[str],
    excludes: list[str],
) -> list[dict[str, str]]:
    problems: list[dict[str, str]] = []
    files = iter_markdown_files(root, frontmatter_roots, ["**/SKILL.md"], excludes)
    for path in files:
        text = path.read_text(encoding="utf-8")
        rel = relative_posix(path, root)
        if not text.startswith("---\n"):
            problems.append({"file": rel, "problem": "missing opening ---"})
            continue
        end = text.find("\n---\n", 4)
        if end == -1:
            problems.append({"file": rel, "problem": "missing closing ---"})
            continue
        frontmatter = text[4:end]
        for field in required_fields:
            pattern = rf"^{re.escape(field)}:\s*\S+"
            if not re.search(pattern, frontmatter, re.MULTILINE):
                problems.append({"file": rel, "problem": f"missing {field}"})
    return problems


def validate_templates(root: Path, pairs: list[TemplatePair]) -> list[dict[str, str]]:
    problems: list[dict[str, str]] = []
    for pair in pairs:
        template_exists = pair.template.exists()
        live_exists = pair.live.exists()
        if not template_exists or not live_exists:
            problems.append(
                {
                    "template": relative_posix(pair.template, root),
                    "live": relative_posix(pair.live, root),
                    "problem": "missing pair",
                }
            )
            continue
        template_lines = pair.template.read_text(encoding="utf-8").splitlines()
        live_lines = pair.live.read_text(encoding="utf-8").splitlines()
        if template_lines != live_lines:
            diff = "\n".join(
                difflib.unified_diff(
                    template_lines,
                    live_lines,
                    fromfile=relative_posix(pair.template, root),
                    tofile=relative_posix(pair.live, root),
                    lineterm="",
                )
            )
            problems.append(
                {
                    "template": relative_posix(pair.template, root),
                    "live": relative_posix(pair.live, root),
                    "problem": "mismatch",
                    "diff": diff,
                }
            )
    return problems


def print_human_report(report: dict[str, Any]) -> None:
    if report["missing_links"]:
        print("Missing local Markdown links:")
        for item in report["missing_links"]:
            print(f"{item['file']} -> {item['target']}")
    if report["bad_frontmatter"]:
        print("Bad skill frontmatter:")
        for item in report["bad_frontmatter"]:
            print(f"{item['file']}: {item['problem']}")
    if report["template_mismatches"]:
        print("Template mismatches:")
        for item in report["template_mismatches"]:
            if item["problem"] == "missing pair":
                print(f"missing pair: {item['template']} -> {item['live']}")
            else:
                print(item["diff"])
    if report["ok"]:
        print(
            "OK: checked "
            f"{report['markdown_file_count']} markdown files, "
            f"{report['frontmatter_file_count']} frontmatter roots, and "
            f"{report['template_pair_count']} template pairs"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, help="JSON config file")
    parser.add_argument("--root", type=Path, help="Repository root")
    parser.add_argument("--markdown-root", action="append", default=[], help="Markdown root to scan")
    parser.add_argument("--include", action="append", default=[], help="Markdown include glob")
    parser.add_argument("--exclude", action="append", default=[], help="Relative exclude glob")
    parser.add_argument("--no-link-check", action="store_true", help="Skip local Markdown link validation")
    parser.add_argument("--link-root", action="append", default=[], help="Fallback link root: SCOPE=BASE or BASE")
    parser.add_argument("--frontmatter-root", action="append", default=[], help="Root containing SKILL.md files")
    parser.add_argument("--frontmatter-field", action="append", default=[], help="Required frontmatter field")
    parser.add_argument("--template-pair", action="append", default=[], help="Template/live pair: TEMPLATE=LIVE")
    parser.add_argument("--format", choices=["human", "json"], default="human", help="Report format")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_json_config(args.config)

    root = (args.root or Path(config.get("root", "."))).resolve()
    markdown_roots = [
        resolve_under(root, item).resolve()
        for item in (args.markdown_root or as_list(config.get("markdown_roots")) or [root])
    ]
    includes = args.include or as_list(config.get("include")) or ["**/*.md"]
    excludes = DEFAULT_EXCLUDES + as_list(config.get("exclude")) + args.exclude
    check_links = bool(config.get("check_links", True)) and not args.no_link_check
    link_roots = parse_link_roots(root, as_list(config.get("link_roots")), args.link_root)
    frontmatter_roots = [
        resolve_under(root, item).resolve()
        for item in (args.frontmatter_root or as_list(config.get("frontmatter_roots")))
    ]
    frontmatter_fields = args.frontmatter_field or as_list(config.get("frontmatter_fields")) or ["name", "description"]
    template_pairs = parse_template_pairs(root, as_list(config.get("template_pairs")), args.template_pair)

    markdown_files = iter_markdown_files(root, markdown_roots, includes, excludes)
    missing_links = validate_links(root, markdown_files, link_roots) if check_links else []
    bad_frontmatter = validate_frontmatter(root, frontmatter_roots, frontmatter_fields, excludes) if frontmatter_roots else []
    template_mismatches = validate_templates(root, template_pairs)
    ok = not missing_links and not bad_frontmatter and not template_mismatches

    report = {
        "ok": ok,
        "markdown_file_count": len(markdown_files),
        "frontmatter_file_count": len(frontmatter_roots),
        "template_pair_count": len(template_pairs),
        "missing_links": missing_links,
        "bad_frontmatter": bad_frontmatter,
        "template_mismatches": template_mismatches,
    }
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human_report(report)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
