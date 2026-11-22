---
status: accepted
date: 2026-11-15
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# Team leader and roles

## Context and Problem Statement

The statement grades the role of each member and a 360 evaluation, and asks for a team leader (PROYECTO_FINAL.pdf, p. 1).

## Decision Drivers

- One owner per step, for the issues and the contribution evidence.
- No single point of failure on the copilot.

## Considered Options

- One leader and three roles: process and CI/CD, data and ontology, copilot and evaluation shared
- No fixed roles, assignment issue by issue

## Decision Outcome

Chosen option: "One leader and three roles: process and CI/CD, data and ontology, copilot and evaluation shared", because it gives each step one owner and one reviewer: leader Ferdinand Lacroix; process and CI/CD Séléné Colle Conte; data and ontology Elio Bonnenfant; copilot and evaluation shared, with the guardrails to Séléné Colle Conte and the statistical analysis to Elio Bonnenfant.

### Consequences

- Good, because `docs/team.md`, `CODEOWNERS` and the assignees of the issues follow one table.
- Bad, because the split per sprint is uneven and is rebalanced by the team (open decision on the load per member).

### Confirmation

Each pull request of block H is reviewed by a member who is not its author; the contribution page of step K5 is generated from issues and pull requests. This record is accepted when the pull request that adds it is approved by the decision-makers.

## Pros and Cons of the Options

### One leader and three roles: process and CI/CD, data and ontology, copilot and evaluation shared

- Good, because: Clear ownership; profiles of the members respected.
- Bad, because: The leader carries coordination on top of his steps.

### No fixed roles, assignment issue by issue

- Good, because: Flexible.
- Bad, because: Weak evidence for the individual criterion.

## More Information

- Decision identifier in the project plan: T13. Decided by Ferdinand Lacroix on 2026-11-15 from the options above, which were prepared with an AI assistant (see [AI usage](../ai-usage.md)).
- Requirements concerned: None (process decision). Identifiers are those of the project requirements v3 of Practica 1; they are rebaselined in step C1.
- Leader named on 2026-11-15; split per member proposed the same day and confirmed in [Team](../team.md) on 2026-11-22: approval of the pull request by Séléné Colle Conte, agreement of Elio Bonnenfant reported by Ferdinand Lacroix (confirmation on GitHub to follow).
