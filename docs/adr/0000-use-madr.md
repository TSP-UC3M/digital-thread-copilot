---
status: proposed
date: 2026-11-16
decision-makers: Ferdinand Lacroix, Elio Bonnenfant, Séléné Colle Conte
---

# Use Markdown Architectural Decision Records

## Context and Problem Statement

The project statement asks for documentation that is versioned inside the repository, traceable, and cross-referenced between requirements, decision records, components and tests (PROYECTO_FINAL.pdf, p. 9 to 10). The team takes scope, method and architecture decisions that must stay readable by the evaluators and by each member. Which format do we use to record them?

## Decision Drivers

- Records live in the repository, next to the code, and are reviewed in pull requests.
- A record shows the options that were considered, not only the one retained.
- Records can be linked from requirements, components and tests, and listed automatically.
- The format costs little to learn and to write.

## Considered Options

- MADR 4.0.0 (Markdown Architectural Decision Records)
- Short decision records in the style of M. Nygard (context, decision, status, consequences)
- A single decision log table in the documentation

## Decision Outcome

Chosen option: "MADR 4.0.0", because it is plain Markdown that our documentation site already builds, and because its sections for decision drivers and considered options make each record state the alternatives and the reasons, which the other two options leave to the author.

### Consequences

- Good, because decisions, options and reasons are reviewed like code and are part of the delivered repository.
- Bad, because writing the options takes more time than a one-line log entry; short decisions may use only the mandatory sections.

### Confirmation

This record is accepted when the pull request that adds it is approved by the decision-makers. Afterwards, reviewers check in each pull request that a change of scope, method or architecture comes with a record that follows the template.

## Pros and Cons of the Options

### MADR 4.0.0

- Good, because the template has dedicated sections for decision drivers, considered options and their pros and cons.
- Good, because it is plain Markdown with metadata in the front matter, which the site generator reads without a plugin.
- Bad, because a full record is longer to write.

### Short records in the style of M. Nygard

- Good, because a record is short.
- Bad, because the options that were rejected are not part of the structure.

### Single decision log table

- Good, because all decisions are visible on one page.
- Bad, because one row cannot hold the context and the comparison of options, and concurrent edits of one table conflict in pull requests.

## More Information

Template: MADR 4.0.0, released on 2024-09-17. Source: https://adr.github.io/madr/, consulted on 2026-11-16.

How we apply it:

- Mandatory sections: Context and Problem Statement, Considered Options, Decision Outcome. The other sections of the template are optional and keep the order of the template.
- Metadata used: `status`, `date`, `decision-makers`; `consulted` and `informed` when they apply. The fields `parent`, `nav_order` and `title` of the template configure another site theme and are not used.
- Status is one of proposed, accepted, rejected, deprecated, superseded by ADR-NNNN.
- Files are named `NNNN-title-with-dashes.md`, numbered consecutively from 0000.
- Deviation from the template: records are stored in `docs/adr/`, not in `docs/decisions/`, to match the name used in the course statement and in our plan.
- A record cites the requirement identifiers it affects once the requirements are in the repository.

The first decision recorded with this format is [project framing](0001-project-framing.md).
