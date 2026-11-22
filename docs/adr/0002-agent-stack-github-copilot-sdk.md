---
status: accepted
date: 2026-11-15
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# Agent stack: GitHub Copilot SDK inside the system

## Context and Problem Statement

The statement makes generative AI mandatory and names OpenSpec and the GitHub Copilot SDK as reference tools, "not only prompts" (PROYECTO_FINAL.pdf, p. 4). The copilot needs an agent loop that selects and calls our deterministic tools. The evaluator must be able to run the system without our credentials (p. 9).

## Decision Drivers

- Use one of the two reference tools of the statement, so that no approval is needed.
- The agent must be restricted to our own tools.
- The model, its provider and its key are set by configuration, not by code.
- The cost of the evaluation runs stays under 2 EUR.

## Considered Options

- GitHub Copilot SDK inside the system
- OpenSpec in the development process only
- Both

## Decision Outcome

Chosen option: "GitHub Copilot SDK inside the system", because it is a reference tool of the statement and the feasibility spike of 2026-11-16 passed its three fail conditions: a custom tool is called with bring-your-own-key and no GitHub account, the agent can be restricted to our tools with an allowlist (`available_tools`, custom tools as `custom:<name>`), and the same SDK runs without tools as the comparison configuration.

### Consequences

- Good, because the agent stack needs no approval and one SDK serves the copilot and the reference configurations.
- Bad, because the SDK fixes parts of the prompt and exposes few generation settings, so run-to-run variability must be measured by repetitions; an available tool is not always called, which the guardrail of ADR-0016 must catch.

### Confirmation

The functional tests of step H2 call the agent through the SDK with tools registered as `custom:<name>`; a test asserts that the comparison configuration registers 0 tool (step H6). Version pinned: `github-copilot-sdk` 1.0.34. This record is accepted when the pull request that adds it is approved by the decision-makers.

## Pros and Cons of the Options

### GitHub Copilot SDK inside the system

- Good, because: Matches the problem statement; reference tool of the statement; bring-your-own-key works without a GitHub account (spike H0).
- Bad, because: The agent's own instructions describe a coding agent and cost about 1550 tokens per request; no temperature or seed parameter.

### OpenSpec in the development process only

- Good, because: Reuses the experience of Practica 1.
- Bad, because: The copilot itself would need another agent framework, to be approved by the professor.

### Both

- Good, because: Covers "process and/or system" fully.
- Bad, because: About 3 h more (step C3), not available in the reduced scope.

## More Information

- Decision identifier in the project plan: T2. Decided by Ferdinand Lacroix on 2026-11-15 from the options above, which were prepared with an AI assistant (see [AI usage](../ai-usage.md)).
- Requirements concerned: FR-TOOL-01 to FR-TOOL-04, FR-GRD-01. Identifiers are those of the project requirements v3 of Practica 1; they are rebaselined in step C1.
- Fallback stated to the professor on 2026-11-15: another agent framework with OpenSpec in the process, subject to his approval (step C3 then becomes a must). Confirmed after the spike on 2026-11-16.
