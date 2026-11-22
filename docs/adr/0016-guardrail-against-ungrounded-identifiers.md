---
status: proposed
date: 2026-11-16
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# Guardrail against answers that cite identifiers without tool evidence

## Context and Problem Statement

In the spike, an available tool was not always called (1 case in 3 with reasoning on), and the answer then invented artifact identifiers. Objective OE4 requires that every answer cites existing identifiers.

## Decision Drivers

- An invented identifier must never reach the user.
- The rule must not depend on one model provider.
- The hallucination metric must still measure the approach: it is computed before and after the guardrail.

## Considered Options

- (a) Reject an answer that contains identifiers when no tool was called in the turn
- (b) Reject an answer unless every identifier it cites appears in the tool results of the same turn
- (c) Force a tool call through the model API
- (d) On rejection, retry once with an explicit instruction, then return the fixed reply "no supporting artifact"

## Decision Outcome

No option is chosen yet: the team decides before step H3; the assistant's recommendation is (b) combined with (d); owner of the step: Séléné Colle Conte.

### Consequences

To complete when the decision is taken.

### Confirmation

The 5 tests of step H3 pass, including: an answer citing a non-existent identifier is blocked, and a question without supporting artifact gets the fixed reply. The status becomes "accepted" in the pull request that records the team's choice.

## Pros and Cons of the Options

### (a) Reject an answer that contains identifiers when no tool was called in the turn

- Good, because: Simple.
- Bad, because: Lets through an invented identifier next to a real tool call.

### (b) Reject an answer unless every identifier it cites appears in the tool results of the same turn

- Good, because: Covers (a) and partial inventions.
- Bad, because: Needs a reliable extraction of identifiers from the answer.

### (c) Force a tool call through the model API

- Good, because: No post-check.
- Bad, because: Not portable: the local endpoint used in the spike does not support `tool_choice`.

### (d) On rejection, retry once with an explicit instruction, then return the fixed reply "no supporting artifact"

- Good, because: Recovers some answers.
- Bad, because: One more model call in the worst case.

## More Information

- Decision identifier in the project plan: H3-G. Submitted to the team on 2026-11-16.
- Requirements concerned: FR-GRD-01 to FR-GRD-04, NFR-SEC-02. Identifiers are those of the project requirements v3 of Practica 1; they are rebaselined in step C1.
