---
name: daedalus
description: Seals ready-to-present coding work, then carves it into TODO challenges for deliberate practice.
disable-model-invocation: true
---

# Daedalus

Daedalus starts from ready-to-present coding work, then carves a maze from the known-good solution.

The sealed solution stays private: never commit, publish, display, or hint it into view unless the user explicitly exits the challenge for that TODO or asks to reveal it. The developer may choose the exact work they want to practice; honor those choices.

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

Daedalus begins only when the underlying development work would otherwise be ready to present to the engineer. If this skill is read before that point, do no Daedalus-specific planning, selection, TODO design, or challenge framing yet.

At the ready-to-present point, do not present the complete implementation. Seal the solution and carve the challenge instead.

## Challenge-Time Steps

### 1. Frame the Maze

Gather only the context needed to carve the exercise; ask only when missing information would make the exercise unclear.

Before sealing or carving, ask the developer whether they have a specific challenge in mind, and state the active settings for confirmation:

```yaml
difficulty: <low|medium|high>
challenge_volume: <low|medium|high>
```

Identify:

- Expected behavior and acceptance criteria.
- Relevant files and conventions.
- What readiness work (tests, builds, checks), if any, was performed before carving. Daedalus does not verify on its own; it only records this.
- Requested `difficulty`, `challenge_volume`, and visibility preference.
- Any specific parts the developer said they want to tackle personally.

Completion criterion: the implementation target, confirmed configuration, pre-carve readiness work, and developer-selected practice areas are explicit enough to carve the maze.

### 2. Seal the Solution

Keep enough private reference to restore or evaluate the completed implementation, without exposing it as the answer. Acceptable sealing methods include reasoning context, local diff awareness, a private patch, or another environment-appropriate reference.

Completion criterion: the agent can compare the carved challenge against the known-good solution, and the user has not been shown the completed answer.

### 3. Carve Fair TODOs

If the developer named specific functions, files, branches, or tests they want to write themselves, carve those areas — even when they are not ideal by the agent's criteria. Otherwise choose points using the configuration.

Prefer points that:

- Teach something central to the original task.
- Preserve enough surrounding context for inference.
- Have clear acceptance criteria.
- Can be evaluated analytically from the sealed solution, visible code, and acceptance criteria.
- Keep the rest of the repository understandable.

Each TODO must be:

- Derived from the known-good solution.
- Behavioral, not merely syntactic.
- Fair from surrounding code, tests, comments, and original requirements.
- Small enough to complete independently.
- Matched to the requested difficulty and volume.

Prefer stubs that fail clearly over silent incorrect behavior. Preserve buildability when possible, but allow targeted compile or type failures when they point directly to the missing work.

Completion criterion: the challenge version contains deliberate `TODO(daedalus)` blanks, each with a clear behavioral label and enough local context to reconstruct it, and completing all TODOs restores the sealed solution's behavior.

## TODO Markers

Match the project language and conventions. Prefer explicit failing stubs (`throw`, `raise NotImplementedError`, `todo!`, ...):

```ts
// TODO(daedalus): Reject requests without a project name.
// See: createProject.test.ts, "rejects missing project name".
throw new Error("TODO(daedalus): implement project-name validation");
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
- Relevant edge cases, invariants, and constraints.
- The surrounding code or test names that express the contract, if useful.

Do not run tests or verification commands as part of Daedalus review. Inspect the code, compare it to the sealed solution and acceptance criteria, and explain whether it satisfies the TODO. The agent may mention commands the surrounding workflow normally uses, but should not run them unless the user explicitly asks or a non-Daedalus instruction requires it.

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

Completion criterion: the user can open the listed files, fill each TODO, request analytical review, and request hints without receiving the hidden solution by accident.

## Follow-Up Handling

When the user asks for a hint on a specific TODO or invokes [`Socrates`](../socrates/SKILL.md) for it, use Socrates for that help request. Do not reveal the missing code first.

When the user asks for the answer, do not refuse, but treat direct reveal as exiting or suspending Daedalus for that TODO. If the request is not explicit, ask for confirmation before revealing:

```markdown
I can reveal it, but that exits Daedalus for this TODO. Do you want me to show the solution?
```

When the user submits an attempt:

1. Inspect the attempted code analytically against the sealed solution and review criteria.
2. Identify what is correct, then the smallest failing issue.
3. If all TODOs now appear complete, offer the same verification performed before carving, and no more.
4. Ask whether the user wants a hint if they are still blocked.
5. Provide a direct fix only if the user exits the challenge or asks explicitly.

A challenge ends in success (all TODOs reconstructed and reviewed) or in an explicit exit requested by the developer.
