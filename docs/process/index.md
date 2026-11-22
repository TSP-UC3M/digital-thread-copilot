# Process

How the team plans, builds and reviews the project. The planning objects live on GitHub (issues, milestones, project board); the evidence that must stay with the code is kept in this repository, under `docs/process/`.

## Scrum as applied here

| Element | In this project |
| --- | --- |
| Team | Three members; roles and owners per block on the [Team](../team.md) page |
| Sprints | Four, of one week, the last one shortened by the delivery date |
| Backlog | One GitHub issue per step of the plan, with a milestone (objective OE1 to OE5, or process and delivery), a sprint label, an assignee and a priority label |
| Sprint planning | At the start of each sprint: goal of the sprint, issues committed, hours planned per member |
| Follow-up | Asynchronous, on the issues and pull requests; a short team meeting when a decision is needed |
| Sprint review and retrospective | At the end of each sprint: issues done, hours spent against planned, check of the dated fallback rules of the scope, at least one improvement action with an owner |
| Increment | `main` after each merged pull request; the documentation site is rebuilt and published on every merge |

## Sprints

| Sprint | Dates | Focus | Record |
| --- | --- | --- | --- |
| 1 | 2026-11-16 to 2026-11-22 | Problem statement and state of the art, process setup, code skeleton and continuous integration, decision records | [Sprint 1](sprint-1.md) |
| 2 | 2026-11-23 to 2026-11-29 | Case study data, ontology and shapes, ingestion, deterministic tools, reference questions | to be added at the sprint review |
| 3 | 2026-11-30 to 2026-12-06 | Copilot, guardrails, web chat, packaging, evaluation runs; feature freeze on 2026-12-06 | to be added at the sprint review |
| 4 | 2026-12-07 to 2026-12-10 | Evaluation verdict, verification report, rehearsal on a clean machine, delivery and defense | to be added at the sprint review |

Each sprint record (`docs/process/sprint-<n>.md`) gives the goal, the issues committed and done, the hours planned and spent, and the retrospective.

## From an idea to `main`

One task, one issue, one branch, one pull request.

1. An issue describes the task and names the step of the plan.
2. The owner works on a branch created from an up-to-date `main`.
3. Local checks before the push: documentation build in strict mode, translation check, lint and tests.
4. A pull request is opened; its title follows Conventional Commits and becomes the commit message on `main` (squash merge).
5. Continuous integration runs the same checks. A teammate who is not the author reviews and approves, with a note that states what was checked.
6. After the merge, the site is published and the issue is closed.

The detailed rules and commands are in `CONTRIBUTING.md` at the root of the repository.

## Definition of done

A step of the plan is done when its measurable criterion is met and shown (commit, file or link), its pull request is approved by a teammate and merged, the documentation that it changes is updated in the same pull request, and any use of generative AI is declared on the [AI usage](../ai-usage.md) page.

## Decisions and evidence

| What | Where |
| --- | --- |
| Technical and framing decisions | [Decisions](../adr/index.md) |
| Use of generative AI | [AI usage](../ai-usage.md) |
| Roles and responsibilities | [Team](../team.md) |
| Export of issues, milestones and sprints | `docs/process/`, exported by script before the delivery |
| Plan of the defense | [Defense plan](../defense/slide-plan.md) |
