---
name: neatify-code
description: Neatify bounded code by improving maintainability while preserving behavior. Use when the developer asks to clean up code without behavior changes, or when a review needs maintainability findings.
---

# Skill: Neatify Code

## Scope

Improve or assess a bounded area of code while preserving current behavior: 
outputs, side effects, error behavior, and public contracts. Default to
the changed code or the developer-selected area. A repository-wide
cleanup requires confirmation.

Do not change public APIs, persistent data shape, authorization behavior,
external contracts, generated files, or architecture boundaries without
explicit approval.

## Required Context

Read only context relevant to the selected scope:

- root or nearest `AGENTS.md`, when present;
- project instructions such as `README`, `CONTRIBUTING`, development guides,
  architecture docs, conventions docs, ADRs, or domain-language docs, when
  relevant and present;
- relevant source, tests, contracts, schemas, generated-file markers, and API
  documentation.

For JavaScript or TypeScript projects where Fallow is already available or
approved, also read [references/fallow.md](references/fallow.md).

Completion criterion: enough local context is loaded to name the behavior
contract, the maintainability concern, and the checks that can verify unchanged
behavior.

## Neatify Principles

Simplify and refine code for clarity, consistency, and maintainability while
preserving exact behavior. Focus on recently modified code unless the developer
selects a broader scope.

- Prefer readable, explicit code over clever compression.
- Reduce unnecessary complexity, nesting, redundancy, and incidental
  abstraction.
- Remove comments that restate obvious code; keep comments that carry
  non-obvious intent, invariants, or constraints.
- Avoid nested ternaries and dense one-liners when a simple branch or helper is
  easier to read.
- Preserve helpful abstractions that clarify ownership, variation, or
  verification boundaries.
- Do not combine too many concerns into one function, component, service, or
  module.

Before applying a simplification, check:

- Is the resulting behavior demonstrably the same?
- Is the new version easier to understand for a maintainer who knows the
  project?
- Did this remove real complexity, or just move it elsewhere?
- Did this improve locality without creating a larger hidden dependency?
- Did this keep domain policy, validation, authorization, and persistence
  responsibilities in their accepted homes?

## Procedure

### 1. Establish Scope And Authority

Identify:

- reviewed or edited baseline;
- files, symbols, or feature slice in scope;
- whether edits are allowed or findings should be reported first;
- behavior and interfaces that must remain unchanged;
- project verification commands that are proportionate.

In review context, report maintainability findings before editing unless the
developer explicitly requested fixes.

If the scope is broad or findings are likely to exceed one coherent change,
triage first and ask the developer to select the slice to handle now.

Completion criterion: the target slice, edit authority, preserved contracts,
and verification plan are explicit.

### 2. Collect Static Evidence First

Use cheap deterministic evidence before deep manual refactoring or broad source
reading:

- project typecheck, lint, formatter check, test discovery, dead-code,
  dependency, or complexity tools when configured and cheap;
- for JavaScript or TypeScript, Fallow when already available or when the
  developer approves a policy-compliant install, selecting commands per
  [references/fallow.md](references/fallow.md): a broad routing pass first,
  then cleanup-specific passes when useful.

Prefer machine-readable tool output when available. Treat static findings as
evidence, not commands.

Completion criterion: configured cheap checks have either produced routing
evidence or been skipped for a stated reason.

### 3. Route From Broad Evidence To Narrow Context

Static output is a routing map, not a complete answer.

For each top target or suspected cleanup slice:

- use codegraph when available to inspect the relevant symbols, callers,
  callees, impact, and nearby structure; otherwise use repository-native
  search, language tooling, dependency graphs, tests, and direct source reading
  for the same follow-up;
- read only the routed source, relevant tests/contracts, and relevant accepted
  design docs needed to judge behavior preservation;
- verify a flagged unused file or export is not a static entry, generated or
  test artifact, external API, plugin hook, framework convention, or
  runtime-loaded path before reporting it as real dead code;
- avoid a full manual sweep after static routing unless the task explicitly
  requires repository-wide coverage or the evidence suggests a cross-cutting
  concern.

Completion criterion: each candidate finding is tied to source context,
callers/tests/contracts when relevant, and a false-positive check.

### 4. Triage Findings

Classify issues as:

- fix now: changed-code maintainability risk, unsafe duplication, dead code,
  excessive complexity, or project-standard mismatch in scope;
- candidate: useful refactor with clear behavior-preservation evidence;
- defer: broad historical cleanup, noisy generated/config/test duplication, or
  work outside the selected slice;
- needs decision: accepted duplication, intentional complexity, API migration,
  architecture boundary change, or unclear behavior.

Document accepted exceptions at the right durability:

- local report for one-off or task-local decisions;
- existing project convention docs for recurring project conventions;
- existing ADR or decision-log location only for durable architectural
  exceptions or choices whose rationale will matter later;
- ask before creating new durable documentation if the project has no obvious
  convention for it.

Completion criterion: every finding in scope is classified as fix now,
candidate, defer, needs decision, or false positive.

### 5. Refactor Or Report

When edits are allowed, make the smallest coherent behavior-preserving
improvement using the Neatify Principles. Prefer tests at useful behavior or
interface boundaries instead of brittle internal details.

Completion criterion: edits or reported findings are limited to one coherent
slice and each claimed improvement has behavior-preservation evidence.

### 6. Route Work That Is No Longer Cleanup

Stop when evidence shows the work is not straightforward behavior-preserving
refactoring:

- architecture diagnosis or a bounded deep-module redesign that needs design
  before code changes;
- uncertain expected behavior, regressions, or consequential blast radius
  across callers, data, contracts, security, or external systems.

Report the evidence and ask the developer before proceeding. Use a more
specific available skill only when it matches the new task and the developer's
request authorizes that direction.

Completion criterion: any non-cleanup work is explicitly stopped, reported, and
left unmodified unless approval is given.

### 7. Verify And Report

Run the narrowest useful checks first. Never claim behavior preservation unless
verification actually ran or the remaining evidence gap is explicit.

Report:

- scope handled;
- static tools used, including Fallow/codegraph commands when applicable, and
  important findings handled, deferred, rejected as false positives, or
  accepted;
- files changed or findings reported;
- verification commands and results;
- remaining risks, deferred cleanup, and any documentation or ADR follow-up.

Completion criterion: the final report accounts for the handled scope, checks
run or skipped, evidence gaps, and deferred work.

## Guardrails

- Do not optimize for fewer lines at the expense of clarity.
- Do not extract abstractions for hypothetical reuse.
- Do not hide complexity by moving it elsewhere.
- Do not merge frontend components merely to create a larger test target.
- Do not hide domain policy inside generic services.
- Do not silently broaden cleanup beyond the selected task or changed code.
- Do not treat Fallow, linters, or codegraph output as a substitute for
  understanding project behavior.
