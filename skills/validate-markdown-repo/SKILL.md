---
name: validate-markdown-repo
description: Validate Markdown-heavy repositories with a bundled, parameterized Python script — local link targets, SKILL.md frontmatter, mirrored template/live file pairs. Use when a task involves checking or maintaining many Markdown files or documentation consistency that would otherwise require writing an ad hoc validation script.
---

# Validate Markdown Repo

Use the bundled script instead of inventing a one-off validator. It provides deterministic checks for:

- local Markdown link targets, including image links and reference definitions
- `SKILL.md` YAML frontmatter fields such as `name` and `description`
- template/live Markdown file pairs that must remain line-for-line identical

## Quick Start

The script lives in this skill's folder; the repository being validated can be anywhere. Substitute this skill's base directory (shown when the skill loads) for `<skill-dir>` and run from the target repository root:

```bash
python3 <skill-dir>/scripts/validate_markdown_repo.py --root .
```

For a skill repository, add frontmatter validation:

```bash
python3 <skill-dir>/scripts/validate_markdown_repo.py --root . --frontmatter-root skills
```

For scaffold/template workflows, pass fallback link bases and template pairs:

```bash
python3 <skill-dir>/scripts/validate_markdown_repo.py \
  --root . \
  --markdown-root docs \
  --link-root docs/scaffold=docs/scaffold \
  --frontmatter-root docs/scaffold/.agent/skills \
  --template-pair docs/templates/overview.md=docs/overview.md
```

## Configuration File

Use a JSON config when there are many paths. Keys mirror the CLI options: `root`, `markdown_roots`, `include`, `exclude`, `check_links`, `link_roots` (objects with `scope` and `base`), `frontmatter_roots`, `frontmatter_fields`, and `template_pairs` (objects with `template` and `live`).

```json
{
  "root": ".",
  "markdown_roots": ["docs"],
  "link_roots": [{ "scope": "docs/scaffold", "base": "docs/scaffold" }],
  "frontmatter_roots": ["docs/scaffold/.agent/skills"],
  "template_pairs": [
    { "template": "docs/templates/overview.md", "live": "docs/overview.md" }
  ]
}
```

```bash
python3 <skill-dir>/scripts/validate_markdown_repo.py --config markdown-validation.json
```

## Script Options

- `--root PATH`: repository root used to resolve relative paths.
- `--markdown-root PATH`: root to scan for Markdown files; repeatable. Defaults to `--root`.
- `--include GLOB`: Markdown include glob; repeatable. Defaults to `**/*.md`.
- `--exclude GLOB`: relative path exclude glob; repeatable. Common build and dependency folders are excluded by default.
- `--no-link-check`: skip local Markdown link validation.
- `--link-root SCOPE=BASE`: when a source Markdown file is under `SCOPE`, also resolve local links relative to `BASE`; repeatable. Use `BASE` without `SCOPE=` to apply to all scanned files.
- `--frontmatter-root PATH`: scan for `SKILL.md` files under this root and require valid frontmatter; repeatable.
- `--frontmatter-field NAME`: required frontmatter field; repeatable. Defaults to `name` and `description`.
- `--template-pair TEMPLATE=LIVE`: require two files to exist and have identical line content; repeatable.
- `--format human|json`: choose report format.

If validation fails, fix the reported files and rerun the same command. Done when the run prints `OK` and exits 0.
