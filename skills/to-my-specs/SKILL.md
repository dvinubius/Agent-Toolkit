---
name: to-my-specs
description: Turns conversational product intent into .devnotes/specs — a three-layer system definition (intent, product spec, design), never derived from implementation details.
disable-model-invocation: true
---

# To My Specs

## Purpose

Create or update specs that record what an application is meant to be — for users, customers, operators, partners, or integrators — regardless of how it is built. Treat an existing `.devnotes/specs/` tree as intent context that may be absent, partial, or stale.

## The Three Layers

The system definition has three layers. Every candidate statement is routed to exactly one, and the layer decides where it lives.

**Intent** — why the system exists. Lives under `.devnotes/specs/intent/`.

- Goal
- Outcome constraints
- Non-goals

**Product Spec** — what the system observably does. Lives under `.devnotes/specs/product-spec/`.

- User-visible behavior
- Data behavior — what data exists, persists, and is visible to whom, as a promise to users
- UX states
- Edge cases
- Product acceptance criteria

`product-spec/` holds behavior, data behavior, edge cases, and acceptance criteria. Its `design/` subfolder holds UX states, flows, and interaction design decisions.

**Implementation** — how the system is built. Never lives under `.devnotes/specs/`.

- Architecture
- Stack
- Data model
- Integration choices
- Engineering constraints

Boundary pairs for the near-misses:

- "Users can recover deleted notes for 30 days" is data behavior; "soft-delete flag plus a nightly cleanup job" is data model.
- "Partners can export orders in a documented, stable format" is product behavior toward integrators; "we sync through the Shopify webhook API" is an integration choice.

## Routing Test

A statement belongs in `.devnotes/specs/` only when both checks pass:

1. A product owner could assert it without choosing how the product is built.
2. It would remain true if the implementation were replaced.

Statements that fail are implementation — reject or rewrite them, even when they arose while reasoning about product intent. Statements that pass route to intent when they say why (goals, outcome constraints, non-goals) and to product spec when they say what (observable behavior).

## Source Rules

Write specs from conversational context about the intention behind the application as a product or integratable system.

Allowed sources:

- The current conversation, explicit user statements, and clarifications from the user.
- Existing specs the user asks to update or reconcile.
- Product, business, customer, workflow, market, integration, or operational intent provided outside the implementation.

Never infer product intent from repository code, tests, schemas, routes, UI components, infrastructure, or commit history, and never treat implementation details as evidence of intended product behavior. Implementation artifacts may be consulted only mechanically — for file placement or editing — never as a source of spec statements.

Do not write overconfident requirements when the conversation only implies a possibility, and do not record "current implementation does X" unless the user explicitly wants an implementation note outside the spec.

## Writing Style

Use natural-language headings rather than global requirement IDs. Prefer headings that describe the product area, behavior, actor, workflow, rule, or question.

Keep coupled requirements together. When coupled requirements must live in separate files or sections, make the relationship explicit with a short note in both relevant places or in the specification map.

Keep specs clear enough that another engineer can implement from them without the spec choosing the implementation.

## Workflow

1. Identify the intended spec scope from the explicit request.
2. Gather only allowed context. If necessary context is missing, ask concise clarification questions or mark open questions.
3. Route every candidate statement through the Routing Test into its layer; drop or rewrite implementation statements.
4. Draft or update files in the layer directories, separating confirmed intent from open questions and optional future considerations.
5. Create or update `.devnotes/specs/README.md` as the specification map.
6. When editing files, preserve existing product intent unless the user explicitly supersedes it.
7. Flag stale or implementation-derived spec content instead of silently accepting it.

Completion criterion: every statement in the created or changed specs passes the Routing Test and sits in its layer's directory, no implementation statement remains anywhere under `.devnotes/specs/`, confirmed intent is separated from open questions, and `.devnotes/specs/README.md` maps every spec file.

## Specification Map

Use the project's existing spec structure when present, while maintaining the map. Template for `.devnotes/specs/README.md`:

```markdown
# Specification Map

## Product Summary

`<What the product is, who it serves, and the main outcome it provides.>`

## About This Folder

This folder holds the system definition in two layers: `intent/` — why the system exists (goal, outcome constraints, non-goals) — and `product-spec/` — what the system observably does, with UX states, flows, and interaction design in `product-spec/design/`. Implementation (architecture, stack, data model, integration choices, engineering constraints) is deliberately excluded. The folder is named "specs" for discoverability: "specs" is the broad term commonly used to cover intent and design as well.

## Current Specification Files

| Layer | Area | File | Scope | Important relationships |
|---|---|---|---|---|
| `<intent / product-spec / product-spec/design>` | `<area>` | `.devnotes/specs/<layer>/<file>.md` | `<behavior covered>` | `<coupled areas or none>` |

## Cross-Cutting Requirements

- `<requirement affecting several spec areas, or none>`

## Domain Language

`<link to the project's canonical domain-language doc, or omit this section>`

## Open Product Questions

- `<question, or none>`
```

Within a layer, use dedicated files for coherent behavior groups — product areas, workflows, actors, business rules. Omit sections that do not apply.
