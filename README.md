# Agent Toolkit

This repository collects personal Codex skills and supporting documentation for agent workflows. Each skill lives under `skills/<skill-name>/SKILL.md` and can be installed or referenced from an agent environment that supports skill discovery.

The repository also includes `agent-loop-explainer.pdf`, a companion explanation artifact for agent loop concepts.

## Repository Layout

```text
skills/
  daedalus/
  my-dev-ops/
  socrates/
  to-my-specs/
  validate-markdown-repo/
  web-app-arsenal/
```

## Skills

| Skill | Use it for | Notes |
|---|---|---|
| [`daedalus`](skills/daedalus/SKILL.md) | Turning a completed coding task into a deliberate-practice challenge. | The agent first implements and verifies a working solution, then removes selected pieces into TODOs with tests, acceptance criteria, and file-linked checklist items. It composes with [`socrates`](skills/socrates/SKILL.md) for hint-based help during the exercise. |
| [`socrates`](skills/socrates/SKILL.md) | Guiding a user through reasoning instead of immediately giving the final answer. | Useful for learning, debugging, design tradeoffs, algorithms, architecture, and other reasoning-heavy work. It uses targeted questions and a graduated hint ladder, while still giving direct warnings for risky actions. |
| [`my-dev-ops`](skills/my-dev-ops/SKILL.md) | Deployment, release, CI/CD, hosting, GitHub, infrastructure, package publishing, and runtime environment work. | Prefers available CLI tools over MCP integrations when reliable, requires clear context for consequential operations, and respects dependency age and operational safety policies. |
| [`to-my-specs`](skills/to-my-specs/SKILL.md) | Creating or updating product and business intent specs from explicit conversational context. | Designed for `.devnotes/specs` style documentation. It avoids inferring product intent from implementation details and separates confirmed intent from open questions. |
| [`validate-markdown-repo`](skills/validate-markdown-repo/SKILL.md) | Validating Markdown-heavy repositories. | Provides a reusable Python checker for local Markdown links, skill frontmatter, and template/live Markdown file pairs. The script is in [`skills/validate-markdown-repo/scripts/validate_markdown_repo.py`](skills/validate-markdown-repo/scripts/validate_markdown_repo.py). |
| [`web-app-arsenal`](skills/web-app-arsenal/SKILL.md) | Choosing and evaluating pragmatic web app tools. | Covers stack and infrastructure candidates such as Biome, Coolify, SerpApi, Depot, PocketBase, Convex, Render, Neon, Supabase, Drizzle, and Fallow, while requiring fit-based comparison against mainstream alternatives. |

## Markdown Validation

Run the repository Markdown check from the repo root:

```bash
python3 skills/validate-markdown-repo/scripts/validate_markdown_repo.py --root . --frontmatter-root skills
```

This validates local Markdown links across the repository and verifies required skill frontmatter fields under `skills/`.
