---
status: accepted
date: 2026-11-15
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# Packaging: Docker Compose, virtual environment for development

## Context and Problem Statement

The statement asks that a new machine builds, tests, documents, deploys and runs the system with one command and no manual step (PROYECTO_FINAL.pdf, p. 9).

## Decision Drivers

- Same result on the evaluator's machine as on ours.
- Developers on Windows keep a light path.

## Considered Options

- Docker Compose
- Virtual environment and task runner only
- Dev container in addition

## Decision Outcome

Chosen option: "Docker Compose", because a container is the only way to guarantee the result on a machine we do not control; the virtual environment with `python scripts/dev.py` stays the developer path.

### Consequences

- Good, because a CI job can rehearse the evaluator's path from an archive of the repository (step F4).
- Bad, because the Copilot CLI runtime is downloaded at first use and must be fetched at image build time (finding of the spike).

### Confirmation

The clean-room job of step F4 is green; a member who did not write it repeats the path (step J5). Docker Desktop works on Ferdinand's machine; the check on the two other machines is pending. This record is accepted when the pull request that adds it is approved by the decision-makers.

## Pros and Cons of the Options

### Docker Compose

- Good, because: Clean machine guarantee; simple delivery.
- Bad, because: The evaluator needs Docker.

### Virtual environment and task runner only

- Good, because: Lighter.
- Bad, because: "Clean" depends on the evaluator's machine.

### Dev container in addition

- Good, because: Also automates the tool configuration.
- Bad, because: One more thing to maintain.

## More Information

- Decision identifier in the project plan: T12. Decided by Ferdinand Lacroix on 2026-11-15 from the options above, which were prepared with an AI assistant (see [AI usage](../ai-usage.md)).
- Requirements concerned: Requirement of PROYECTO_FINAL.pdf, p. 9; project requirement identifier to add in step C1. Identifiers are those of the project requirements v3 of Practica 1; they are rebaselined in step C1.
