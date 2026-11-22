---
status: accepted
date: 2026-11-21
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# Architecture: hexagonal style with named design patterns

## Context and Problem Statement

When he validated the objectives on 2026-11-19, the professor asked for a more concrete architecture: what it is based on and which design patterns it follows, by name. The statement also asks for an explicit architecture, defined in terms of standards (PROYECTO_FINAL.pdf, p. 8). The system mixes a deterministic part (artifacts, graph, tools) and a generative part (agent, model provider), and several of its choices may change late: input formats, model provider, user interface.

## Decision Drivers

- The deterministic core must not depend on a file format, on a model provider or on the interface, so that [ADR-0005](0005-requirements-format.md), [ADR-0007](0007-user-interface-chat-framework.md) and [ADR-0010](0010-llm-access-and-replay-mode.md) can change without touching the tools.
- The tools and the graph must be testable without any model.
- Every pattern named must be visible in one package and checkable; no pattern without a component that needs it (team of 3, until 2026-12-10).

## Considered Options

- Layered architecture (interface, application, domain, infrastructure)
- Hexagonal architecture (ports and adapters), with named design patterns at component level
- Conventions of the agent stack only, no explicit style

## Decision Outcome

Chosen option: "Hexagonal architecture (ports and adapters), with named design patterns at component level", because it puts the graph and the tools at the centre and every format, provider and interface at the edge, which is exactly where the project expects change; a layered architecture would let the domain depend on the infrastructure below it, and no explicit style would give the panel nothing to check.

Patterns and where they apply:

| Pattern | Source | Where it applies | Package |
| --- | --- | --- | --- |
| Hexagonal architecture (ports and adapters) | Cockburn, 2005 | Whole system: the core defines ports (Python protocols); ingestion, export, model provider and interface are adapters | all |
| Pipes and Filters | Buschmann et al., 1996 | Ingestion: read, map to RDF, validate with SHACL, load into the graph; each filter is a function with one input and one output | `ingest` |
| Adapter | Gamma et al., 1994 | One input adapter per artifact format (requirements YAML, SysML v2 text, test cases YAML, JUnit XML results) and one output adapter (ReqIF 1.2) | `ingest`, `export` |
| Repository | Fowler, 2002; Evans, 2003 | Access to the graph: the tools ask for artifacts and links through one object that runs the SPARQL queries; no tool manipulates triples | `core` |
| ReAct (reason and act) | Yao et al., 2023 | Agent loop: the model reasons, calls a tool, reads its result, then answers; run by the GitHub Copilot SDK ([ADR-0002](0002-agent-stack-github-copilot-sdk.md)) | `copilot` |
| Chain of Responsibility | Gamma et al., 1994 | Guardrail on answers: an ordered chain of validators (cited identifiers present in the tool results of the turn, then the fallback of [ADR-0016](0016-guardrail-against-ungrounded-identifiers.md), still proposed) | `copilot` |
| Command | Gamma et al., 1994 | Write actions: each one is an object that is shown to the engineer, executed only after confirmation and logged (FR-GRD-02, FR-GRD-04) | `copilot` |
| Strategy | Gamma et al., 1994 | Model provider chosen by configuration: live model or replay of recorded responses ([ADR-0010](0010-llm-access-and-replay-mode.md)) | `llm` |

Package layout under `src/digital_thread_copilot/` and dependency rule:

| Package | Role | May import |
| --- | --- | --- |
| `core` | Graph repository, tools, ports | nothing of the project (rdflib, pySHACL only) |
| `ingest` | Ingestion pipeline and input adapters | `core` |
| `export` | ReqIF 1.2 output adapter | `core` |
| `copilot` | Agent loop, guardrail validators, write commands | `core` |
| `llm` | Live and replay providers | `copilot` (its port) |
| `ui` | Chainlit handlers only | `copilot` |

### Consequences

- Good, because the tools and the graph are tested without a model, and the replay provider makes the agent testable in CI.
- Good, because a change of format, provider or interface stays inside one adapter.
- Good, because the architecture can be shown to the panel as a short table whose every row points to code.
- Bad, because ports and adapters add a few interfaces that a small system could do without.
- Bad, because the patterns must be kept in the code: a shortcut (a tool that reads a file, the interface that calls the graph) breaks the claim.

### Confirmation

From the first code of block G: the package layout above exists, and an import-linter contract in CI enforces the "May import" column (in particular: `core` imports none of `ingest`, `export`, `copilot`, `llm`, `ui`). The architecture page (`docs/02-architecture.md`) lists each pattern with its package. This record is accepted when the pull request that adds it is approved by the decision-makers.

## Pros and Cons of the Options

### Layered architecture (interface, application, domain, infrastructure)

- Good, because: Widely known; simple to explain.
- Bad, because: The domain depends on the infrastructure layer below it; formats and provider are not isolated by construction.

### Hexagonal architecture (ports and adapters), with named design patterns at component level

- Good, because: Isolates the deterministic core; every change expected by the project is an adapter.
- Bad, because: More interfaces; the rule must be enforced to stay true.

### Conventions of the agent stack only, no explicit style

- Good, because: Least code.
- Bad, because: Nothing to show or check; does not answer the professor's request.

## More Information

- Decided by Ferdinand Lacroix on 2026-11-21 from the options above, which were prepared with an AI assistant (see [AI usage](../ai-usage.md)); the set of patterns corrects a first proposal that put the write confirmation in the guardrail chain (Command is used for it instead).
- Architecture description: terms of ISO/IEC/IEEE 42010:2022 (stakeholders, concerns, views); diagrams at the levels of the C4 model (context, containers, components) and one dynamic view, in `docs/02-architecture.md`.
- References, checked under rule R1 by Ferdinand Lacroix on 2026-11-22 against the publisher, author or standard pages: A. Cockburn, "Hexagonal architecture", HaT Technical Report 2005.02, 2005; F. Buschmann et al., Pattern-Oriented Software Architecture, vol. 1, Wiley, 1996; E. Gamma, R. Helm, R. Johnson, J. Vlissides, Design Patterns, Addison-Wesley, 1994; M. Fowler, Patterns of Enterprise Application Architecture, Addison-Wesley, 2002; E. Evans, Domain-Driven Design, Addison-Wesley, 2003; S. Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", ICLR 2023, arXiv:2210.03629; ISO/IEC/IEEE 42010:2022; S. Brown, The C4 model, https://c4model.com.
- Requirements concerned: FR-ING-01 to FR-ING-03, FR-TOOL-01 to FR-TOOL-05, FR-AGT-01, FR-GRD-01 to FR-GRD-04, FR-UI-01, NFR-OPS-03.
