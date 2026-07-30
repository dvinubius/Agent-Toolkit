# Agent Toolkit

This repository collects personal coding agent skills and supporting documentation for agent workflows. Each skill lives under `skills/<skill-name>/SKILL.md` and can be installed or referenced from an agent environment that supports skill discovery.

The repository also includes `agent-loop-explainer.pdf`, a companion explanation artifact for agent loop concepts.

## Repository Layout

```text
skills/
  daedalus/
  explain-diff/
  feynman/
  my-dev-ops/
  neatify-code/
  socrates/
  to-my-specs/
  validate-markdown-repo/
  web-app-arsenal/
  writing-great-skills/
```

## Skills

| Skill | Use it for | Notes |
|---|---|---|
| [`daedalus`](skills/daedalus/SKILL.md) | Turning ready-to-present coding work into a deliberate-practice challenge. | At the point where the agent would normally present completed work, it seals the solution and carves selected pieces into TODOs with analytical review criteria and file-linked checklist items. After all TODOs are complete, it offers the same verification used before carving, and no more. It composes with [`socrates`](skills/socrates/SKILL.md) only when the user asks for hint-based help. |
| [`socrates`](skills/socrates/SKILL.md) | Guiding a user through reasoning instead of immediately giving the final answer. | Useful for learning, debugging, design tradeoffs, algorithms, architecture, and other reasoning-heavy work. It uses targeted questions and a graduated hint ladder, while still giving direct warnings for risky actions. |
| [`explain-diff`](skills/explain-diff/SKILL.md) | Producing a rich, interactive HTML explanation of a code change, diff, branch, or PR — background, intuition, code walkthrough, and a comprehension quiz. | Derived from [Geoffrey Litt's explain-diff gist](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524). This version adds quiz anti-leakage rules — options of comparable length with distractors drawn from real misreadings, and correct-answer positions spread across A–D with a pre-save check — so the answer can't be guessed from form alone. |
| [`feynman`](skills/feynman/SKILL.md) | Teaching one technical theme as a mechanism-first document with examples, edge cases, and an exercise. | Derived from [Owain Lewis's feynman](https://github.com/owainlewis/agent-skills/blob/main/skills/feynman/SKILL.md). This version folds the document-shape rules into the Structure template as the single source of truth, replaces the separate Check section with a completion criterion, collapses overlapping ordering and style rules, and names the difference in the weak/strong mechanism example. |
| [`my-dev-ops`](skills/my-dev-ops/SKILL.md) | Deployment, release, CI/CD, hosting, GitHub, infrastructure, package publishing, and runtime environment work. | Prefers available CLI tools over MCP integrations when reliable, requires clear context for consequential operations, and respects dependency age and operational safety policies. |
| [`neatify-code`](skills/neatify-code/SKILL.md) | Improving bounded code maintainability while preserving behavior. | Defaults to changed code, reviewed diffs, or a developer-selected slice; requires confirmation for repository-wide cleanup; uses static evidence first; and includes optional Fallow guidance for JavaScript and TypeScript projects when Fallow is already available or explicitly approved. |
| [`to-my-specs`](skills/to-my-specs/SKILL.md) | Creating or updating product and business intent specs from explicit conversational context. | Designed for `.devnotes/specs` style documentation. It avoids inferring product intent from implementation details and separates confirmed intent from open questions. |
| [`validate-markdown-repo`](skills/validate-markdown-repo/SKILL.md) | Validating Markdown-heavy repositories. | Provides a reusable Python checker for local Markdown links, skill frontmatter, and template/live Markdown file pairs. The script is in [`skills/validate-markdown-repo/scripts/validate_markdown_repo.py`](skills/validate-markdown-repo/scripts/validate_markdown_repo.py). |
| [`web-app-arsenal`](skills/web-app-arsenal/SKILL.md) | Choosing and evaluating pragmatic web app tools. | Covers stack and infrastructure candidates such as Biome, Coolify, SerpApi, Depot, PocketBase, Convex, Render, Neon, Supabase, Drizzle, and Fallow, while requiring fit-based comparison against mainstream alternatives. |
| [`writing-great-skills`](skills/writing-great-skills/SKILL.md) | Writing, auditing, and testing agent skills. | Derived from [Matt Pocock's writing-great-skills](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md), which supplies the core vocabulary and framework. This version adds audit/write procedures with completion criteria, calibration to model strength (degrees of freedom, over-specification), worked-example guidance, an empirical testing loop, and new failure modes (contradiction, overfitting). |

## Markdown Validation

Run the repository Markdown check from the repo root:

```bash
python3 skills/validate-markdown-repo/scripts/validate_markdown_repo.py --root . --frontmatter-root skills
```

This validates local Markdown links across the repository and verifies required skill frontmatter fields under `skills/`.

## Attribution

Some skills are derived from work by other authors; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
