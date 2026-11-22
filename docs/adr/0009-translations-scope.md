---
status: accepted
date: 2026-11-15
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# Translations: home and problem statement only

## Context and Problem Statement

The site exists in English, French and Spanish for the first pages. Every change of a translated page costs three edits, and about 11 pages are expected.

## Decision Drivers

- English is the reference language of the repository.
- Finished translations should not be thrown away.

## Considered Options

- Every page in 3 languages
- Home and problem statement only, frozen at tag `v0.1-planteamiento`
- Remove the translations

## Decision Outcome

Chosen option: "Home and problem statement only, frozen at tag `v0.1-planteamiento`", because it keeps the existing translations without tripling the cost of the pages to come.

### Consequences

- Good, because the freshness check of translations stays meaningful on two pages.
- Bad, because readers of the French and Spanish sites fall back to English for the other pages.

### Confirmation

`python scripts/check_translations.py --strict` exits 0; no translated file exists for the later pages. This record is accepted when the pull request that adds it is approved by the decision-makers.

## Pros and Cons of the Options

### Every page in 3 languages

- Good, because: Consistent site.
- Bad, because: Three times the cost of each change.

### Home and problem statement only, frozen at tag `v0.1-planteamiento`

- Good, because: Keeps what exists at no further cost.
- Bad, because: Later pages are in English only.

### Remove the translations

- Good, because: Simplest.
- Bad, because: Discards finished work.

## More Information

- Decision identifier in the project plan: T10. Decided by Ferdinand Lacroix on 2026-11-15 from the options above, which were prepared with an AI assistant (see [AI usage](../ai-usage.md)).
- Requirements concerned: None (documentation rule of the team). Identifiers are those of the project requirements v3 of Practica 1; they are rebaselined in step C1.
