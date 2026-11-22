# digital-thread-copilot

Generative AI engineering copilot that queries and acts on a system's digital thread (requirements, SysML v2 model and tests) represented as a knowledge graph.

**Documentation:** https://tsp-uc3m.github.io/digital-thread-copilot/

## Hypothesis

If traceability, impact and coverage questions on a digital thread are answered by an LLM copilot restricted to deterministic tools over a knowledge graph of the artifacts, then its answers cite the correct artifacts with a recall and a precision of at least 0.90 and a hallucination rate of at most 5 %, and with a significantly higher recall than the same LLM given all the artifacts as text in its context, without graph or tools (paired test on the same questions, p < 0.05).

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

- `main` is protected: every change goes through a pull request with passing checks.
- One branch per task, named `<type>/<short-description>` (for example `feat/graph-ingestion`).
- Commit messages and pull request titles follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/); pull requests are squash-merged.
- Issues are linked to a milestone (OE1 to OE5).

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development setup and the full workflow.
