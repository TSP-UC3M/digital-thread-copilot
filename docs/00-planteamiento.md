# digital-thread-copilot

!!! note "Status: objectives validated"
    The professor validated objectives OE1 to OE5 in class on 2026-11-19 and asked for concrete choices. The architecture, its design patterns, the ontology and the format of every artifact are now named on this page and in the architecture page (`docs/02-architecture.md`, ADR-0017). The hypothesis, objective OE4 and the figures of the evaluation were revised in November 2026 (scope decisions recorded in [ADR-0001](adr/0001-project-framing.md)).

**Candidate titles:** 1) `digital-thread-copilot` 2) `trace-copilot` 3) `kg-engineering-copilot`
**Selected:** `digital-thread-copilot`

- **Area:** Digital engineering and model-based systems engineering (MBSE).
- **Topic:** Conversational copilot that queries and acts on a system's digital thread (requirements, SysML v2 model and tests) represented as a knowledge graph.
- **Symptom:** Answering traceability and impact questions ("which tests verify this safety requirement?", "what is affected if I change the maximum bolus dose?") requires navigating manually across several tools and documents. It is slow and affected artifacts are missed.
- **Cause:** Artifacts live in silos with heterogeneous formats, and their relationships are neither explicit nor queryable in a unified way. Generic AI assistants have no access to this context, so they make up answers.
- **Interest:** Reduce the time spent on traceability and impact analysis and prevent a change from leaving tests or requirements unreviewed. In safety-critical systems such as medical infusion pumps, a missed trace can harm a patient and block certification.
- **Hypothesis:** If traceability, impact and coverage questions on a digital thread are answered by an LLM copilot restricted to deterministic tools over a knowledge graph of the artifacts, then its answers cite the correct artifacts with a recall and a precision of at least 0.90 and a hallucination rate of at most 5 %, and with a significantly higher recall than the same LLM given all the artifacts as text in its context, without graph or tools (paired test on the same questions, p < 0.05). Secondary, indicative observation: engineers using the copilot answer at least 50 % faster than by manual search (3 participants, 10 questions each).

## Summary

In systems engineering projects, traceability and impact questions are answered by manually navigating across requirements, models and tests stored in silos. This project proposes `digital-thread-copilot`, a generative AI copilot that integrates these artifacts into an RDF knowledge graph aligned with standards (SysML v2, ReqIF, OSLC) and queries them through deterministic tools (SPARQL, graph traversal, test execution). It can also draft a test case for a requirement that no test verifies; the draft is validated before being added to the repository. Every answer cites the identifiers of the artifacts it relies on. The proposal will be evaluated on the digital thread of the Generic Patient Controlled Analgesia (GPCA) infusion pump, a public research reference for medical devices, with a set of 20 reference questions, measuring precision, recall and hallucination rate against the same LLM without graph or tools and, as an indicative measure, response time against manual search.

## Introduction

Within digital engineering and MBSE **(AREA)**, a system's life cycle produces requirements, logical models and test cases that must remain connected in a digital thread. In practice, answering questions such as "which tests verify this requirement?" or "what is affected if I change this component?" requires going manually through several tools and documents, which is slow and prone to omissions **(SYMPTOM)**. The root of the problem is that artifacts are stored in silos with heterogeneous formats and their relationships are neither explicit nor queryable in a unified way, while generic AI assistants lack this context **(CAUSE)**.

This work aims to develop a copilot that queries and acts on the digital thread represented as a knowledge graph **(OBJECTIVE)**. We posit that the answers of this copilot cite the correct artifacts with a recall and a precision of at least 0.90 and a hallucination rate of at most 5 %, and with a significantly higher recall than the same LLM given all the artifacts as text, without graph or tools **(HYPOTHESIS)**. Solving this problem matters because impact analysis drives the verification, validation and certification of the system, especially for safety-critical devices such as infusion pumps, where software is regulated by standards like IEC 62304 **(IMPORTANCE OF SOLVING THE PROBLEM)**. If it is not solved, changes with undetected impact lead to rework, tests that are not re-run, non-conformities and, in the worst case, hazards for the patient **(CONSEQUENCES OF NOT SOLVING THE PROBLEM)**. Solving it provides faster, more complete answers that are traceable to their sources **(BENEFITS OF SOLVING THE PROBLEM)**.

There are OSLC-based life cycle management tools, commercial digital thread platforms and recent work combining LLMs and knowledge graphs, but they either offer no conversational interface or do not ground their answers in explicit relationships between artifacts (see Preliminary state of the art) **(EXISTING WORK)**. Our proposal integrates requirements, the SysML v2 model and tests into an RDF graph and exposes a set of deterministic tools to the LLM, forcing it to cite the artifacts it uses **(PROPOSED SOLUTION)**. The hypothesis will be tested with 20 reference questions on the digital thread of the GPCA infusion pump, measuring precision, recall and hallucination rate, and time as an indicative measure **(PARAMETERS TO CORROBORATE THE HYPOTHESIS)**.

## Objectives

**General objective:** Develop a generative AI engineering copilot that queries and acts on a digital thread represented as a knowledge graph, so that traceability and impact questions are answered quickly, exhaustively and grounded in the project's artifacts.

| ID | Specific objective | Output in the repository | Acceptance criterion | Traces to |
| --- | --- | --- | --- | --- |
| OE1 | Analyze the state of the art on digital threads, knowledge graphs and LLMs applied to MBSE | `docs/01-state-of-the-art.md` | 8 works with verified DOI or URL (at least 3 papers and 1 tool), selected by a systematic search in IEEE Xplore and Scopus completed by other documented methods; 3 works read in full and a comparison table | Cause, Existing work |
| OE2 | Design the system architecture and the digital thread ontology | `docs/02-architecture.md`, ADRs, `ontology/digital-thread.ttl`, `shapes/digital-thread-shapes.ttl` | Hexagonal architecture (ports and adapters) described with the views of ISO/IEC/IEEE 42010 at the C4 levels, each design pattern linked to its package (ADR-0017); ontology in OWL 2 (Turtle), aligned with OSLC RM and QM 2.1, covering requirement, model element, test case, test result and verification method with the satisfies, verifies, depends-on and reports-on relationships; the SHACL shapes validate the case study with no errors and detect each broken fixture | Cause, Proposed solution |
| OE3 | Implement the ingestion of artifacts into the knowledge graph | `src/digital_thread_copilot/ingest/`, `data/gpca/` | Ingestion pipeline (read, map to RDF, validate with SHACL, load) for 3 artifact types: requirements in YAML validated by JSON Schema, with a ReqIF 1.2 export; SysML v2 model in textual notation; test cases in YAML and their results in JUnit XML; 100 % of the case study artifacts loaded; unit tests in CI | Cause |
| OE4 | Implement the copilot connected to the engineering repository, with deterministic tools, test case generation and guardrails | `src/digital_thread_copilot/copilot/`, `src/digital_thread_copilot/ui/` (Chainlit web chat) | The copilot reads the artifacts versioned in the repository; at least 5 tools (search, trace, impact, test execution, coverage gaps); a draft test case generated for an uncovered requirement is validated before being proposed; every answer cites existing IDs; write actions require confirmation and are logged; web chat; end-to-end traceability demonstration (requirement to model element to test to result); functional tests in CI. Extensions, built only if time allows: generated SysML v2 snippets and traceability reports; view of the queried subgraph and of the trace; re-ingestion on every change of an artifact | Hypothesis, Proposed solution |
| OE5 | Evaluate the hypothesis with a set of reference questions | `eval/`, `docs/05-evaluation.md` | 20 questions with reference answers; metrics computed automatically in CI; documented decision to accept or reject the hypothesis | Hypothesis, Parameters |

## Preliminary state of the art

- **Search string:** `("digital thread" OR "authoritative source of truth") AND ("knowledge graph" OR ontology) AND ("large language model" OR LLM OR "generative AI") AND (MBSE OR SysML OR traceability)`
- **Date of search:** _to be completed_
- **Databases searched:** _to be completed (e.g. IEEE Xplore and Scopus, through the UC3M library)_

| Work | Approach | Standards | Limitation with respect to our problem | Reference (DOI or URL) |
| --- | --- | --- | --- | --- |
| _to be completed_ | | | | |

> Group rule: no reference is added without checking its DOI or URL.

## Proposal

1. **Digital thread:** safety requirements, logical architecture and verification artifacts of the GPCA infusion pump. Requirements are written in YAML, validated by JSON Schema and exported to ReqIF 1.2, part of the published architecture (AADL, Simulink/Stateflow) is translated into a SysML v2 logical model, and test cases are derived from the published verification material. Everything is loaded into an RDF graph with a lightweight ontology in OWL 2 (Turtle, `ontology/digital-thread.ttl`) aligned with OSLC and SysML v2, checked by SHACL shapes.
2. **Connection to the engineering repository:** the artifacts are versioned in the Git repository and loaded into the graph when the system starts. Extension: re-ingestion on every change, so that the copilot always works on the current state of the project.
3. **Deterministic tools:** requirement search, trace queries (SPARQL), impact analysis by graph traversal and test execution.
4. **Artifact generation:** on request, the copilot drafts a test case for a requirement that no test verifies. The draft is validated against its schema and only added to the repository after the engineer confirms it. Extension: SysML v2 snippets, validated with the SysML v2 parser, and traceability reports.
5. **Agent:** LLM orchestrated with the GitHub Copilot SDK following the ReAct pattern (reason, call a tool, read its result, answer): it selects and calls the tools and always cites the artifacts used.
6. **Guardrails:** answers rejected when not grounded in the graph, separation of read and write tools, confirmation of actions and logging.
7. **Interface:** web chat built with Chainlit, a thin layer without logic. Extension: a view of the queried subgraph and of the end-to-end trace (requirement, model element, test, result).
8. **Architecture:** hexagonal (ports and adapters): the graph and the tools form the core; ingestion (Pipes and Filters, one Adapter per format), ReqIF export, model provider (Strategy: live model or replay) and interface are adapters. The guardrail is a chain of validators (Chain of Responsibility) and every write is a confirmed, logged Command. Detail: `docs/02-architecture.md` and ADR-0017.

## Validation of the proposal

- **Case study:** digital thread of the GPCA infusion pump, built from the public artifacts of the Generic Infusion Pump project (FDA, University of Pennsylvania, University of Minnesota): a subset of 12 safety requirements, the corresponding SysML v2 model elements and the 12 test cases that verify them. Original documents are linked, not copied, since no license is stated.
- **Dataset:** 20 traceability, impact and coverage questions with their reference answers.
- **Metrics:** precision and recall of cited artifacts, hallucination rate (non-existent artifacts or false relationships), time per question (s). Secondary metric, measured only (no threshold, the hypothesis does not depend on it): validity rate of generated test cases (share passing validation on the first attempt).
- **Thresholds:** recall and precision of at least 0.90; hallucination rate of at most 5 %; recall significantly higher than that of reference configuration (ii) below (paired test on the same questions, p < 0.05). Indicative only, outside the acceptance criterion: time reduced by at least 50 % compared to the manual process.
- **Procedure:** the 20 questions are run 3 times on three configurations that use the same model, version and parameters: the copilot; (i) the LLM with the question only, reported as a lower bound; (ii) the LLM with the text of all the artifacts in its context, without graph or tools. The criterion compares the copilot with (ii). Separately, 3 participants outside the group each answer 10 questions, half manually and half with the copilot (crossed order). Threat to validity: the case study is small, so all the artifacts fit in the context of (ii) and the difference may be small.

## Standards involved

| Standard | Use in the project |
| --- | --- |
| SysML v2 | Logical model of the system (textual notation) |
| ReqIF 1.2 (OMG) | Export of the requirements, written in YAML and validated by JSON Schema |
| OWL 2 / RDF (Turtle) | Ontology `ontology/digital-thread.ttl` and knowledge graph |
| SPARQL | Traceability and impact queries |
| SHACL | Integrity validation of the graph (`shapes/digital-thread-shapes.ttl`) |
| JUnit XML | Test results loaded into the graph |
| ISO/IEC/IEEE 42010 | Architecture description by views (`docs/02-architecture.md`) |
| OSLC (RM, QM) | Vocabulary for traceability links between requirements and tests |
| JSON Schema | Validation of the requirement and test case files; definition of the agent's tools |
| AADL | Source architecture of the GPCA case study, partially translated into SysML v2 |
| IEC 62304, ISO 14971 | Context only: medical device software life cycle and risk management, which motivate traceability in the case study |

## AI usage statement

- _Tool:_ Claude (Anthropic). _Use:_ proposed structure, draft wording and translation of the problem statement, reviewed and validated by the group.
- _Tool:_ Claude (Anthropic). _Dates:_ 2026-11-15 and 2026-11-16. _Use (project framing):_ diagnosis of the failed documentation workflow and wording of its fix; effort estimates and scope scenarios; option tables with a recommendation for each framing decision; proposal to split the hypothesis into a primary and a secondary criterion and proposed definition of the primary criterion (thresholds, reference configurations, paired test); checklists for the verification of references; an independent review of the framing by a second AI agent. _Review by the group:_ every decision was taken by a group member from the options presented, and the framing is submitted to the three members for approval in ADR-0001 (`docs/adr/0001-project-framing.md`). The validation request sent to the professor on 2026-11-15 was written by the group.
- Later uses are listed on the [AI usage](ai-usage.md) page.

The hypothesis and the objectives are the group's decision.

## References

Case study sources (URLs checked on 2026-10-22):

- University of Pennsylvania, *The Generic Infusion Pump (GIP) project*. https://rtg.cis.upenn.edu/gip-UPenn/
- University of Minnesota, *GPCA artifacts: system requirements, AADL and Simulink/Stateflow models, verification suite* (2015). https://crisys.cs.umn.edu/gpca.shtml
- *Generic Infusion Pump Hazard Analysis and Safety Requirements, Version 1.0*, Technical Report MS-CIS-08-31, University of Pennsylvania, 2009. https://repository.upenn.edu/cis_reports/893
- Object Management Group, *SysML v2 release repository* (example models, including the Annex A Simple Vehicle Model; EPL 2.0). https://github.com/systems-modeling/sysml-v2-release

_State of the art references: to be completed, only with a verified DOI or URL._
