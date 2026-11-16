---
status: proposed
date: 2026-11-16
decision-makers: Ferdinand Lacroix, Elio Bonnenfant, Séléné Colle Conte
---

# Project framing: scope, hypothesis criteria, roles and fallbacks

## Context and Problem Statement

The problem statement of 2026-10-22 ([Problem statement](../00-planteamiento.md)) promises a case study of about 20 requirements, 30 reference questions and a secondary case study. An estimate of the work made on 2026-11-15 gave 148.5 h of mandatory work for a capacity of 105 h (3 members, 10 h per week, 3.5 weeks until week 14). The course statement requires a verified and validated system to pass and weights the final verification at 10 %, the panel vote at 30 %, the process, quality and impact at 50 % and the role of each member at 10 % (PROYECTO_FINAL.pdf, p. 1). Activity 0 states that no group starts developing without validated objectives (Actividad0_Enunciado_Planteamiento.pdf, p. 2).

The effort figures are estimates by the team, not measurements. They are compared with the hours spent at each sprint review.

## Decision Drivers

- Deliver a working, verified system by week 14 rather than a wider unfinished one.
- Keep a hypothesis that can be accepted or rejected with the data we can actually collect.
- Keep every grading criterion covered.

## Considered Options

| Option | Mandatory work | Hours per member per week | Effect on the hypothesis |
| --- | --- | --- | --- |
| S1: full scope | 148.5 h | 14.1 | Unchanged |
| S2: reduced depth | 125.5 h | 12.0 | Wording changes; acceptance figures reduced |
| S3: fit to 105 h | 105 h | 10.0 | Manual comparison removed |

## Decision Outcome

Chosen option: "S2: reduced depth", because it keeps the hypothesis testable and the manual comparison with a workload the team can commit to, at 12 h per member per week (126 h of capacity). With the leader's coordination time and the small steps added during framing, the planned mandatory work is 130.75 h: the plan is 4.75 h above capacity, which the team accepts and controls with the dated fallbacks listed under More Information.

The decision fixes four things, detailed under More Information: the scope, the criteria that decide the hypothesis, the roles, and the fallbacks.

### Consequences

- Good, because the mandatory work is close to the capacity and every grading criterion keeps at least one step.
- Bad, because fewer questions and requirements give wider confidence intervals and a weaker demonstration, and the plan has no buffer.
- The problem statement, the README and the home page still show the figures and the hypothesis of 2026-10-22. They are updated once the professor has answered.

### Confirmation

This record is accepted when Elio Bonnenfant and Séléné Colle Conte have approved the pull request that adds it, which is the written confirmation of the team, and when the professor has validated the objectives (requested by mail on 2026-11-15). No ingestion or copilot development starts before that validation. Compliance is then checked at each sprint review against the fallback table.

## Pros and Cons of the Options

### S1: full scope

- Good, because the problem statement of 2026-10-22 stays unchanged.
- Bad, because it needs 14.1 h per member per week, and the overrun would fall on the evaluation, the packaging and the defense.

### S2: reduced depth

- Good, because every grading criterion stays covered and the manual comparison is kept.
- Bad, because the acceptance figures of the problem statement are reduced and must be validated again by the professor.

### S3: fit to 105 h

- Good, because it fits 10 h per member per week.
- Bad, because the manual comparison is removed and test execution becomes a lookup of recorded results.

## More Information

### Scope

| Item | Problem statement of 2026-10-22 | This decision |
| --- | --- | --- |
| Case study requirements (GPCA infusion pump) | About 20 | 12 |
| Test cases | One set for the 20 requirements | 12 |
| SysML v2 model | Written by the team from the published architecture | Unchanged, limited to the 12 requirements |
| Reference questions | 30 | 20 |
| State of the art | At least 6 works, 2 databases | 8 works, searches in IEEE Xplore and Scopus; works found by other means are counted separately |
| Manual comparison | At least 3 participants, 30 questions | 3 participants outside the group, 10 questions each |
| Secondary case study (Simple Vehicle Model) | Optional | Dropped |
| Generated SysML v2 snippets and traceability reports, subgraph view, re-ingestion on every change | In objective OE4 and in the proposal | Extensions, done only if time allows |

### Hypothesis criteria

- **Primary criterion (automated).** On the reference questions, the copilot reaches a recall and a precision of cited artifacts of at least 0.90 and a hallucination rate of at most 5 %, and differs significantly (paired test on the same questions, p < 0.05, effect size reported) from the reference configuration (ii) below.
- **Reference configurations**, both measured with the same model, version and parameters as the copilot, and no tools: (i) the model receives the question only, reported as a lower bound; (ii) the model receives the question and the text of all artifacts in its context.
- **Secondary criterion (indicative).** Time to answer reduced by at least 50 % against manual search. With 3 participants this is an observation, not a statistical result.
- The thresholds 0.90, 5 % and 50 % are choices of the team; no reference is claimed for them.
- The test, the metric under test, the unit of the hallucination rate, the averaging and the aggregation of repeated runs are fixed in the evaluation protocol, committed before any measurement. All measurements come from live runs.

Known threat to validity: the case study is small (12 requirements, 12 tests). All artifacts fit in the context of reference (ii), so the difference with the copilot may be small. Whether the approach matters more on larger digital threads is a matter for the discussion of the results, not part of the criterion.

### Roles

| Member | Role |
| --- | --- |
| Ferdinand Lacroix | Team leader; copilot core |
| Séléné Colle Conte | Process and CI/CD; copilot guardrails |
| Elio Bonnenfant | Data and ontology; statistical analysis of the evaluation |

Every pull request on the copilot is reviewed by a member who is not its author. The owner of each step is recorded in its issue.

### Fallbacks

Each fallback is checked at the sprint review closest to its date. If its condition is true, the reduction applies and is recorded.

| Date | Condition | Reduction |
| --- | --- | --- |
| 2026-11-19 | Planning tool or backlog not in place | Shorter sprint notes |
| 2026-11-22 | State of the art or problem statement not merged | Reading notes at the minimum length |
| 2026-11-25 | Requirements or architecture not merged | 2 architecture views instead of 3 |
| 2026-11-27 | Test cases not runnable by one command | Recorded test results instead of execution |
| 2026-11-27 | Ontology not merged | 5 competency questions instead of 10 |
| 2026-11-27 | Fewer than 3 external participants confirmed | Manual comparison dropped; secondary criterion reported as not measured |
| 2026-11-29 | Ingestion not merged | SysML v2 ingestion limited to parts and satisfy relationships |
| 2026-12-01 | Tools not merged or no end-to-end answer | Lighter guardrail tests, replay and chat |
| 2026-12-03 | Clean-machine build not green | Release merged into the build step |
| 2026-12-06 | Validation scenario not passing, or feature freeze not reached | Lighter documentation and one rehearsal |

On 2026-12-01 the team decides whether spare hours allow extensions, in this order: a second rehearsal, 30 reference questions (the added questions written by a member who has not seen copilot answers and frozen before any run), fuller quality and traceability pages.

### Use of generative AI

Use of generative AI in this framing is declared in the section "AI usage statement" of the [problem statement](../00-planteamiento.md). The format of this record is defined in [ADR-0000](0000-use-madr.md).
