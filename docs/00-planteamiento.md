# digital-thread-copilot

**Candidate titles:** 1) `digital-thread-copilot` 2) `trace-copilot` 3) `kg-engineering-copilot`
**Selected:** `digital-thread-copilot`

- **Area:** Digital engineering and model-based systems engineering (MBSE).
- **Topic:** Conversational copilot that queries and acts on a system's digital thread (requirements, SysML v2 model and tests) represented as a knowledge graph.
- **Symptom:** Answering traceability and impact questions ("which tests verify this safety requirement?", "what is affected if I change the maximum bolus dose?") requires navigating manually across several tools and documents. It is slow and affected artifacts are missed.
- **Cause:** Artifacts live in silos with heterogeneous formats, and their relationships are neither explicit nor queryable in a unified way. Generic AI assistants have no access to this context, so they make up answers.
- **Interest:** Reduce the time spent on traceability and impact analysis and prevent a change from leaving tests or requirements unreviewed. In safety-critical systems such as medical infusion pumps, a missed trace can harm a patient and block certification.
- **Hypothesis:** If an engineer queries the digital thread through an LLM copilot grounded in a knowledge graph and deterministic tools, then they answer traceability and impact questions at least 50 % faster and with an artifact recall of at least 90 % (compared to manual search across the artifacts and to an LLM without access to the graph).

## Summary

In systems engineering projects, traceability and impact questions are answered by manually navigating across requirements, models and tests stored in silos. This project proposes `digital-thread-copilot`, a generative AI copilot that integrates these artifacts into an RDF knowledge graph aligned with standards (SysML v2, ReqIF, OSLC) and queries them through deterministic tools (SPARQL, graph traversal, test execution). It can also generate new artifacts, such as test cases or SysML v2 snippets, which are validated before being added to the repository. Every answer cites the identifiers of the artifacts it relies on. The proposal will be evaluated on the digital thread of the Generic Patient Controlled Analgesia (GPCA) infusion pump, a public research reference for medical devices, with a set of 30 reference questions, and optionally on the SysML v2 Simple Vehicle Model to check portability, measuring response time, precision, recall and hallucination rate against manual search and against an LLM without access to the graph.

## Introduction

Within digital engineering and MBSE **(AREA)**, a system's life cycle produces requirements, logical models and test cases that must remain connected in a digital thread. In practice, answering questions such as "which tests verify this requirement?" or "what is affected if I change this component?" requires going manually through several tools and documents, which is slow and prone to omissions **(SYMPTOM)**. The root of the problem is that artifacts are stored in silos with heterogeneous formats and their relationships are neither explicit nor queryable in a unified way, while generic AI assistants lack this context **(CAUSE)**.

This work aims to develop a copilot that queries and acts on the digital thread represented as a knowledge graph **(OBJECTIVE)**. We posit that, using this copilot, an engineer will answer at least 50 % faster and with an artifact recall of at least 90 % compared to manual search and to an LLM without the graph **(HYPOTHESIS)**. Solving this problem matters because impact analysis drives the verification, validation and certification of the system, especially for safety-critical devices such as infusion pumps, where software is regulated by standards like IEC 62304 **(IMPORTANCE OF SOLVING THE PROBLEM)**. If it is not solved, changes with undetected impact lead to rework, tests that are not re-run, non-conformities and, in the worst case, hazards for the patient **(CONSEQUENCES OF NOT SOLVING THE PROBLEM)**. Solving it provides faster, more complete answers that are traceable to their sources **(BENEFITS OF SOLVING THE PROBLEM)**.

There are OSLC-based life cycle management tools, commercial digital thread platforms and recent work combining LLMs and knowledge graphs, but they either offer no conversational interface or do not ground their answers in explicit relationships between artifacts (see Preliminary state of the art) **(EXISTING WORK)**. Our proposal integrates requirements, the SysML v2 model and tests into an RDF graph and exposes a set of deterministic tools to the LLM, forcing it to cite the artifacts it uses **(PROPOSED SOLUTION)**. The hypothesis will be tested with 30 reference questions on the digital thread of the GPCA infusion pump, measuring time, precision, recall and hallucination rate **(PARAMETERS TO CORROBORATE THE HYPOTHESIS)**.

## Objectives

**General objective:** Develop a generative AI engineering copilot that queries and acts on a digital thread represented as a knowledge graph, so that traceability and impact questions are answered quickly, exhaustively and grounded in the project's artifacts.

| ID | Specific objective | Output in the repository | Acceptance criterion | Traces to |
| --- | --- | --- | --- | --- |
| OE1 | Analyze the state of the art on digital threads, knowledge graphs and LLMs applied to MBSE | `docs/01-state-of-the-art.md` | At least 6 works with verified DOI or URL (3 papers and 1 tool), 2 databases searched, 3 works read in full and a comparison table | Cause, Existing work |
| OE2 | Design the system architecture and the digital thread ontology | `docs/02-architecture.md`, ADRs, `ontology/*.ttl`, `shapes/*.ttl` | The ontology covers requirement, model element and test with the satisfies, verifies and depends-on relationships; the SHACL shapes validate the case study with no errors | Cause, Proposed solution |
| OE3 | Implement the ingestion of artifacts into the knowledge graph | `src/ingest/`, `data/gpca/` | Ingestion of 3 artifact types (ReqIF/JSON requirements, SysML v2 model, test cases); 100 % of the case study artifacts loaded; unit tests in CI | Cause |
| OE4 | Implement the copilot connected to the engineering repository, with deterministic tools, artifact generation and guardrails | `src/copilot/`, web interface | The copilot reads the artifacts versioned in the repository; at least 5 tools (search, trace, impact, test execution, artifact generation); generated artifacts (test cases, SysML v2 snippets, traceability reports) are validated before being proposed; every answer cites existing IDs; write actions require confirmation and are logged; end-to-end traceability demo (requirement to model element to test to result); functional tests in CI | Hypothesis, Proposed solution |
| OE5 | Evaluate the hypothesis with a set of reference questions | `eval/`, `docs/05-evaluation.md` | 30 questions with reference answers; metrics computed automatically in CI; documented decision to accept or reject the hypothesis; optional: portability check on the secondary case study | Hypothesis, Parameters |

## Preliminary state of the art

- **Search string:** `("digital thread" OR "authoritative source of truth") AND ("knowledge graph" OR ontology) AND ("large language model" OR LLM OR "generative AI") AND (MBSE OR SysML OR traceability)`
- **Date of search:** _to be completed_
- **Databases searched:** _to be completed (e.g. IEEE Xplore and Scopus, through the UC3M library)_

| Work | Approach | Standards | Limitation with respect to our problem | Reference (DOI or URL) |
| --- | --- | --- | --- | --- |
| _to be completed_ | | | | |

> Group rule: no reference is added without checking its DOI or URL.

## Proposal

1. **Digital thread:** safety requirements, logical architecture and verification artifacts of the GPCA infusion pump. Requirements are encoded in ReqIF/JSON, part of the published architecture (AADL, Simulink/Stateflow) is translated into a SysML v2 logical model, and test cases are derived from the published verification material. Everything is loaded into an RDF graph with a lightweight ontology aligned with OSLC and SysML v2.
2. **Connection to the engineering repository:** the artifacts are versioned in the Git repository and re-ingested into the graph on every change, so the copilot always works on the current state of the project.
3. **Deterministic tools:** requirement search, trace queries (SPARQL), impact analysis by graph traversal and test execution.
4. **Artifact generation:** on request, the copilot drafts new artifacts (a test case for an uncovered requirement, a SysML v2 snippet, a traceability report). Each draft is validated (SHACL, SysML v2 parser) and only added to the repository after the engineer confirms it.
5. **Agent:** LLM orchestrated with the GitHub Copilot SDK that selects and calls the tools and always cites the artifacts used.
6. **Guardrails:** answers rejected when not grounded in the graph, separation of read and write tools, confirmation of actions and logging.
7. **Interface:** web chat with a view of the queried subgraph and of the end-to-end trace (requirement, model element, test, result).

## Validation of the proposal

- **Case study:** digital thread of the GPCA infusion pump, built from the public artifacts of the Generic Infusion Pump project (FDA, University of Pennsylvania, University of Minnesota): a subset of about 20 safety requirements, the corresponding SysML v2 model elements and the test cases that verify them. Original documents are linked, not copied, since no license is stated.
- **Secondary case study (optional, if time allows):** the *Simple Vehicle Model* from Annex A of the SysML v2 specification (official OMG repository, EPL 2.0 license). It is used only to check that the copilot works on a second, non-medical system without code changes, with a reduced set of 10 questions.
- **Dataset:** 30 traceability, impact and coverage questions with their reference answers.
- **Metrics:** time per question (s), precision and recall of cited artifacts, hallucination rate (non-existent artifacts or false relationships). Secondary metric, measured only (no threshold, the hypothesis does not depend on it): validity rate of generated artifacts (share passing SHACL and the SysML v2 parser on the first attempt).
- **Thresholds:** time reduced by at least 50 % compared to the manual process; recall and precision of at least 0.90; hallucination rate of at most 5 %.
- **Procedure:** at least 3 participants outside the group answer half of the questions manually and the other half with the copilot (crossed order). The 30 questions are also given to an LLM without access to the graph as a second baseline.

## Standards involved

| Standard | Use in the project |
| --- | --- |
| SysML v2 | Logical model of the system (textual notation) |
| ReqIF | Requirements interchange |
| OWL / RDF | Domain ontology and knowledge graph |
| SPARQL | Traceability and impact queries |
| SHACL | Integrity validation of the graph |
| OSLC (RM, QM) | Vocabulary for traceability links between requirements and tests |
| OpenAPI / JSON | Definition of the agent's tools |
| AADL | Source architecture of the GPCA case study, partially translated into SysML v2 |
| IEC 62304, ISO 14971 | Context only: medical device software life cycle and risk management, which motivate traceability in the case study |

## AI usage statement

- _Tool:_ Claude (Anthropic). _Use:_ proposed structure, draft wording and translation of the problem statement, reviewed and validated by the group.
- _To be completed with every later use (search synonyms, summaries, page layout, etc.)._

The hypothesis and the objectives are the group's decision.

## References

Case study sources (URLs checked on 2026-10-22):

- University of Pennsylvania, *The Generic Infusion Pump (GIP) project*. https://rtg.cis.upenn.edu/gip-UPenn/
- University of Minnesota, *GPCA artifacts: system requirements, AADL and Simulink/Stateflow models, verification suite* (2015). https://crisys.cs.umn.edu/gpca.shtml
- *Generic Infusion Pump Hazard Analysis and Safety Requirements, Version 1.0*, Technical Report MS-CIS-08-31, University of Pennsylvania, 2009. https://repository.upenn.edu/cis_reports/893
- Object Management Group, *SysML v2 release repository* (example models, including the Annex A Simple Vehicle Model; EPL 2.0). https://github.com/systems-modeling/sysml-v2-release

_State of the art references: to be completed, only with a verified DOI or URL._
