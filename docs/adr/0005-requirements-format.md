---
status: accepted
date: 2026-11-21
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# Requirements format: YAML validated by JSON Schema, with ReqIF 1.2 export

## Context and Problem Statement

Requirements of the case study and of the project must be machine readable, reviewed in pull requests and defined in terms of standards (PROYECTO_FINAL.pdf, p. 8, names ReqIF). The problem statement left the format open ("ReqIF/JSON"); the first version of this record, on 2026-11-15, still said "YAML or JSON". On 2026-11-19 the professor asked for a named format for every artifact.

## Decision Drivers

- Readable diffs in pull requests, and room for a comment that gives the reason of a requirement or of its change.
- Interoperability through a standard exchange format.
- Schema validation in CI.
- The drafts of the project requirements (C1), of the case study requirements (D2) and test cases (D4), and the verification matrix script already read YAML.

## Considered Options

- ReqIF as source
- YAML as source, validated by JSON Schema, with an export to ReqIF 1.2
- JSON as source, validated by JSON Schema, with an export to ReqIF 1.2
- JSON only

## Decision Outcome

Chosen option: "YAML as source, validated by JSON Schema, with an export to ReqIF 1.2", because the source stays reviewable line by line with comments, the drafts need no conversion, and the export keeps the link with the standard. The same rule applies to the test cases of the case study (D4).

Files: `requirements/requirements.yaml` (project requirements, step C1) and `data/gpca/requirements.yaml` (case study, step D2), each with a JSON Schema (draft-07) next to it; ReqIF 1.2 export written by an output adapter (ADR-0017, added with the architecture page).

### Consequences

- Good, because each requirement is one reviewable record validated against a schema.
- Good, because YAML is read with `yaml.safe_load` only (no object construction from the file).
- Bad, because PyYAML follows YAML 1.1, which turns some unquoted words and numbers into booleans or floats (`NO`, `1.10`): every text value is quoted, and the schema rejects a boolean or a number where a string is expected.
- Bad, because the export must be tested; if it takes more than 1 h, the fallback is the YAML source only, with the limitation stated.

### Confirmation

The requirement files validate against their schema in CI (steps C1 and D2); a test checks the exported ReqIF against the ReqIF 1.2 XSD. This record is accepted when the pull request that adds it is approved by the decision-makers.

## Pros and Cons of the Options

### ReqIF as source

- Good, because: Pure standard.
- Bad, because: Verbose XML, hard to review.

### YAML as source, validated by JSON Schema, with an export to ReqIF 1.2

- Good, because: Easy to edit and review, comments allowed; still interoperable; drafts already written in it.
- Bad, because: One converter to write and test; YAML 1.1 implicit typing to guard against.

### JSON as source, validated by JSON Schema, with an export to ReqIF 1.2

- Good, because: No implicit typing; the word used by the professor in class.
- Bad, because: No comments; every draft (C1, D2, D4) and the verification matrix script to convert.

### JSON only

- Good, because: Simplest.
- Bad, because: Weakens "defined in terms of standards".

## More Information

- Decision identifier in the project plan: T6. Decided by Ferdinand Lacroix on 2026-11-15 ("YAML or JSON"), then on 2026-11-21 (YAML), from the options above, which were prepared with an AI assistant (see [AI usage](../ai-usage.md)).
- Requirements concerned: FR-ING-01, FR-ING-03.
- ReqIF 1.2: Object Management Group, Requirements Interchange Format, formal/16-07-01.
