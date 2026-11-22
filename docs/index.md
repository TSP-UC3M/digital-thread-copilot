# digital-thread-copilot

Generative AI engineering copilot that queries and acts on a system's digital thread (requirements, SysML v2 model and tests) represented as a knowledge graph.

## Hypothesis

If traceability, impact and coverage questions on a digital thread are answered by an LLM copilot restricted to deterministic tools over a knowledge graph of the artifacts, then its answers cite the correct artifacts with a recall and a precision of at least 0.90 and a hallucination rate of at most 5 %, and with a significantly higher recall than the same LLM given all the artifacts as text in its context, without graph or tools (paired test on the same questions, p < 0.05).

## General objective

Develop a generative AI engineering copilot that queries and acts on a digital thread represented as a knowledge graph, so that traceability and impact questions are answered quickly, exhaustively and grounded in the project's artifacts.

See the full [problem statement](00-planteamiento.md).

## Team

Ferdinand Lacroix, Elio Bonnenfant, Séléné Colle Conte. Course: Digitalización de Ingeniería de Sistemas Complejos, UC3M (2026-2027).
