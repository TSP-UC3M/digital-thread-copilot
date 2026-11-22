---
status: accepted
date: 2026-11-15
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# LLM access: live model by configuration, replay mode for CI and demonstration

## Context and Problem Statement

The evaluator must build and run the system with no manual step, and the teaching staff sets the AI configuration for the final competition (PROYECTO_FINAL.pdf, p. 9). Tests in CI must not depend on a paid key or on a non-deterministic answer.

## Decision Drivers

- No credential needed to start the system and to run CI.
- Provider, endpoint, model and key change by environment settings only.
- Measurements must come from real model answers.

## Considered Options

- Live model only
- Live model plus a replay mode with recorded responses
- Local open model only

## Decision Outcome

Chosen option: "Live model plus a replay mode with recorded responses", because it is the only option that satisfies both the evaluator's path and deterministic tests; replay is used for CI and the demonstration only, and every evaluation measurement comes from live runs.

### Consequences

- Good, because changing the model needs only environment settings (shown with 2 models in step H7).
- Bad, because recordings go stale when prompts or tools change and must be regenerated.

### Confirmation

With no credential set, the start command runs the demonstration scenario in replay mode (step H7). The evaluation protocol states that replayed answers are never measured. This record is accepted when the pull request that adds it is approved by the decision-makers.

## Pros and Cons of the Options

### Live model only

- Good, because: Nothing to build.
- Bad, because: Contradicts "no manual intervention"; flaky CI.

### Live model plus a replay mode with recorded responses

- Good, because: CI and demonstration run without credentials and stay deterministic.
- Bad, because: About 3 h (step H7); recordings to refresh.

### Local open model only

- Good, because: No credential at all.
- Bad, because: Heavy download; weaker tool calling.

## More Information

- Decision identifier in the project plan: T11. Decided by Ferdinand Lacroix on 2026-11-15 from the options above, which were prepared with an AI assistant (see [AI usage](../ai-usage.md)).
- Requirements concerned: NFR-OPS-02, FR-EVAL-01. Identifiers are those of the project requirements v3 of Practica 1; they are rebaselined in step C1.
- Confirmed after the spike on 2026-11-16: provider, endpoint, model and key are read from the environment.
