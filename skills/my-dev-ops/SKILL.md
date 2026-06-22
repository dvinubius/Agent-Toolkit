---
name: my-dev-ops
description: Handle deployment, release, infrastructure, environment, CI/CD, hosting, GitHub, package publishing, or other operational work while preferring available CLI tools over MCP integrations for token efficiency and reliability. Use when explicitly doing operational, deployment, repository administration, or runtime environment work.
---

# My Dev Ops

## Scope

Use this skill for operational work, including deployment, release, hosting, infrastructure, environments, CI/CD, GitHub or source-control administration, package publishing, monitoring, incident follow-up, and runtime configuration.

Prefer available CLI tools over MCP calls when a CLI can perform the operation reliably. The goal is to reduce token overhead, keep actions reproducible, and make operational work easy to audit.

## Authority Boundary

This skill does not authorize destructive operations, production actions, deployments, commits, pushes, dependency installation, billing changes, permission changes, or secret changes by itself.

Follow the current project, organization, repository, and agent rules. Treat files such as `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.agent/`, `.claude/`, `.codex/`, runbooks, and policy docs as authoritative when present.

Do not edit methodology, agent policy, or project-governance files during ordinary operational work unless the user explicitly asks for that change.

## Required Context

Before consequential operational work, read the applicable local context:

- Agent and repository instructions such as `AGENTS.md`, `CLAUDE.md`, or equivalent files.
- Development, test, release, deployment, and rollback commands from README files, package scripts, Makefiles, task runners, workflow files, runbooks, or deployment docs.
- Relevant project configuration, environment examples, CI/CD workflows, hosting config, infrastructure config, and operational documentation.
- Applicable official technical docs when the action could affect behavior, contracts, data, security, privacy, cost, availability, or production state.

Read only the context needed for the operation. Avoid broad repository exploration when a targeted command or config file answers the question.

## Tool Preference

Use this order of preference:

1. A project-provided command or script.
2. The official CLI for the service or platform.
3. A standard local CLI such as `git`, `gh`, `npm`, `pnpm`, `docker`, `kubectl`, `terraform`, `vercel`, `netlify`, `flyctl`, `aws`, `gcloud`, or `az`.
4. An MCP integration or connector.

Use MCP only when:

- No suitable CLI is available.
- The MCP tool is materially more reliable, complete, or safer for the specific operation.
- The user explicitly requests that MCP tool.
- The task requires data only exposed through the MCP integration in the current environment.

If the relevant CLI is missing, suggest configuring or installing that CLI before suggesting MCP installation, unless the project or user prefers MCP for that service.

## Approval And Safety

Before any consequential operational action, state:

- Target system, project, repository, account, branch, environment, or service.
- Command or tool to be used.
- Expected effect.
- Required approval.
- Rollback or recovery path when relevant.

Consequential actions include production deploys, releases, rollbacks, database or infrastructure changes, secret or environment-variable changes, permission changes, domain or DNS changes, billing-impacting changes, commits, pushes, merges, tags, package publishes, and destructive cleanup.

For read-only inspection, prefer direct CLI queries and summarize the relevant results.

## Dependency Installation

Do not install dependencies unless the user or project rules permit it. Before installing a package or CLI plugin, verify that the package and version are not newly published within the restricted age window required by the active project or agent instructions.

If installation is not allowed or not worth the risk, use an already available local command, official web docs, or ask the user to install the dependency.

## Procedure

1. Identify the operational target and risk level.
2. Read the minimum required project and operational context.
3. Choose the lowest-overhead reliable CLI path.
4. State any consequential action before executing it.
5. Run read-only checks first when useful.
6. Execute approved changes.
7. Verify the outcome with the appropriate command, status page, logs, workflow state, or local check.
8. Report what changed, what was checked, and any remaining risk.

## Output

Report:

- Operational target.
- Tool or command path chosen, including why MCP was or was not used when relevant.
- Commands or MCP calls attempted.
- Results and checks run.
- Approvals obtained.
- Remaining risks, rollback notes, or follow-up.
