---
name: my-dev-ops
description: Operational work — deployment, release, hosting, infrastructure, environments, CI/CD, GitHub or source-control administration, package publishing, monitoring, incident follow-up, runtime configuration — preferring CLIs over MCP integrations. Use when doing any of that work, or when choosing between a CLI and an MCP tool for an operation.
---

# My Dev Ops

Prefer available CLI tools over MCP calls when a CLI can perform the operation reliably: lower token overhead, reproducible actions, an auditable trail.

## Tool Preference

Order of preference:

1. A project-provided command or script.
2. The official CLI for the service or platform.
3. A standard local CLI such as `git`, `gh`, `docker`, `kubectl`, `terraform`, `vercel`, `aws`, `gcloud`.
4. An MCP integration or connector.

Use MCP only when:

- No suitable CLI is available.
- The MCP tool is materially more reliable, complete, or safer for the specific operation.
- The user explicitly requests that MCP tool.
- The task requires data only exposed through the MCP integration in the current environment.

If the relevant CLI is missing, suggest configuring or installing that CLI before suggesting MCP installation, unless the project or user prefers MCP for that service.

## Authority Boundary

This skill does not by itself authorize destructive operations, production actions, deployments, commits, pushes, dependency installation, billing changes, permission changes, or secret changes.

Do not edit methodology, agent-policy, or project-governance files (`AGENTS.md`, `CLAUDE.md`, `.agent/`, runbooks, policy docs) during ordinary operational work unless the user explicitly asks for that change.

## Required Context

Before consequential operational work, read the applicable local context: agent and repository instructions; the project's own development, test, release, deployment, and rollback commands (package scripts, Makefiles, workflow files, runbooks); and official technical docs when the action could affect data, security, cost, availability, or production state.

Read only the context the operation needs — a targeted command or config file beats broad repository exploration.

## Approval and Safety

Consequential actions include production deploys, releases, rollbacks, database or infrastructure changes, secret or environment-variable changes, permission changes, domain or DNS changes, billing-impacting changes, commits, pushes, merges, tags, package publishes, and destructive cleanup.

Before any consequential action, state:

- Target system, project, repository, account, branch, environment, or service.
- Command or tool to be used.
- Expected effect.
- Required approval.
- Rollback or recovery path when relevant.

For read-only inspection, run direct CLI queries and summarize the relevant results.

## Dependency Installation

Do not install dependencies unless the user or project rules permit it. Before installing a package or CLI plugin, verify the package and version against the age window required by the active project or agent instructions. If installation is not allowed or not worth the risk, use an already available local command, official web docs, or ask the user to install it.

## Procedure

1. Identify the operational target and risk level.
2. Read the minimum required project and operational context.
3. Choose the lowest-overhead reliable CLI path.
4. State any consequential action before executing it, per [Approval and Safety](#approval-and-safety).
5. Run read-only checks first when useful.
6. Execute approved changes.
7. Verify the outcome with the appropriate command, status page, logs, workflow state, or local check.
8. Report: the operational target; the tool path chosen (and why MCP was or was not used, when relevant); commands attempted and their results; approvals obtained; remaining risks, rollback notes, or follow-up.

Completion criterion: the outcome is verified by an actual check (not assumed from command exit), and the report accounts for every consequential action taken.
