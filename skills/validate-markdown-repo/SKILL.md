---
name: validate-markdown-repo
description: Validate Markdown-heavy work in any repository with a bundled, parameterized Python script. Use when a task involves checking or maintaining many Markdown files, local Markdown links, skill-style SKILL.md frontmatter, mirrored template files, scaffold docs, generated docs, or documentation consistency that would otherwise require writing an ad hoc Markdown validation script.
---

# Validate Markdown Repo

Use the bundled script instead of inventing a one-off validator when a task involves many Markdown files and needs deterministic checks for:

- local Markdown link targets, including image links and reference definitions
- `SKILL.md` YAML frontmatter fields such as `name` and `description`
- template/live Markdown file pairs that must remain byte-for-line identical

## Quick Start

Run from the repository root:

```bash
python3 skills/validate-markdown-repo/scripts/validate_markdown_repo.py --root .
```

For a skill repository, add frontmatter validation:

```bash
python3 skills/validate-markdown-repo/scripts/validate_markdown_repo.py \
  --root . \
  --frontmatter-root skills
```

For scaffold/template workflows, pass fallback link bases and template pairs:

```bash
python3 skills/validate-markdown-repo/scripts/validate_markdown_repo.py \
  --root . \
  --markdown-root Agentic-Methodologies/Lean-DOX-Hybrid-Methodology \
  --link-root Agentic-Methodologies/Lean-DOX-Hybrid-Methodology/scaffold=Agentic-Methodologies/Lean-DOX-Hybrid-Methodology/scaffold \
  --frontmatter-root Agentic-Methodologies/Lean-DOX-Hybrid-Methodology/scaffold/.agent/skills \
  --template-pair Agentic-Methodologies/Lean-DOX-Hybrid-Methodology/scaffold/.agent/docs/templates/overview.md=Agentic-Methodologies/Lean-DOX-Hybrid-Methodology/scaffold/docs/overview.md
```

## Configuration File

Use a JSON config when there are many paths:

```json
{
  "root": ".",
  "markdown_roots": ["Agentic-Methodologies/Lean-DOX-Hybrid-Methodology"],
  "link_roots": [
    {
      "scope": "Agentic-Methodologies/Lean-DOX-Hybrid-Methodology/scaffold",
      "base": "Agentic-Methodologies/Lean-DOX-Hybrid-Methodology/scaffold"
    }
  ],
  "frontmatter_roots": [
    "Agentic-Methodologies/Lean-DOX-Hybrid-Methodology/scaffold/.agent/skills"
  ],
  "template_pairs": [
    {
      "template": "Agentic-Methodologies/Lean-DOX-Hybrid-Methodology/scaffold/.agent/docs/templates/overview.md",
      "live": "Agentic-Methodologies/Lean-DOX-Hybrid-Methodology/scaffold/docs/overview.md"
    }
  ]
}
```

Then run:

```bash
python3 skills/validate-markdown-repo/scripts/validate_markdown_repo.py --config markdown-validation.json
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

If validation fails, fix the reported files and rerun the same command.
