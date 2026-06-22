# Web App Arsenal Reference

Last researched: 2026-06-22. Use current official docs before production decisions, pricing estimates, or installs.

## Biome

Official: https://biomejs.dev/

What it is: a Rust-based web toolchain focused on formatting, linting, and project checks for JavaScript, TypeScript, JSX/TSX, JSON, HTML, CSS, and GraphQL.

Consider when:
- The project wants one fast formatter/linter command for JS/TS web code.
- CI time or editor latency from ESLint/Prettier is a real annoyance.
- The repo can accept Biome's formatting output and rule set.

Pros:
- Very fast formatter and linter with a single `check` workflow.
- Low setup cost and useful default behavior.
- Good fit for new TypeScript, React, and frontend-heavy repos.
- Can simplify tool sprawl by replacing some ESLint/Prettier usage.

Cons:
- Does not cover every language/framework formatting case that Prettier covers.
- ESLint still has a larger ecosystem for custom rules and framework-specific plugins.
- Migration may produce broad formatting diffs.
- Its stricter parser and formatting choices can differ from Prettier, so run a small migration diff before committing.

Alternatives to consider:
- Prettier plus ESLint when plugin compatibility or ecosystem convention matters more than speed.
- Framework-integrated lint defaults when the app already depends on them and the setup is stable.

## Coolify

Official: https://coolify.io/docs/

What it is: an open-source, self-hosted PaaS for deploying apps, services, and databases to servers over SSH, with Git integrations, Docker-compatible services, SSL, backups, PR deploys, and an API.

Consider when:
- The user wants VPS ownership, lower lock-in, or self-hosted infrastructure.
- The app can tolerate the team owning server health, upgrades, security patches, backups, and incident response.
- Docker-compatible deployment is already natural for the project.

Pros:
- Strong control and portability: apps and data live on the user's servers.
- Useful one-click service and database deployment for small teams.
- Good for hobby, indie, internal, and cost-sensitive projects where ops skill exists.
- Can deploy many frameworks and services without committing to one cloud PaaS.

Cons:
- Self-hosting moves operational responsibility onto the team.
- Reliability depends on the chosen server, backup setup, monitoring, and maintenance discipline.
- Less hands-off than Render, Fly.io, Railway, Vercel, Netlify, Heroku, or cloud-managed services.
- Not ideal when the team wants a vendor to own production uptime and platform security.

Alternatives to consider:
- Render/Railway/Fly.io/Heroku for managed app hosting.
- Vercel/Netlify for frontend-first apps.
- AWS/GCP/Azure when enterprise controls or cloud-native managed services dominate.

## SerpApi

Official: https://serpapi.com/

What it is: hosted APIs for search-engine and marketplace result data, including Google Search, Images, News, Maps, Shopping, Scholar, Bing, DuckDuckGo, Amazon, eBay, and others.

Consider when:
- The app needs structured search result data and cannot rely on a first-party API.
- Avoiding scraper maintenance, proxy rotation, parsing breakage, and legal uncertainty is worth paying for.
- The data use is lawful and compatible with the product's compliance posture.

Pros:
- Broad coverage across many search engines and vertical APIs.
- Removes much of the engineering burden of scraping and parsing SERPs.
- Published plans define search quotas and throughput.
- Offers compliance/security features on higher tiers, including privacy modes and legal-shield language for lawful public search collection.

Cons:
- Can become expensive at high query volume.
- External dependency for a user-visible data path; handle latency, caching, quotas, and failures.
- Legal shield does not make downstream data use automatically legal.
- Prefer official provider APIs when they exist and satisfy the product need.

Alternatives to consider:
- First-party APIs such as Google Programmable Search, Bing Web Search, marketplace APIs, or data-provider APIs.
- A search index such as Meilisearch, Typesense, Elasticsearch/OpenSearch, Algolia, or Postgres full-text search when the data is owned by the app.

## Depot

Official: https://depot.dev/

What it is: a CI and build acceleration platform for Docker builds, Depot CI, and faster GitHub Actions runners, with caching, parallel steps, SSH debugging, multi-arch builds, and per-second billing.

Consider when:
- Docker builds or CI duration are a repeated productivity bottleneck.
- The repo builds multi-architecture images or has expensive dependency/build caches.
- The team wants to keep familiar CI workflows while improving speed.

Pros:
- Strong fit for slow Docker builds and large CI workloads.
- Native Intel/Arm container builds and automatic layer caching.
- Can reduce feedback loops for agent-heavy or high-commit development.
- Debugging and cache behavior can be better than generic CI runners.

Cons:
- Adds a paid CI/build vendor and account setup.
- Small apps may not have enough CI pain to justify the dependency.
- Migration requires reviewing secrets, permissions, workflow parity, and build reproducibility.
- Do not treat faster CI as a substitute for trimming unnecessary build steps.

Alternatives to consider:
- GitHub Actions with better caching, self-hosted runners, BuildKit registry cache, Docker Build Cloud, CircleCI, Buildkite, or cloud-native CI.

## PocketBase

Official: https://pocketbase.io/faq/

What it is: a self-hosted backend built around embedded SQLite, auth, realtime APIs, file storage, admin UI, and extensibility through Go or JavaScript.

Consider when:
- The app is small to midsize, internal, indie, local-first-ish, or a prototype that benefits from a single portable backend.
- Vertical scaling on one server is acceptable.
- The team values simple deployment over managed distributed architecture.

Pros:
- Fast path to a complete backend without assembling Postgres, auth, storage, and realtime separately.
- Portable self-hosted model with a small operational footprint.
- Good fit for demos, MVPs, intranets, mobile API backends, and modest SaaS products.
- SQLite can be excellent for read-heavy small/midsize apps.

Cons:
- Official FAQ says it is a personal open-source project with limited scope and no promised maintenance/support.
- Self-hosted only; no official hosted PocketBase service.
- Scales vertically on a single server rather than horizontally.
- Uses SQLite only out of the box; no built-in Postgres/MySQL replacement.
- Does not provide cloud functions; custom logic lives in the PocketBase app/framework.

Alternatives to consider:
- Supabase or Firebase when managed auth/storage/realtime and hosted operations matter.
- Plain Postgres plus a backend framework when relational scale, reporting, and operational maturity matter.
- Django/Rails/Laravel when a conventional full-stack backend is a better long-term fit.

## Render

Official: https://render.com/docs

What it is: a managed cloud platform for deploying and scaling web services, static sites, background workers, cron jobs, private services, managed Postgres, Redis-compatible key-value stores, persistent disks, infrastructure-as-code, logs, metrics, and health checks.

Consider when:
- The app needs a managed PaaS for backend services, workers, databases, and static sites without running servers directly.
- The team wants repo-connected deploys, rollbacks, logs, metrics, custom domains, and private networking.
- Simplicity matters more than maximum cloud-specific control.

Pros:
- Broad app-hosting surface for full-stack products, not just static/frontend deployments.
- Managed datastores and persistent disks are available from the same platform.
- Operational tools include scaling, rollbacks, health checks, logs, metrics, notifications, REST API, CLI, Terraform, and Blueprints.
- Good general-purpose option when Heroku-like simplicity is wanted.

Cons:
- May be less specialized than Vercel/Netlify for frontend-edge workflows.
- May be less flexible than AWS/GCP/Azure for enterprise networking, compliance, and specialized managed services.
- Managed convenience can cost more than a tuned VPS at steady low scale.
- Check current plan limits, regions, cold-start behavior, and database features before committing.

Alternatives to consider:
- Vercel/Netlify for frontend-first apps.
- Fly.io/Railway for different deployment ergonomics.
- Coolify on a VPS when self-hosting and control are the point.
- AWS/GCP/Azure for enterprise cloud requirements.

## Neon

Official: https://neon.com/docs/introduction

What it is: serverless Postgres with autoscaling, database branching, instant restore, extensions, CLI/API integrations, and framework/ORM guides.

Consider when:
- The app needs Postgres and benefits from serverless scaling, preview/dev database branches, or fast restore.
- The rest of the backend stack is already handled elsewhere.
- Branch-per-preview workflows matter for agent or PR-heavy development.

Pros:
- Real Postgres with a strong developer experience.
- Branching is useful for tests, previews, migrations, and isolated agent work.
- Autoscaling/serverless model can fit spiky or early-stage workloads.
- Strong fit with TypeScript stacks, Drizzle, Next.js, and modern serverless deployments.

Cons:
- It is primarily a database platform, not a complete backend suite.
- If the app needs managed auth, storage, realtime, functions, and dashboard policies together, Supabase may be a better default.
- Serverless Postgres still requires attention to connection pooling, cold paths, latency, and plan limits.
- Database branching can complicate operational discipline if migrations and environments are not clearly managed.

Alternatives to consider:
- Supabase for a Postgres-backed full backend platform.
- AWS RDS, Cloud SQL, Azure Database for PostgreSQL, Crunchy Bridge, or Render Postgres for more traditional managed Postgres.
- SQLite/Turso for edge/local or simpler data needs.

## Supabase

Official: https://supabase.com/docs

What it is: a Postgres-backed backend platform with database, Auth, Storage, Realtime, Edge Functions, REST/GraphQL APIs, AI/vector modules, CLI, management API, and integrations.

Consider when:
- The app needs a managed backend platform, not just a database.
- Auth, file storage, realtime, Postgres, and row-level security should work together quickly.
- A Firebase-like developer experience with SQL/Postgres underneath is attractive.

Pros:
- Mainstream, broad, and productive for web/mobile apps.
- Good fit for apps that need auth, database, storage, realtime, and server-side functions in one platform.
- Postgres foundation keeps data portable compared with document-only backend platforms.
- Strong docs, SDKs, CLI, dashboard, migrations, and migration paths from common services.

Cons:
- RLS and security policy design are production-critical; weak policies can expose or corrupt data.
- The platform has more moving parts than just using Postgres.
- If the app only needs a database, Neon/RDS/Render Postgres may be simpler.
- Free-plan and add-on limitations can matter for production availability, backups, and launch traffic.

Alternatives to consider:
- Neon plus custom auth/storage when a lean Postgres-first architecture is better.
- Firebase when the app strongly benefits from Google's managed mobile/backend ecosystem.
- Custom backend plus managed Postgres when domain logic and operational control dominate.

## Drizzle

Official: https://orm.drizzle.team/docs/overview

What it is: a lightweight TypeScript ORM/query builder with SQL-like and relational APIs, TypeScript schema definitions, migrations, Studio, validation integrations, and support across Postgres, MySQL, SQLite, serverless databases, and edge-oriented runtimes.

Consider when:
- The app is TypeScript and the team wants type-safe SQL without a heavy data framework.
- Developers know SQL and want the database model to stay visible.
- The deployment target is serverless or edge-friendly.

Pros:
- SQL-like API reduces abstraction mismatch for SQL-literate developers.
- Lightweight, flexible, and serverless-ready.
- Works well with Neon, Supabase, Postgres, SQLite/Turso, and many TypeScript stacks.
- Migrations and schema live naturally in TypeScript projects.

Cons:
- Less batteries-included than Prisma for generated clients, schema workflows, and some ecosystem conventions.
- Requires more comfort with SQL and database design.
- TypeScript-only fit; not useful for Python/Ruby/Go backend code.
- Migration discipline still matters; do not rely on an ORM to fix weak database lifecycle practices.

Alternatives to consider:
- Prisma when the team wants a more opinionated generated client and mature ecosystem.
- Kysely for a type-safe SQL query builder without ORM framing.
- Raw SQL with `postgres`, `pg`, or framework-native database tools for simpler apps.

## Fallow

Official: https://github.com/fallow-rs/fallow

What it is: a TypeScript/JavaScript codebase intelligence engine that reports unused code, duplication, complexity hotspots, dependency hygiene, architecture boundaries, PR risk, and optional runtime evidence.

Consider when:
- The project has enough JS/TS code that ordinary lint/type checks do not explain codebase-level risk.
- The team wants deterministic evidence for unused code, duplication, architectural drift, or PR review focus.
- CI or agents would benefit from structured repository context beyond file-level lint results.

Pros:
- Complements linting and type checking by analyzing the codebase as a system.
- Useful for pruning dead code and spotting architecture/dependency issues.
- Deterministic reports are easier to inspect than AI-generated guesses.
- Can provide structured repo context to agents and editor tools.

Cons:
- Newer and less mainstream than ESLint, TypeScript, dependency-cruiser, Knip, Madge, or Sonar-style tools.
- Scope is JS/TS-centric; not a general polyglot architecture analyzer.
- Findings can create CI noise unless thresholds and adoption are staged.
- Optional runtime layer may be paid or operationally invasive.
- Verify package/version age before installing; if the current release is younger than 3 weeks, pin an older acceptable version or defer.

Alternatives to consider:
- ESLint, TypeScript, Knip, dependency-cruiser, Madge, SonarQube/SonarCloud, CodeQL, or framework-specific analyzers depending on the exact risk.

## Source Notes

- Biome home and formatter docs: https://biomejs.dev/ and https://biomejs.dev/formatter/differences-with-prettier/
- Coolify docs: https://coolify.io/docs/
- SerpApi home/pricing/security details: https://serpapi.com/
- Depot home/docs entry points: https://depot.dev/
- PocketBase FAQ: https://pocketbase.io/faq/
- Render docs: https://render.com/docs
- Neon docs: https://neon.com/docs/introduction
- Supabase docs and production checklist: https://supabase.com/docs and https://supabase.com/docs/guides/deployment/going-into-prod
- Drizzle overview: https://orm.drizzle.team/docs/overview
- Fallow repository README: https://github.com/fallow-rs/fallow
