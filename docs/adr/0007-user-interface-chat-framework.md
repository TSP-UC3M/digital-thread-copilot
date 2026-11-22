---
status: accepted
date: 2026-11-21
decision-makers: Ferdinand Lacroix
consulted: Séléné Colle Conte, Elio Bonnenfant
---

# User interface: Chainlit chat as a thin adapter

## Context and Problem Statement

Objective OE4 asks for a web interface; the statement presents the copilot as the interface to the digital thread (PROYECTO_FINAL.pdf, p. 7). The first version of this record, on 2026-11-15, chose "a chat framework (Chainlit or Streamlit)" and left the framework open. On 2026-11-19 the professor asked for concrete, named choices; the panel of 3 professors ranks the projects from the presentation and its demonstration.

## Decision Drivers

- A working chat in hours, not days.
- Served by the single start command.
- One scripted browser test must be possible.
- The panel must see which tool the agent called and which identifiers it returned (the claim of the project is traceability).
- The agent stack is asynchronous (the GitHub Copilot SDK is called with `await`, see the spike of 2026-11-16).

## Considered Options

- Chainlit, as a thin adapter over the copilot package
- Streamlit, as a thin adapter over the copilot package
- Custom web front end
- Command line only

## Decision Outcome

Chosen option: "Chainlit, as a thin adapter over the copilot package", because the core of the product is a conversational agent: Chainlit shows each tool call as a step with its inputs and outputs, streams answers and runs asynchronous code natively, while Streamlit re-runs its whole script on every message and would need the agent session and the event loop to be kept by hand. Decision rule recorded with the choice: Chainlit while the agent is the core and any graphical view only displays results of the agent; Streamlit only if a policy forbade community-maintained dependencies or if the application became first a data analysis tool with a small chat.

The interface is an adapter of the hexagonal architecture (ADR-0017, added with the architecture page): the package `digital_thread_copilot.ui` holds only the Chainlit handlers and calls the copilot package; no tool, prompt or guardrail logic lives there, so that replacing the framework costs little.

### Consequences

- Good, because effort stays on the tools and the evaluation, and the tool calls are visible in the demonstration without extra code.
- Good, because the version is pinned and the layer is small: the maintenance risk below is bounded.
- Bad, because Chainlit is community-maintained since May 2025 (the original team stepped back; maintainers work under a maintainer agreement, without warranty from Chainlit SAS).
- Bad, because the graph and trace view (step H9, an extension) is less flexible than with a data application framework.

### Confirmation

A scripted browser test asks one question and reads an answer that contains an artifact identifier (step H8). An import-linter contract in CI forbids any import of `digital_thread_copilot.ui` from the other packages. This record is accepted when the pull request that adds it is approved by the decision-makers.

## Pros and Cons of the Options

### Chainlit, as a thin adapter over the copilot package

- Good, because: Made for chat and agent interfaces; tool steps, streaming and asynchronous code are native.
- Bad, because: Community-maintained; smaller ecosystem.

### Streamlit, as a thin adapter over the copilot package

- Good, because: Actively maintained, large community, flexible for charts and tables.
- Bad, because: Whole script re-run on each interaction; agent steps and asynchronous calls to write by hand.

### Custom web front end

- Good, because: Full control, richer trace view.
- Bad, because: 2 to 3 times the effort.

### Command line only

- Good, because: Cheapest.
- Bad, because: Weak for the panel vote; contradicts OE4.

## More Information

- Decision identifier in the project plan: T8. Decided by Ferdinand Lacroix on 2026-11-15 (a chat framework), then on 2026-11-21 (Chainlit, with the decision rule above), from the options above, which were prepared with an AI assistant (see [AI usage](../ai-usage.md)).
- Versions read on 2026-11-21 on PyPI: chainlit 2.12.0 (August 2026, community-maintained notice on the page), streamlit 1.67.0 (2026-11-05). The version used is pinned in step H8.
- Requirements concerned: FR-UI-01, FR-UI-02.
