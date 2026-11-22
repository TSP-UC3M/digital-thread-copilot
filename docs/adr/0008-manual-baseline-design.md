---
status: accepted
date: 2026-11-15
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# Manual baseline: 3 external participants, 10 questions each

## Context and Problem Statement

The hypothesis compares the copilot with a manual search across the artifacts. This comparison needs participants outside the group and sessions before 2026-12-06.

## Decision Drivers

- Sessions short enough to recruit volunteers.
- The verdict on the hypothesis must not depend on recruitment.

## Considered Options

- 3 participants, 30 questions, crossed order
- 3 participants, 10 questions each, crossed order
- No manual baseline

## Decision Outcome

Chosen option: "3 participants, 10 questions each, crossed order", because it keeps a human reference at a cost that fits the calendar; with 3 participants the result is indicative only, so it is the secondary criterion of the hypothesis and the primary criterion is automated (ADR-0001).

### Consequences

- Good, because the hypothesis can be decided even if recruitment fails.
- Bad, because the time comparison has no statistical weight and is reported as indicative.

### Confirmation

Protocol written before the first session (step I3). Fallback by the trigger of block I on 2026-11-27: no manual baseline, secondary criterion reported as not measured. This record is accepted when the pull request that adds it is approved by the decision-makers.

## Pros and Cons of the Options

### 3 participants, 30 questions, crossed order

- Good, because: As first written.
- Bad, because: About 2 h per participant.

### 3 participants, 10 questions each, crossed order

- Good, because: Sessions of about 45 minutes.
- Bad, because: Less data.

### No manual baseline

- Good, because: Fully automated evaluation.
- Bad, because: Loses the comparison with the manual process.

## More Information

- Decision identifier in the project plan: T9. Decided by Ferdinand Lacroix on 2026-11-15 from the options above, which were prepared with an AI assistant (see [AI usage](../ai-usage.md)).
- Requirements concerned: FR-EVAL-01. Identifiers are those of the project requirements v3 of Practica 1; they are rebaselined in step C1.
- Figure submitted to the professor in the validation request of 2026-11-15.
