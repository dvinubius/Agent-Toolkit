---
name: web-app-arsenal
description: Pragmatic web app stack selection guidance for development, CI, databases, backend platforms, search APIs, code quality, and deployment. Use when choosing, reviewing, or comparing tools/products for a web app, especially Biome, Coolify, SerpApi, Depot, PocketBase, Render, Neon, Supabase, Drizzle, or Fallow, or when an agent needs pros/cons and fit guidance before adding infrastructure or dependencies.
---

# Web App Arsenal

Use this skill to evaluate whether a tool from the user's web-app arsenal is a good fit for the app in front of you. Treat the listed tools as interesting candidates, not defaults.

## Decision Rules

- Prefer the best fit for the app, even when it is not in this arsenal. If Vercel, Netlify, Fly.io, Railway, AWS, Prisma, plain Postgres, Playwright, or another mainstream option better serves the constraints, recommend it plainly.
- Start from the app's constraints: team size, budget, expected traffic, compliance needs, operational tolerance, data model, auth needs, CI pain, deployment target, and existing stack.
- Avoid adding a paid or hosted dependency unless it removes meaningful product, operations, compliance, or maintenance risk.
- Before installing any package, obey the user's package-age policy: verify the package and exact version age from the registry or repository, and do not install versions published less than 3 weeks ago.
- When a choice affects production operations, cite current official docs or pricing pages before making a final recommendation.

## Workflow

1. Identify the job-to-be-done: formatting/linting, deployment, CI acceleration, backend platform, Postgres, ORM, search data, or codebase intelligence.
2. Read [references/tools.md](references/tools.md) before recommending any arsenal item.
3. Compare the arsenal option against the obvious mainstream alternatives for this app.
4. State a recommendation with the tradeoff: why this tool fits, why it might not, and what to use instead if the constraints change.

## Arsenal Map

- **Biome**: JS/TS formatter and linter candidate.
- **Coolify**: self-hosted PaaS candidate for VPS/server ownership.
- **SerpApi**: search-engine results API candidate.
- **Depot**: CI, Docker build, and GitHub Actions acceleration candidate.
- **PocketBase**: compact self-hosted backend candidate for small and midsize apps.
- **Render**: managed PaaS candidate for apps, workers, static sites, and managed datastores.
- **Neon**: serverless Postgres candidate with branching/autoscaling.
- **Supabase**: Postgres-backed backend platform candidate with auth, storage, realtime, and edge functions.
- **Drizzle**: TypeScript SQL-like ORM/query builder candidate.
- **Fallow**: TypeScript/JavaScript codebase intelligence candidate.
