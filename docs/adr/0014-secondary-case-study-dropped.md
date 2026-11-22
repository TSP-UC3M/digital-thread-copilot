---
status: accepted
date: 2026-11-15
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# Secondary case study dropped

## Context and Problem Statement

The problem statement kept the Simple Vehicle Model of the SysML v2 specification as an optional second case study, to check portability.

## Decision Drivers

- The reduced scope has no spare hours.
- The primary case study must not depend on the secondary one.

## Considered Options

- Keep it as optional
- Drop it now

## Decision Outcome

Chosen option: "Drop it now", because the 4 h are not available in the reduced scope, and the pump model is written by the team in any case: the published GPCA artifacts are AADL, Simulink/Stateflow and UPPAAL models, and we found no SysML v2 model among them.

### Consequences

- Good, because the effort goes to one complete digital thread.
- Bad, because portability to a second system is not shown; this is stated as a threat to validity.

### Confirmation

The problem statement no longer mentions the secondary case study once it is finalized (step A6). This record is accepted when the pull request that adds it is approved by the decision-makers.

## Pros and Cons of the Options

### Keep it as optional

- Good, because: Shows portability if time remains.
- Bad, because: 4 h unlikely to be available.

### Drop it now

- Good, because: Removes a distraction; one sentence to change in the problem statement.
- Bad, because: No portability check.

## More Information

- Decision identifier in the project plan: T15. Decided by Ferdinand Lacroix on 2026-11-15 from the options above, which were prepared with an AI assistant (see [AI usage](../ai-usage.md)).
- Requirements concerned: None (scope decision, objective OE5). Identifiers are those of the project requirements v3 of Practica 1; they are rebaselined in step C1.
- The absence of a SysML v2 model in the GPCA artifacts is recorded with the pages visited in the provenance file (step D1).
