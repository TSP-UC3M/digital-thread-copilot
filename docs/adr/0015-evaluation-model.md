---
status: proposed
date: 2026-11-16
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# Model used for the evaluation runs

## Context and Problem Statement

The evaluation needs 180 live runs (20 questions, 3 configurations, 3 repetitions) with one model, version and parameter set. The spike measured about 3800 input and 80 output tokens per copilot run; the token cost of 180 runs is far below 2 EUR for small paid models, but paid keys ask for a minimum credit of about 5 USD (stated by Ferdinand, not checked).

## Decision Drivers

- Same model for the three configurations.
- A reader should be able to repeat the measurement.
- Tool calling must be reliable enough to measure the approach and not the model's weakness.

## Considered Options

- Paid key for all runs
- Local model for the main evaluation (`qwen3:8b`, reasoning off, pinned digest), paid key only for a replication
- Copilot Free
- Paid key for the main evaluation and the participant sessions, local model for development, CI and a keyless replication

## Decision Outcome

No option is chosen yet: the team decides before the evaluation protocol is frozen; the advisor's recommendation and Ferdinand's proposal are the fourth option.

### Consequences

To complete when the decision is taken.

### Confirmation

The evaluation protocol names the model, its version or digest, the reasoning setting and the provider before any measurement. The status becomes "accepted" in the pull request that records the team's choice.

## Pros and Cons of the Options

### Paid key for all runs

- Good, because: Stronger model; fast runs.
- Bad, because: Minimum credit to buy; a reader needs a key to repeat.

### Local model for the main evaluation (`qwen3:8b`, reasoning off, pinned digest), paid key only for a replication

- Good, because: No key; repeatable by anyone.
- Bad, because: Slow on CPU; weaker tool calling (1 tool call skipped in 3 with reasoning on).

### Copilot Free

- Good, because: No cost.
- Bad, because: The model is not chosen by us: rejected.

### Paid key for the main evaluation and the participant sessions, local model for development, CI and a keyless replication

- Good, because: Best answers where they are measured; replication without key.
- Bad, because: Minimum credit shared by the three members.

## More Information

- Decision identifier in the project plan: B-EV. Submitted to the team on 2026-11-16.
- Requirements concerned: FR-EVAL-01. Identifiers are those of the project requirements v3 of Practica 1; they are rebaselined in step C1.
- Analysis: working notes of 2026-11-16 on the budget of the evaluation. Reasoning is off in the evaluation unless decided otherwise (decision of 2026-11-16 after the spike).
