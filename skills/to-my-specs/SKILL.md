---
name: to-my-specs
description: Turn conversational agent context into product/business intent specs for an app or integratable system. Use only when explicitly invoked by an engineer to create or update project specs, especially a specs/ directory, from stated product intent rather than repository implementation details. Do not use implicitly during normal task execution.
---

# To My Specs

## Purpose

Use this skill to create or update specs that record the intended product, business, and integration behavior of an application.

Specs are not implementation plans. They describe what the product or system is meant to be true for users, customers, operators, partners, or integrators.

## Invocation Rule

Use this skill only when the engineer explicitly invokes it, for example with `$to-my-specs` or a direct request to use the `to-my-specs` skill.

Do not read project specs by default during unrelated implementation tasks. Treat a project `specs/` directory as optional product/business intent context that may be absent, partial, or stale.

## Source Rules

Write specs from conversational context about the intention behind the application as a product or integratable system.

Allowed sources:

- The current conversation and explicit user statements.
- Existing specs the user asks to update or reconcile.
- Product, business, customer, workflow, market, integration, or operational intent provided outside the implementation.
- Clarifications from the user.

Disallowed sources:

- Inferring product intent from repository code, tests, schemas, routes, UI components, infrastructure, or commit history.
- Treating implementation details as evidence of intended product behavior.
- Reverse-engineering missing intent from technical architecture.

If code or other implementation artifacts are relevant for file placement or mechanical editing, use them only for that mechanical purpose. Do not derive spec statements from them.

## Spec Test

Include a statement only when both checks pass:

1. A product owner could assert it without choosing how the product is built.
2. It would remain true if the implementation were replaced.

Reject or rewrite statements that choose libraries, data models, APIs, database structure, component hierarchy, hosting, internal algorithms, or other construction choices.

## What To Capture

Prefer product/business language for:

- User, customer, operator, partner, or integrator goals.
- Product capabilities and constraints.
- Business rules and policy decisions.
- Workflow outcomes and lifecycle states.
- Permissions, roles, accountability, and audit needs when they are product requirements.
- Integration promises, external contracts, and interoperability expectations.
- Success criteria, acceptance boundaries, and non-goals.
- Open questions where intent is not yet known.

## What To Avoid

Do not write:

- Implementation plans, tasks, tickets, milestones, or engineering approaches.
- Technical architecture unless the user states a product-level integration contract that must survive implementation replacement.
- Details copied or inferred from code.
- Overconfident requirements when the conversation only implies a possibility.
- "Current implementation does X" unless the user explicitly wants an implementation note outside the spec.

## Workflow

1. Identify the intended spec scope from the explicit request.
2. Gather only allowed context. If necessary context is missing, ask concise clarification questions or mark open questions.
3. Draft or update specs in product/business terms.
4. Separate confirmed intent from open questions and optional future considerations.
5. When editing files, preserve existing product intent unless the user explicitly supersedes it.
6. Flag stale or implementation-derived spec content instead of silently accepting it.

## Suggested Spec Shape

Use the project's existing spec structure when present. If no structure exists, prefer concise Markdown under `specs/`.

Useful sections:

- Purpose
- Product Context
- Actors
- Capabilities
- Business Rules
- Workflows
- Integration Expectations
- Non-Goals
- Open Questions

Omit sections that do not apply. Keep specs clear enough that another engineer can implement from them without the spec choosing the implementation.
