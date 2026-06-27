---
name: daedalus
description: Complete a coding task, verify the working solution, then transform selected parts into a deliberate-practice coding challenge with TODOs, file-linked checklist items, and validation through tests or agent review. Integrates with Socrates for hint-based help instead of direct answers.
---

# Daedalus

## Purpose

Activate this skill when the user wants the agent to complete the coding work but also wants to retain, recover, or practice the craft of writing code themselves.

Daedalus mode has two phases:

1. **Craft the solution.** The agent implements and verifies the requested coding task as if it were solving it normally.
2. **Turn the solution into a maze.** Once the agent is confident the implementation is correct, it deliberately removes selected parts of the code and gives the developer a structured reconstruction exercise.

The goal is not to slow the developer down arbitrarily. The goal is to restore agency, taste, debugging intuition, and the pleasure of doing software engineering rather than merely receiving completed code.

Daedalus is a companion to the [`Socrates`](../socrates/SKILL.md) skill. Daedalus creates the challenge. Socrates governs how the agent helps when the developer asks for guidance.

## Mental Model

Daedalus is a master craftsperson who first builds the artifact correctly, then converts part of it into an apprentice exercise.

The agent should:

- Solve the real problem.
- Verify the solution.
- Remove selected pieces with care.
- Leave a clear path for the developer to restore correctness.
- Provide tests, commands, and acceptance criteria.
- Avoid revealing the completed answer unless the user explicitly exits the challenge.

This is **reverse code completion**: instead of filling in blanks for the developer, the agent creates meaningful blanks from a known-good implementation.

## When to Use

Use Daedalus when the user asks for any of the following:

- A coding task that should become a learning exercise.
- A partially completed implementation with TODOs for the user.
- A challenge, kata, workshop, or practice version of a feature.
- Help “not spoon-feeding” code while still making progress.
- A mode that lets the agent implement first, then remove pieces for the developer.
- A companion workflow for Socratic coding practice.

Also use it when the user says things like:

- “Make me write part of this myself.”
- “Turn this into an exercise.”
- “Leave blanks for me.”
- “Give me TODOs instead of the full implementation.”
- “I miss writing the code myself.”
- “Use Daedalus.”
- “Daedalus mode.”

## When Not to Use

Do not use Daedalus when:

- The user needs an urgent production fix with no practice component.
- The user explicitly asks for the complete implementation only.
- The task is security-sensitive, destructive, compliance-sensitive, or time-critical.
- The user is asking for explanation, not code transformation.
- The repository is in a state where creating deliberate failures would be harmful or confusing.
- The challenge would obscure critical safety, privacy, accessibility, or security requirements.

In these cases, solve directly or use [`Socrates`](../socrates/SKILL.md) if the user wants reasoning guidance.

## Default Configuration

Daedalus has two required configurable dimensions.

```yaml
difficulty: low
challenge_volume: low
```

Both default to `low`.

### Difficulty

Difficulty controls **inference distance**: how much reasoning the developer must do to reconstruct each missing part.

It does not primarily mean number of lines.

#### `difficulty: low`

Use low difficulty when the developer should perform light reconstruction.

Remove:

- Local expressions.
- Simple conditionals.
- Straightforward return values.
- Small mapping/filtering logic.
- Basic parameter passing.
- Simple error messages.
- Small test assertions.

The surrounding context should make the missing code fairly obvious.

The developer should mainly practice recognition, syntax, and local reasoning.

#### `difficulty: medium`

Use medium difficulty when the developer should perform meaningful implementation work.

Remove:

- Complete helper function bodies.
- Branching logic.
- Validation logic.
- Moderate error handling.
- State transitions.
- Adapter or mapper functions.
- Non-trivial tests.
- Integration glue between already visible components.

The developer should need to understand the surrounding design before filling the blanks.

#### `difficulty: high`

Use high difficulty when the developer should reconstruct core logic.

Remove:

- Algorithmic logic.
- Architectural glue.
- Edge-case handling.
- Multi-step control flow.
- Concurrency, caching, or async coordination logic.
- Type-level modeling or schema logic.
- Complex tests that encode behavior.
- Carefully chosen parts of the main implementation path.

The developer should need to reason from tests, invariants, and acceptance criteria.

High difficulty must still be fair: the challenge should be solvable from the codebase context, tests, and checklist.

### Challenge Volume

Challenge volume controls **how many distinct reconstruction tasks** the developer receives.

It does not measure raw lines of code.

```yaml
challenge_volume: low | medium | high
```

#### `challenge_volume: low`

Create 1–2 challenge items.

Use this when the user wants a small taste of hands-on work or when the task itself is small.

#### `challenge_volume: medium`

Create 3–5 challenge items.

Use this for a meaningful but bounded practice session.

#### `challenge_volume: high`

Create 6–8 challenge items.

Use this when the user wants a substantial reconstruction exercise.

Avoid exceeding 8 items unless the user explicitly requests a larger workshop-style challenge.

## Optional Configuration

The following settings may be used by an agent implementation, but they should not be required from the user.

```yaml
solution_visibility: sealed
validation_strategy: tests_first
socratic_help: true
```

### `solution_visibility`

Controls whether the completed implementation may be shown.

Recommended default:

```yaml
solution_visibility: sealed
```

Options:

- `hidden`: never show the completed solution during the challenge.
- `sealed`: do not show the completed solution unless the user explicitly asks to reveal it or exits Daedalus mode.
- `reveal_on_explicit_request`: reveal the completed answer when directly requested, preferably after offering one Socratic hint first.

### `validation_strategy`

Recommended default:

```yaml
validation_strategy: tests_first
```

Options:

- `tests_first`: prefer executable tests as the primary validation path.
- `agent_review`: use agent evaluation when tests are impractical.
- `hybrid`: provide tests where possible and agent review for the rest.

### `socratic_help`

Recommended default:

```yaml
socratic_help: true
```

When enabled, any request for help on a TODO should invoke the [`Socrates`](../socrates/SKILL.md) skill. The agent should provide questions and hints before revealing code.

## Core Operating Rule

Do not give the developer arbitrary blanks.

Only remove code after the agent has first produced, inspected, and validated a working implementation.

The challenge should be derived from a known-good solution, not improvised as a skeleton from the beginning.

The developer should receive:

1. Files containing TODOs, stubs, blanks, or omitted functions.
2. A checklist of missing pieces.
3. Links or precise references to the files and locations that need work.
4. Associated tests that currently fail because of the missing pieces, wherever feasible.
5. Commands to run the tests.
6. A fallback validation path when executable tests are not feasible.

## End-to-End Workflow

### 1. Understand the Task

Clarify the implementation objective only when necessary.

Identify:

- Expected behavior.
- Relevant files.
- Existing conventions.
- Test framework.
- Build commands.
- Type-checking or linting commands.
- User-specified difficulty and challenge volume.

If the user does not specify configuration, use:

```yaml
difficulty: low
challenge_volume: low
```

### 2. Implement the Complete Solution

Implement the requested coding task normally.

During this phase, the agent may:

- Edit files.
- Add tests.
- Refactor code.
- Run existing tests.
- Add new tests.
- Inspect logs and failures.
- Iterate until the implementation appears correct.

The user should not receive the final complete implementation as the main deliverable when Daedalus mode is active.

### 3. Verify the Complete Solution

Before creating blanks, the agent should establish reasonable confidence that the full solution works.

Prefer objective validation:

- Unit tests.
- Integration tests.
- End-to-end tests.
- Type checks.
- Linters.
- Build commands.
- Manual reproduction steps.
- Snapshot updates, when appropriate.
- Static analysis, where available.

If no tests exist, the agent should consider adding focused tests before removing code.

If the environment cannot run tests, the agent should still reason through validation and be transparent about what could not be executed.

### 4. Preserve the Solution Privately

The agent may use the completed solution internally as a reference while designing the challenge.

Depending on the environment, preservation may mean:

- Keeping the solution in reasoning context.
- Keeping a local patch before replacing parts with TODOs.
- Using version control diff awareness.
- Avoiding exposure of the completed answer in the final response.

Do not commit, publish, or display the full answer unless the user has asked for it.

### 5. Select Challenge Points

Choose challenge points based on `difficulty` and `challenge_volume`.

Good challenge points:

- Teach something central to the task.
- Are small enough to be completed independently.
- Have clear acceptance criteria.
- Can be validated by a test or command.
- Preserve enough context for the developer to reason.
- Avoid turning the whole codebase into a scavenger hunt.

Bad challenge points:

- Require guessing hidden intent.
- Depend on invisible implementation details.
- Break unrelated systems.
- Remove too much surrounding context.
- Require extensive boilerplate with little learning value.
- Are mainly formatting or mechanical busywork.
- Cannot be validated in any meaningful way.

### 6. Remove or Stub Selected Code

Use explicit markers such as:

```ts
// TODO(daedalus): Implement this branch.
throw new Error("TODO(daedalus): implement input validation");
```

or:

```python
raise NotImplementedError("TODO(daedalus): implement retry backoff")
```

or:

```rust
todo!("daedalus: implement cache lookup")
```

The exact marker should match the language and project conventions.

Prefer stubs that fail clearly over silent incorrect behavior.

A Daedalus TODO should usually include:

- A short label.
- The expected behavior.
- A pointer to the relevant test.
- A hint level only if appropriate.

Example:

```ts
// TODO(daedalus): Return only active users sorted by lastSeen descending.
// See: user-list.test.ts, "filters and sorts active users"
```

### 7. Create or Preserve Failing Tests

For each TODO, attempt to provide at least one associated test that fails because of the missing code and passes when the missing code is correctly implemented.

Tests should be specific enough to validate behavior but not so revealing that they fully spoon-feed the implementation.

Each challenge item should ideally include:

- Test file.
- Test name.
- Command to run it.
- Expected failure while TODO remains.
- Expected success after completion.

Example checklist item:

```markdown
- [ ] Implement active-user filtering in [`src/users/selectActiveUsers.ts`](src/users/selectActiveUsers.ts).
  - Failing test: [`src/users/selectActiveUsers.test.ts`](src/users/selectActiveUsers.test.ts) — `filters inactive users and sorts by lastSeen`
  - Run: `pnpm test src/users/selectActiveUsers.test.ts`
```

### 8. Provide a File-Linked Checklist

The final response should include a concise checklist.

Every item should point to the exact file that needs work. When possible, include line numbers or anchors according to the environment.

Checklist items should include:

- What to implement.
- Where to implement it.
- Which test validates it.
- Which command to run.
- Whether Socratic help is available.

Preferred shape:

```markdown
## Daedalus Challenge

Configuration:

```yaml
difficulty: low
challenge_volume: low
```

### Your TODOs

- [ ] Implement `<behavior>` in [`path/to/file.ext`](path/to/file.ext).
  - Validation: [`path/to/test.ext`](path/to/test.ext) — `<test name>`
  - Run: `<test command>`

- [ ] Implement `<behavior>` in [`path/to/other-file.ext`](path/to/other-file.ext).
  - Validation: [`path/to/other-test.ext`](path/to/other-test.ext) — `<test name>`
  - Run: `<test command>`

### Completion Criteria

You are done when:

- The listed TODO markers are gone.
- The associated tests pass.
- The broader test/type-check command still passes.
```

If the environment supports clickable file links, use them. If not, provide exact paths and line references.

### 9. Offer Socratic Help

When the developer asks for help with a TODO, switch to [`Socrates`](../socrates/SKILL.md).

Do not immediately reveal the missing code.

Use a hint ladder:

1. Ask what the developer thinks the missing behavior should be.
2. Point to the relevant test.
3. Ask what input/output relationship the test implies.
4. Identify the invariant or edge case.
5. Give a small pseudocode hint.
6. Provide partial code only after meaningful effort.
7. Reveal the solution only if the user explicitly asks or exits Daedalus mode.

Example:

User:

> I’m stuck on TODO 2.

Agent:

> Let’s use Socrates for this one. Look at the failing test first: what behavior is it asserting for an expired token?

## Validation Requirements

### Prefer Tests

Daedalus should strongly prefer executable validation.

For each TODO, attempt to provide at least one of:

- A unit test.
- An integration test.
- A component test.
- A CLI smoke test.
- A type-level test.
- A snapshot or fixture test.
- A manual test script.
- A reproducible command.

The associated test should fail for the intended reason while the TODO is incomplete.

### Avoid Misleading Tests

Do not create tests that:

- Fail for unrelated setup reasons.
- Depend on unavailable services unless properly mocked.
- Require secrets or production credentials.
- Are flaky by design.
- Assert implementation details unnecessarily.
- Reveal the entire solution in the test name or fixture.

### Test Granularity

For `challenge_volume: low`, one test may cover one or two TODOs.

For `challenge_volume: medium`, prefer a small cluster of focused tests.

For `challenge_volume: high`, provide a validation map showing which tests cover which TODOs.

### Fallback: Agent Evaluation

If the code is not testable in the current context, Daedalus should still give the developer a way to validate their work.

Use agent evaluation when:

- The repo has no runnable test setup.
- The environment cannot install dependencies.
- Tests require external services unavailable locally.
- The change is primarily visual, architectural, or exploratory.
- The agent cannot safely execute code.
- The task is too small or too context-bound for a meaningful test.

In this case, provide an explicit fallback:

```markdown
Validation fallback: ask the agent to review your completed TODOs against the acceptance criteria.
```

The agent review should evaluate:

- Correctness.
- Edge cases.
- Consistency with surrounding code.
- Type safety.
- Error handling.
- Security implications.
- Maintainability.
- Whether the implementation satisfies the original task.

When using fallback evaluation, the final checklist should include review prompts such as:

```markdown
After completing this TODO, ask:

> Review my implementation of TODO 1 in `src/cache/ttl.ts`.
> Do not rewrite it unless necessary. First tell me whether it satisfies the acceptance criteria.
```

### Hybrid Validation

When some TODOs are testable and others are not, use a hybrid validation map.

Example:

```markdown
| TODO | Primary validation | Fallback |
|---|---|---|
| 1 | `pnpm test src/parser.test.ts` | Agent review of parser edge cases |
| 2 | `pnpm typecheck` | Agent review of type model |
| 3 | Manual browser flow | Agent review of UI behavior |
```

## Challenge Design Rules

### Keep the Task Real

The challenge should preserve the user's original coding goal.

Do not turn the task into an artificial puzzle if the original value was a practical feature or fix.

### Preserve Context

Do not remove so much context that the developer cannot infer intent.

The surrounding code, tests, names, and comments should provide a fair path to the answer.

### Prefer Behavioral TODOs

A TODO should describe behavior, not merely syntax.

Bad:

```ts
// TODO: write code here
```

Better:

```ts
// TODO(daedalus): Normalize the email before comparing it with stored addresses.
```

### Preserve Buildability When Possible

Prefer stubs that allow the project to compile but fail targeted tests.

However, for some challenge types, compile-time failures may be appropriate, especially in strongly typed languages.

Acceptable failure types:

- A test assertion fails.
- A TODO exception is thrown.
- A type-checking test fails.
- A compile error points directly to a missing function.
- A snapshot mismatch indicates missing behavior.

Avoid broad, cascading failures that obscure the challenge.

### Avoid Destructive Blanks

Do not remove code that protects against:

- Data loss.
- Credential exposure.
- Authorization bypass.
- Injection vulnerabilities.
- Unsafe filesystem operations.
- Payment or billing errors.
- Production deployment safety checks.

For safety-critical logic, use explanation or Socratic review instead of removing the guard.

### Do Not Hide Essential Requirements

The developer should not have to guess requirements that only exist in the sealed solution.

Requirements should be inferable from:

- The original user request.
- The file names.
- The TODO comments.
- The tests.
- The checklist.
- Existing project conventions.

### Preserve Style and Conventions

The challenge code should still feel native to the repository.

Follow existing conventions for:

- Formatting.
- Naming.
- Test structure.
- Error handling.
- Dependency injection.
- Logging.
- State management.
- Comments.
- Package scripts.

## Difficulty and Volume Matrix

Use this matrix when deciding what to remove.

| Difficulty | Volume | Result |
|---|---:|---|
| low | low | 1–2 simple local blanks |
| low | medium | 3–5 simple local blanks |
| low | high | 6–8 simple blanks across the touched area |
| medium | low | 1–2 meaningful helper or branch blanks |
| medium | medium | 3–5 behavioral TODOs with focused tests |
| medium | high | 6–8 TODOs spanning implementation and tests |
| high | low | 1–2 core reasoning challenges |
| high | medium | 3–5 substantial reconstruction points |
| high | high | 6–8 workshop-level challenges with a validation map |

## Final Response Format

When Daedalus completes, respond with:

1. A brief summary of what was implemented before challenge conversion.
2. The active configuration.
3. A checklist of TODOs with file links.
4. The associated failing tests or validation steps.
5. The command sequence to validate completion.
6. A note that help will be Socratic by default.

Template:

```markdown
Implemented and converted the task into a Daedalus challenge.

Configuration:

```yaml
difficulty: low
challenge_volume: low
```

## Your TODOs

- [ ] `<todo summary>` in [`path/to/file.ext`](path/to/file.ext).
  - Failing test: [`path/to/test.ext`](path/to/test.ext) — `<test name>`
  - Run: `<command>`

## Validation

Run:

```bash
<command>
```

Expected now: the listed tests fail because of the Daedalus TODOs.

Expected after completion: the listed tests pass, and the broader check still passes.

## Need a hint?

Ask about any TODO by number. I will use Socrates mode first, so you get hints before code.
```

## Handling User Requests During a Challenge

### User asks for a hint

Invoke [`Socrates`](../socrates/SKILL.md).

Good response:

```markdown
Let’s reason through TODO 1.

The failing test gives us the contract. What input is it passing into the function, and what output does it expect?
```

### User asks for the answer

Do not refuse. But avoid revealing immediately unless the user is explicit.

First offer:

```markdown
I can reveal it, but Daedalus is designed to preserve the exercise. Would you like one stronger hint first, or should I exit Daedalus and show the solution?
```

If the user explicitly says to reveal, reveal the solution.

### User submits an attempt

Evaluate the attempt.

Prefer this order:

1. Run or inspect the relevant test if possible.
2. Identify what is correct.
3. Identify the smallest failing issue.
4. Ask a Socratic follow-up question if the user wants to keep practicing.
5. Provide a direct fix only if the user exits the challenge or asks explicitly.

### User wants the challenge made easier

Reduce difficulty or volume.

Examples:

- Replace a missing function with a partially completed function.
- Add stronger TODO comments.
- Add more explicit test names.
- Add a hint near the blank.
- Narrow the failing test.

### User wants the challenge made harder

Increase difficulty or volume.

Examples:

- Remove more implementation detail.
- Replace direct hints with behavioral comments.
- Add edge-case TODOs.
- Remove overly revealing comments.
- Ask the developer to write an additional test.

## Examples

### Example 1: Low Difficulty, Low Volume

Configuration:

```yaml
difficulty: low
challenge_volume: low
```

Result:

```ts
export function formatDisplayName(user: User): string {
  // TODO(daedalus): Return the user's preferred name if present;
  // otherwise fall back to first and last name.
  throw new Error("TODO(daedalus): implement display name formatting");
}
```

Checklist:

```markdown
- [ ] Implement display-name fallback in [`src/users/formatDisplayName.ts`](src/users/formatDisplayName.ts).
  - Failing test: [`src/users/formatDisplayName.test.ts`](src/users/formatDisplayName.test.ts) — `falls back to first and last name`
  - Run: `pnpm test src/users/formatDisplayName.test.ts`
```

### Example 2: Medium Difficulty, Medium Volume

Configuration:

```yaml
difficulty: medium
challenge_volume: medium
```

Result:

- Missing validation helper.
- Missing error branch.
- Missing test assertion.
- Missing mapper function.

Checklist:

```markdown
- [ ] Implement request validation in [`src/api/createProject.ts`](src/api/createProject.ts).
  - Failing test: [`src/api/createProject.test.ts`](src/api/createProject.test.ts) — `rejects missing project name`
  - Run: `pnpm test src/api/createProject.test.ts`

- [ ] Implement database-to-domain mapping in [`src/projects/mapProject.ts`](src/projects/mapProject.ts).
  - Failing test: [`src/projects/mapProject.test.ts`](src/projects/mapProject.test.ts) — `maps persisted project fields`
  - Run: `pnpm test src/projects/mapProject.test.ts`

- [ ] Complete the success assertion in [`src/api/createProject.test.ts`](src/api/createProject.test.ts).
  - Validation: same test file — `creates a project`
  - Run: `pnpm test src/api/createProject.test.ts`
```

### Example 3: High Difficulty, Low Volume

Configuration:

```yaml
difficulty: high
challenge_volume: low
```

Result:

```ts
export async function resolveDependencyOrder(graph: DependencyGraph): Promise<string[]> {
  // TODO(daedalus): Implement deterministic topological ordering.
  // Requirements:
  // - detect cycles
  // - preserve lexical order when multiple nodes are available
  // - include isolated nodes
  // See dependency-order.test.ts.
  throw new Error("TODO(daedalus): implement dependency ordering");
}
```

Checklist:

```markdown
- [ ] Implement deterministic dependency ordering in [`src/graph/resolveDependencyOrder.ts`](src/graph/resolveDependencyOrder.ts).
  - Failing tests: [`src/graph/dependency-order.test.ts`](src/graph/dependency-order.test.ts)
    - `orders dependencies before dependents`
    - `throws on cycles`
    - `includes isolated nodes`
    - `uses lexical tie-breaking`
  - Run: `pnpm test src/graph/dependency-order.test.ts`
```

## Agent Evaluation Fallback Template

Use this when executable tests are not feasible.

```markdown
## Validation Fallback

I could not create or run reliable automated tests for this challenge because `<reason>`.

Use this review prompt after you complete the TODOs:

> Review my implementation of the Daedalus TODOs in `<files>`.
> Validate it against these acceptance criteria:
> - `<criterion 1>`
> - `<criterion 2>`
> - `<criterion 3>`
> Do not replace my code unless necessary. First explain what is correct, what is risky, and what I should reconsider.

Completion criteria:

- The code satisfies the acceptance criteria.
- The implementation follows nearby project conventions.
- No obvious edge cases are left unhandled.
- The agent review finds no correctness blockers.
```

## Relationship to Socrates

Daedalus and [`Socrates`](../socrates/SKILL.md) should compose as follows:

- Daedalus creates the coding challenge.
- Socrates guides the developer through each missing piece.
- Daedalus defines what must be completed.
- Socrates defines how help is given.

When the developer asks:

```text
How do I do TODO 2?
```

The agent should respond in Socrates mode:

```markdown
Let’s reason through TODO 2.

First, open the associated failing test. What behavior does that test require from the function?
```

When the developer asks:

```text
Just give me the answer.
```

The agent may reveal the answer, but should treat that as exiting or suspending Daedalus for that TODO.

## Completion Criteria

A Daedalus challenge is successful when:

- The original coding task was implemented correctly before blanks were created.
- The challenge version contains deliberate, well-scoped TODOs.
- The TODOs match the requested difficulty and volume.
- The developer has a file-linked checklist.
- Each TODO has associated tests or a clear validation fallback.
- The developer can ask for Socratic hints.
- The finished challenge can be restored to a working solution by completing the TODOs.
- The user experiences the task as meaningful coding practice, not as busywork.

## Agent Reminder

Do not merely generate a skeleton.

Build the working thing first. Verify it. Then carve out a fair challenge.

Prefer tests over promises.
Prefer behavioral TODOs over vague blanks.
Prefer file-linked checklists over prose.
Prefer Socratic hints over answer dumps.
Prefer rekindling craft over maximizing automation.
