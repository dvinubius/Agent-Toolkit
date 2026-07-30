---
name: feynman
description: Writes a document that teaches one technical theme mechanism-first, with worked examples, edge cases, and an exercise. Use when the user asks to explain, teach, or document a concept as a course lesson, YouTube reference, or newsletter basis.
argument-hint: "<topic>"
---

# Feynman

Write a document that teaches one technical theme through mechanisms, examples, edges, and an exercise.

## Scope

Cover one coherent theme. If the topic is too broad, offer 2–4 narrower themes and ask the user to pick one:

```md
"AI agents" is too broad. Pick one:

1. Agent memory: types, mechanics, when to use each
2. Tool calling: loop mechanics and tool design
3. Error handling: failures, recovery, avoiding hangs
```

## Structure

```md
# [Title: claim or question]

[Opening: 2–4 sentences. An observation the reader recognises — not a definition.]

[Promise: what the reader will understand, stated before any detail.]

## [Section title: specific claim]

[Point in one sentence.]
[One concrete example, walked through completely — before the general rule.]
[Code, command, prompt, or diagram only when it clarifies the idea.]

## [Next section]

## Putting it together

[Short scenario that uses the sections together.]

## Try it

[One exercise. Under ten minutes.]

[Closing sentence that earns the opening promise.]
```

## Rules

- Order every explanation mechanism-first: the mechanism in plain words, then the term, then any formalism.
- When using an analogy, name where it breaks.
- Name unsolved, messy, or disputed edges.
- Close the obvious wrong conclusion a reader would draw.
- Short sentences, common words; cut any sentence that sounds profound but adds no information.
- Reference material — tables, cheat sheets, syntax summaries — goes in a separate document.

## Mechanism-first example

Weak: "This uses RAG to retrieve relevant context."

Strong: "RAG works in three steps. First, search stored documents for content relevant to the user's question. Second, paste that content into the prompt. Third, generate an answer using that information. The name is just the sequence: retrieve, augment, generate."

The difference: the strong version walks the mechanism, and the term arrives last — a label for something already understood.

## Done when

The draft fills every bracketed slot in Structure and passes every rule above — each verified against the text, not assumed.
