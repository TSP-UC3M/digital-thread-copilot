# digital-thread-copilot

Generative AI engineering copilot that queries and acts on a system's digital thread (requirements, SysML v2 model and tests) represented as a knowledge graph.

**Documentation:** https://tsp-uc3m.github.io/digital-thread-copilot/

## Hypothesis

If an engineer queries the digital thread through an LLM copilot grounded in a knowledge graph and deterministic tools, then they answer traceability and impact questions at least 50 % faster and with an artifact recall of at least 90 % (compared to manual search across the artifacts and to an LLM without access to the graph).

## General objective

Develop a generative AI engineering copilot that queries and acts on a digital thread represented as a knowledge graph, so that traceability and impact questions are answered quickly, exhaustively and grounded in the project's artifacts.

## Specific objectives

| ID | Objective |
| --- | --- |
| OE1 | Analyze the state of the art on digital threads, knowledge graphs and LLMs applied to MBSE |
| OE2 | Design the system architecture and the digital thread ontology |
| OE3 | Implement the ingestion of artifacts into the knowledge graph |
| OE4 | Implement the copilot with deterministic tools and guardrails |
| OE5 | Evaluate the hypothesis with a set of reference questions |

Full problem statement: [docs/00-planteamiento.md](docs/00-planteamiento.md)

## Team

- Ferdinand Lacroix
- Elio Bonnenfant
- Séléné Colle Conte

Course: Digitalización de Ingeniería de Sistemas Complejos, UC3M (2026-2027)

## Workflow

- `main` holds the validated version only.
- One branch per task: `feature/<name>`, merged through a Pull Request.
- Issues are linked to a milestone (OE1 to OE5).
