# Team

Project 10 of the course Digitization of Complex Systems Engineering (UC3M, 2026-2027): engineering copilot based on the digital thread.

## Members and roles

| Member | GitHub | Role |
| --- | --- | --- |
| Ferdinand Lacroix | `Froostiez` | Team leader; copilot (agent, tools, interface); state of the art |
| Séléné Colle Conte | `Selen-e` | Process and CI/CD; guardrails of the copilot |
| Elio Bonnenfant | `ebonnenfant` | Data, ontology and ingestion; evaluation and statistical analysis |

The leader was named on 2026-11-15. The copilot and the evaluation are shared between the three members at the level of the steps; the assignee of each issue is its owner.

## Responsibility per block of the plan

Each block has one owner, who answers for its deliverables, and one reviewer, who approves its pull requests. A pull request is never merged without the approval of a teammate (see [CONTRIBUTING](https://github.com/TSP-UC3M/digital-thread-copilot/blob/main/CONTRIBUTING.md)).

| Block | Content | Owner | Reviewer |
| --- | --- | --- | --- |
| A | Problem statement and state of the art | Ferdinand Lacroix | Séléné Colle Conte |
| B | Scrum process on GitHub | Séléné Colle Conte | Ferdinand Lacroix |
| C | Requirements, decisions, architecture | Ferdinand Lacroix | Elio Bonnenfant |
| D | Case study data | Elio Bonnenfant | Séléné Colle Conte |
| E | Ontology and shapes | Elio Bonnenfant | Ferdinand Lacroix |
| F | Skeleton, CI/CD, quality | Séléné Colle Conte | Elio Bonnenfant |
| G | Ingestion | Elio Bonnenfant | Ferdinand Lacroix |
| H | Tools and copilot | Ferdinand Lacroix | Séléné Colle Conte and Elio Bonnenfant, in turn |
| I | Evaluation of the hypothesis | Elio Bonnenfant | Ferdinand Lacroix |
| J | Documentation and final verification and validation | Séléné Colle Conte | Elio Bonnenfant |
| K | Delivery and defense | Séléné Colle Conte | Ferdinand Lacroix |

Exceptions inside a block: the requirements of the project (step C1) are owned by Elio Bonnenfant; the guardrails (H3) by Séléné Colle Conte and the generation of draft test cases (H4) by Elio Bonnenfant, both reviewed by Ferdinand Lacroix; the metrics harness (I2) by Séléné Colle Conte. The file `.github/CODEOWNERS` follows this table. When the reviewer of a block is away, another member approves (sprint 1: Ferdinand Lacroix for block F).

## Planning objects

Labels, milestones and the backlog are defined as files (`.github/labels.json`, `.github/backlog.json`) and applied by `scripts/github_setup.py` and by the `labels` workflow. One issue exists per step of the plan, with its sprint, its priority, its milestone and its owner.

| Sprint | Dates | Goal |
| --- | --- | --- |
| 1 | 2026-11-16 to 2026-11-22 | Problem statement closed, process in place, decisions taken, skeleton with CI |
| 2 | 2026-11-23 to 2026-11-29 | Digital thread of the case study in the graph, deterministic tools |
| 3 | 2026-11-30 to 2026-12-06 | Copilot, evaluation runs, packaging; feature freeze on 2026-12-06 |
| 4 | 2026-12-07 to 2026-12-10 | Final verification and validation, documentation, delivery, defense |
