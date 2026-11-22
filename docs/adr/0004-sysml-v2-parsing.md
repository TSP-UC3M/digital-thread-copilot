---
status: accepted
date: 2026-11-15
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# SysML v2 parsing: existing Python parser, pinned

## Context and Problem Statement

The logical model of the infusion pump is written by the team in the SysML v2 textual notation (step D3). Ingestion needs its parts, ports, requirement usages and satisfy relationships; generated snippets must be checked by a parser.

## Decision Drivers

- The model file is the source of truth.
- Packaging must stay light (one command, clean machine).
- A subset of the language is enough for the case study.

## Considered Options

- Official Pilot Implementation (Java)
- Existing Python parser for the subset used, version pinned
- Hand-written structured export of the model

## Decision Outcome

Chosen option: "Existing Python parser for the subset used, version pinned", because maintained Python parsers exist and the case study uses a small subset; a 30 minute trial at the start of step D3 decides which one (`sysmlpy`, then `tree-sitter-sysml`): it passes if the tool reads our model and returns parts, ports, requirements and satisfy relationships.

### Consequences

- Good, because ingestion and validation of generated snippets use the same parser, in Python.
- Bad, because only the subset we use is supported; the page of the architecture states it.

### Confirmation

The model of step D3 parses with 0 error in CI. If the trial fails for both parsers: fallback to the third option, with a test that compares the model file and its export. This record is accepted when the pull request that adds it is approved by the decision-makers.

## Pros and Cons of the Options

### Official Pilot Implementation (Java)

- Good, because: Reference tool, full language.
- Bad, because: Heavy to package and automate; half a day at risk.

### Existing Python parser for the subset used, version pinned

- Good, because: Light; same language as the rest.
- Bad, because: Subset only, to state as a limitation.

### Hand-written structured export of the model

- Good, because: Fastest.
- Bad, because: The model is no longer the single source; needs a consistency test.

## More Information

- Decision identifier in the project plan: T5. Decided by Ferdinand Lacroix on 2026-11-15 from the options above, which were prepared with an AI assistant (see [AI usage](../ai-usage.md)).
- Requirements concerned: FR-ING-02, FR-GEN-02, FR-GEN-04. Identifiers are those of the project requirements v3 of Practica 1; they are rebaselined in step C1.
- The assumption that such parsers read our subset is not verified before the trial of step D3.
