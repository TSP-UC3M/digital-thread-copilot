---
status: accepted
date: 2026-11-15
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# Graph store: rdflib in memory

## Context and Problem Statement

The digital thread (requirements, model elements, test cases, results and their links) is stored as an RDF graph queried with SPARQL and checked with SHACL (problem statement, standards table). The case study has about 12 requirements, 12 test cases and one small model.

## Decision Drivers

- Standards named in the statement: RDF, OWL, SPARQL, SHACL (PROYECTO_FINAL.pdf, p. 8).
- No service to deploy for the evaluator (one command on a clean machine, p. 9).
- Same language as the rest of the system (Python).

## Considered Options

- rdflib, in memory, loaded from files
- Oxigraph, embedded
- Apache Jena Fuseki server
- Neo4j property graph

## Decision Outcome

Chosen option: "rdflib, in memory, loaded from files", because it needs no service and covers SPARQL and, with pySHACL, SHACL; the size of the case study makes its speed irrelevant.

### Consequences

- Good, because the graph is rebuilt from the versioned files at each start, so the repository stays the source of truth.
- Bad, because scaling claims cannot be measured on this store; this goes into the threats to validity of the evaluation.

### Confirmation

The ingestion tests of block G load the graph with rdflib and assert node and edge counts; the shapes of step E2 are checked in CI. This record is accepted when the pull request that adds it is approved by the decision-makers.

## Pros and Cons of the Options

### rdflib, in memory, loaded from files

- Good, because: No service; native SPARQL; SHACL through pySHACL.
- Bad, because: Slow on large graphs, which the case study is not.

### Oxigraph, embedded

- Good, because: Faster.
- Bad, because: One more dependency for no visible gain at this size.

### Apache Jena Fuseki server

- Good, because: Standard SPARQL endpoint.
- Bad, because: One more container to build, start and check.

### Neo4j property graph

- Good, because: Good visual tools.
- Bad, because: Not RDF: contradicts the standards of the problem statement.

## More Information

- Decision identifier in the project plan: T4. Decided by Ferdinand Lacroix on 2026-11-15 from the options above, which were prepared with an AI assistant (see [AI usage](../ai-usage.md)).
- Requirements concerned: FR-ING-01 to FR-ING-03. Identifiers are those of the project requirements v3 of Practica 1; they are rebaselined in step C1.
