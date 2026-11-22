---
status: accepted
date: 2026-11-15
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# Test execution: small executable reference model

## Context and Problem Statement

The copilot must act through tools, including test execution (PROYECTO_FINAL.pdf, p. 7). The published GPCA artifacts give models and verification material, not a runnable system.

## Decision Drivers

- A real execution supports the demonstration and the panel vote.
- Code that is not the copilot must stay small.

## Considered Options

- Small executable reference model of the pump behaviour
- Test cases with recorded results only

## Decision Outcome

Chosen option: "Small executable reference model of the pump behaviour", because a computed pass or fail makes the test execution tool an action and not a lookup; the model is limited to the behaviours of the 12 selected requirements.

### Consequences

- Good, because one command runs all test cases and prints pass or fail for each (step D4).
- Bad, because the reference model is ours, not the published one; this is a threat to validity of the case study.

### Confirmation

Step D4: one command runs the 12 test cases. Fallback by the trigger of block D on 2026-11-27: recorded results only. This record is accepted when the pull request that adds it is approved by the decision-makers.

## Pros and Cons of the Options

### Small executable reference model of the pump behaviour

- Good, because: Tests really run; pass or fail is computed.
- Bad, because: More code outside the copilot.

### Test cases with recorded results only

- Good, because: About 1.5 h less.
- Bad, because: "Test execution" becomes a lookup.

## More Information

- Decision identifier in the project plan: T7. Decided by Ferdinand Lacroix on 2026-11-15 from the options above, which were prepared with an AI assistant (see [AI usage](../ai-usage.md)).
- Requirements concerned: FR-ING-03, test execution tool among FR-TOOL-01 to FR-TOOL-04. Identifiers are those of the project requirements v3 of Practica 1; they are rebaselined in step C1.
