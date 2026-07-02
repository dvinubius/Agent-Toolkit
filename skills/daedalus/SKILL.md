---
name: daedalus
description: User-invoked deliberate-practice workflow that seals ready-to-present coding work, then carves it into TODO challenges.
disable-model-invocation: true
---

# Daedalus

Daedalus starts from ready-to-present coding work, then carves a maze from the known-good solution.

The developer may choose the exact work they want to practice. Preserve that agency. Any sealed solution remains private unless the user explicitly exits the challenge or asks to reveal it.

Daedalus creates the challenge. If the user asks for a hint on a TODO or explicitly invokes [`Socrates`](../socrates/SKILL.md) for that TODO, use Socrates for that help request.

## Configuration

Defaults:

```yaml
difficulty: low
challenge_volume: low
```

`difficulty` controls inference distance:

- `low`: local expressions, small conditionals, straightforward return values, simple assertions.
- `medium`: helper bodies, validation branches, state transitions, adapters, non-trivial tests.
- `high`: core logic, algorithms, edge cases, async/concurrency/caching coordination, type or schema modeling.

`challenge_volume` controls how many reconstruction tasks the developer receives:

- `low`: 1-2 TODOs.
- `medium`: 3-5 TODOs.
- `high`: 6-8 TODOs.

## Activation Boundary

Daedalus begins only when the underlying development work would otherwise be ready to present to the engineer.

If this skill is read before that point, do no Daedalus-specific planning, selection, TODO design, or challenge framing yet.

At the ready-to-present point, do not present the complete implementation. Seal the solution and carve the challenge instead.

Daedalus does not define how to verify the completed solution and does not run verification commands on its own. It only records whatever readiness work already happened before challenge time. During the challenge, evaluate the developer's work analytically against the sealed solution, the visible requirements, and the acceptance criteria.

## Challenge-Time Steps

### 1. Frame the Maze

At challenge time, gather only the context needed to carve the exercise. Ask only when missing information would make the exercise unclear.

Before sealing or carving, ask the developer whether they have a specific challenge in mind. Also state the active settings and ask for confirmation:

```yaml
difficulty: <low|medium|high>
challenge_volume: <low|medium|high>
```

Identify:

- Expected behavior and acceptance criteria.
- Relevant files and conventions.
- What readiness work, if any, was performed before carving.
- Requested `difficulty`, `challenge_volume`, and visibility preference.
- Any specific parts the developer said they want to tackle personally.

Completion criterion: the implementation target, confirmed configuration, pre-carve readiness work, and developer-selected practice areas are explicit enough to carve the maze.

### 2. Seal the Solution

Keep enough private reference to restore or evaluate the completed implementation, without exposing it as the answer.

Acceptable sealing methods include reasoning context, local diff awareness, a private patch, or another environment-appropriate reference. Do not commit, publish, or display the full answer unless the user explicitly asks.

Completion criterion: the agent can compare the carved challenge against the known-good solution, and the user has not been shown the completed answer.

### 3. Carve Fair TODOs

If the developer named specific functions, files, branches, or tests they want to write themselves, carve those areas. Otherwise choose points using the configuration.

Prefer points that:

- Teach something central to the original task.
- Preserve enough surrounding context for inference.
- Have clear acceptance criteria.
- Can be evaluated analytically from the sealed solution, visible code, and acceptance criteria.
- Keep the rest of the repository understandable.

Honor developer-selected points even when they are not ideal by the agent's criteria.

Each TODO must be:

- Derived from the known-good solution.
- Behavioral, not merely syntactic.
- Fair from surrounding code, tests, comments, and original requirements.
- Small enough to complete independently.
- Matched to the requested difficulty and volume.

Prefer stubs that fail clearly over silent incorrect behavior. Preserve buildability when possible, but allow targeted compile or type failures when they point directly to the missing work.

Completion criterion: the challenge version contains deliberate `TODO(daedalus)`-style blanks, each with a clear behavioral label and enough local context to reconstruct it.

## Difficulty Matrix

| Difficulty | Volume | Result |
|---|---:|---|
| low | low | 1-2 simple local blanks |
| low | medium | 3-5 simple local blanks |
| low | high | 6-8 simple blanks across the touched area |
| medium | low | 1-2 meaningful helper or branch blanks |
| medium | medium | 3-5 behavioral TODOs with focused review criteria |
| medium | high | 6-8 TODOs spanning implementation and tests |
| high | low | 1-2 core reasoning challenges |
| high | medium | 3-5 substantial reconstruction points |
| high | high | 6-8 workshop-level challenges with a review map |

## TODO Markers

Match the project language and conventions. Prefer explicit failing stubs.

TypeScript:

```ts
// TODO(daedalus): Reject requests without a project name.
// See: createProject.test.ts, "rejects missing project name".
throw new Error("TODO(daedalus): implement project-name validation");
```

Python:

```python
# TODO(daedalus): Retry transient failures with exponential backoff.
# See: test_retry_backoff.py::test_retries_transient_errors
raise NotImplementedError("TODO(daedalus): implement retry backoff")
```

Rust:

```rust
// TODO(daedalus): Look up cached entries before recomputing.
todo!("daedalus: implement cache lookup")
```

A TODO should usually include:

- A short behavioral label.
- The expected behavior.
- A pointer to the relevant review criterion.
- A hint only when needed for fairness.

## Analytical Review

For every TODO, provide review criteria the agent can use to evaluate the developer's reconstruction analytically:

- Required behavior.
- Inputs, outputs, state changes, or errors to inspect.
- Relevant edge cases.
- Relevant invariants and constraints.
- The surrounding code or test names that express the contract, if useful.

Do not run tests or verification commands as part of Daedalus attempt review. Inspect the code, compare it to the sealed solution and acceptance criteria, and explain whether it satisfies the TODO. The agent may mention commands the surrounding workflow normally uses, but should not run them unless the user explicitly asks or a non-Daedalus instruction requires it.

Review prompt shape:

```markdown
Review my implementation of the Daedalus TODOs in `<files>`.
Evaluate it against these acceptance criteria:
- `<criterion 1>`
- `<criterion 2>`
- `<criterion 3>`
Do not replace my code unless necessary. First explain what is correct, what is incomplete, and what I should reconsider.
```

Review map shape:

```markdown
| TODO | Review criteria | Optional final verification |
|---|---|---|
| 1 | Parser edge cases and error handling | Same readiness work used before carving |
| 2 | Type model matches surrounding domain objects | Same readiness work used before carving |
| 3 | UI state and accessibility behavior | Same readiness work used before carving |
```

## Deliver the Challenge

Final response shape:

````markdown
Implemented and converted the task into a Daedalus challenge.

Configuration:

```yaml
difficulty: low
challenge_volume: low
```

## Your TODOs

- [ ] `<todo summary>` in [`path/to/file.ext`](path/to/file.ext).
  - Review criteria: `<behavior, edge cases, and relevant contract>`

## Review

Ask me to review your attempt after you fill any TODO. I will inspect it analytically against the sealed solution and the listed criteria.

After all TODOs are complete, I will offer the same level of verification that was used before this became a Daedalus challenge: `<pre-carve readiness work, or analytical review only if none was run>`.

## Need a hint?

Ask for a hint on any TODO by number. I will use Socrates for that help request before giving code.
````

If the environment supports clickable file links, use them. Otherwise include exact paths and line references.

Do not include the sealed implementation in the final response.

Completion criterion: the user can open the listed files, fill each TODO, request analytical review, and request hints without receiving the hidden solution by accident.

## Follow-Up Handling

When the user asks for a hint on a specific TODO or explicitly invokes Socrates for that TODO, invoke [`Socrates`](../socrates/SKILL.md). Do not reveal the missing code first.

When the user asks for the answer, do not refuse, but treat direct reveal as exiting or suspending Daedalus for that TODO. If the request is not explicit, ask for confirmation before revealing:

```markdown
I can reveal it, but that exits Daedalus for this TODO. Do you want me to show the solution?
```

When the user submits an attempt:

1. Inspect the attempted code analytically against the sealed solution and review criteria.
2. Identify what is correct.
3. Identify the smallest failing issue.
4. If all TODOs now appear complete, offer the same verification performed before carving, and no more.
5. Ask whether the user wants a hint if they are still blocked.
6. Provide a direct fix only if the user exits the challenge or asks explicitly.

## Challenge Completion

Challenges can be completed as a success or an explicit exit requested by the dev.

A Daedalus challenge is successful when:

- The underlying coding task reached its normal ready-to-present point before blanks were created.
- The carved TODOs match the requested difficulty and volume.
- Each TODO is file-linked and behaviorally specified.
- Each TODO has clear analytical review criteria.
- The sealed answer can be restored by completing the TODOs.
- After all TODOs are completed, the agent offers the same verification used before carving, and no more.
- The exercise feels like meaningful coding practice, not busywork.
