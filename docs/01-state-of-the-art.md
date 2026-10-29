# Preliminary state of the art

!!! warning "Draft"
    Candidate list prepared for group selection. The group still has to (1) repeat the search in two bibliographic databases, (2) select the works to keep, (3) read the three closest works in full, and (4) update citation counts from Google Scholar.

## Search protocol

- **Main search string:** `("digital thread" OR "authoritative source of truth") AND ("knowledge graph" OR ontology) AND ("large language model" OR LLM OR "generative AI") AND (MBSE OR SysML OR traceability)`
- **Complementary strings:** `"large language model" AND SysML`, `"retrieval-augmented generation" AND traceability`, `"knowledge graph" AND "large language model" AND roadmap`, `"digital thread" AND review`
- **Date of search:** 2026-10-29
- **Sources used for this draft:** web search, publisher pages and Crossref metadata (DOI, venue, citation count)
- **Bibliographic databases (to be completed by the group):** e.g. IEEE Xplore and Scopus, through the UC3M library

## Quality criteria

Each work is assessed with the group's bibliography rule: citation count (Crossref, date of retrieval), venue quality (SJR quartile for journals, CORE rank for conferences), type of publication (peer-reviewed or preprint) and relevance to our problem. Verdict scale: **Strong** (can support an architecture decision), **Adequate** (complement or example), **Weak** (context only, never alone).

!!! note
    Citation counts come from Crossref on 2026-10-29 and are usually lower than Google Scholar. Quartiles and CORE ranks marked *approx.* are indicative and must be checked on SJR and the CORE portal.

## Closest works (to be read in full)

| # | Work | Approach | Standards | Limitation with respect to our problem | Reference |
| --- | --- | --- | --- | --- | --- |
| 1 | Quast, Jacobs, Dehn, Höpfner (2026). *Enabling Humans and AI Systems to Retrieve Information from System Architectures in MBSE*. Systems 14(1):83 | Multi-agent LLM system with GraphRAG that answers questions on a SysML v2 architecture converted into a Neo4j graph; 93 % correct answers on 100 questions | SysML v2, property graph (Neo4j) | Read-only question answering on architecture models; no requirements-to-test traceability, no actions on artifacts, no comparison with manual work | [10.3390/systems14010083](https://doi.org/10.3390/systems14010083) |
| 2 | Cibrián Sánchez, Olivert Iserte, Llorens Morillo, Álvarez Rodríguez (2025). *An agent-based approach for the automatic generation of valid SysMLv2 models in industrial contexts*. Computers in Industry 172:104350 | LLM agents with retrieval of curated SysML v2 examples and iterative validation against the official grammar | SysML v2 (ANTLR grammar) | Focused on model generation from requirements; does not exploit a digital thread across requirements, models and tests | [10.1016/j.compind.2025.104350](https://doi.org/10.1016/j.compind.2025.104350) |
| 3 | Fuchß, Hey, Keim, Liu, Ewald, Thirolf, Koziolek (2025). *LiSSA: Toward Generic Traceability Link Recovery through Retrieval-Augmented Generation*. ICSE 2025, pp. 1396-1408 | RAG pipeline that recovers trace links between documentation, architecture and code | None specific (text and code) | Recovers missing links in software projects; does not reason over an existing graph nor answer impact questions | [10.1109/ICSE55347.2025.00186](https://doi.org/10.1109/ICSE55347.2025.00186) |

## Candidate works

Sorted by verdict, then by relevance.

| # | Work | Venue and type | Citations (Crossref) | Quartile / rank | Verdict | Use in the project |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Quast et al. (2026), see above | Systems (MDPI), journal | 5 | Q2 *approx.* | Strong | Closest work; baseline for our design |
| 2 | Cibrián Sánchez et al. (2025), see above | Computers in Industry (Elsevier), journal | 24 | Q1 *approx.* | Strong | Validation loop for generated SysML v2 |
| 3 | Fuchß et al. (2025), see above | ICSE, conference | 33 | CORE A* *approx.* | Strong | RAG for traceability |
| 4 | Pan, Luo, Wang, Chen, Wang, Wu (2024). *Unifying Large Language Models and Knowledge Graphs: A Roadmap*. IEEE TKDE 36(7):3580-3599. [10.1109/TKDE.2024.3352100](https://doi.org/10.1109/TKDE.2024.3352100) | Journal | 1167 | Q1 *approx.* | Strong | Theoretical frame for LLM + KG coupling |
| 5 | Huang et al. (2025). *A Survey on Hallucination in Large Language Models*. ACM TOIS 43(2). [10.1145/3703155](https://doi.org/10.1145/3703155) | Journal | 1959 | Q1 *approx.* | Strong | Definition of the hallucination metric |
| 6 | Yao et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. [iclr.cc](https://iclr.cc/virtual/2023/oral/12647) | Conference | Not in Crossref | CORE A* *approx.* | Strong | Agent pattern for tool calling |
| 7 | Lewis et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS 2020. [papers.nips.cc](https://papers.nips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html) | Conference | Not in Crossref | CORE A* *approx.* | Strong | Origin of RAG |
| 8 | Kwon, Monnier, Barbau, Bernstein (2020). *Enriching standards-based digital thread by fusing as-designed and as-inspected data using knowledge graphs*. Advanced Engineering Informatics 46:101102. [10.1016/j.aei.2020.101102](https://doi.org/10.1016/j.aei.2020.101102) | Journal | 90 | Q1 *approx.* | Strong | Digital thread as a standards-based knowledge graph |
| 9 | Singh, Willcox (2018). *Engineering Design with Digital Thread*. AIAA Journal 56(11):4515-4528. [10.2514/1.J057255](https://doi.org/10.2514/1.J057255) | Journal | 135 | Q1 *approx.* | Strong | Foundational definition of the digital thread |
| 10 | Abdel-Aty, Negri (2024). *Conceptualizing the digital thread for smart manufacturing: a systematic literature review*. Journal of Intelligent Manufacturing 35:3629-3653. [10.1007/s10845-024-02407-1](https://doi.org/10.1007/s10845-024-02407-1) | Journal, open access | 60 | Q1 *approx.* | Strong | Traceability as a core function of the digital thread |
| 11 | Topcu, Husain, Ofsa, Wach (2025). *Trust at Your Own Peril: ... Large Language Models to Generate Expert-Like Systems Engineering Artifacts and a Characterization of Failure Modes*. Systems Engineering 28(5). [10.1002/sys.21810](https://doi.org/10.1002/sys.21810) | Journal (INCOSE) | 7 | Q1-Q2 *approx.* | Strong | Evidence that ungrounded LLMs fail in SE: motivates the cause |
| 12 | Wu, Wang, Lu, Yan, Gong, Dong, Kiritsis (2025). *Digital thread in engineering: Concept, state of art, and enabling framework*. Advanced Engineering Informatics 65:103258. [10.1016/j.aei.2025.103258](https://doi.org/10.1016/j.aei.2025.103258) | Journal | 13 | Q1 *approx.* | Strong | Recent review and reference architecture |
| 13 | Cibrián, Olivert-Iserte, Díez-Fenoy, Mendieta, Llorens, Álvarez-Rodríguez (2025). *Ensuring Semantic Consistency in SysML v2 Models Through Metamodel-Driven Validation*. IEEE Access 13:121444-121457. [10.1109/ACCESS.2025.3587786](https://doi.org/10.1109/ACCESS.2025.3587786) | Journal, open access | 12 | Q1 SJR / Q2 JCR *approx.* | Adequate | Semantic validation of generated SysML v2 |
| 14 | Hey, Fuchß, Keim, Koziolek (2025). *Requirements Traceability Link Recovery via Retrieval-Augmented Generation*. REFSQ 2025, LNCS, pp. 381-397. [10.1007/978-3-031-88531-0_27](https://doi.org/10.1007/978-3-031-88531-0_27) | Conference | 17 | CORE rank to check | Adequate | Requirement-to-requirement trace links with LLMs |
| 15 | Ali, Naganathan, Bork (2024). *Establishing Traceability Between Natural Language Requirements and Software Artifacts by Combining RAG and LLMs*. ER 2024, LNCS, pp. 295-314. [10.1007/978-3-031-75872-0_16](https://doi.org/10.1007/978-3-031-75872-0_16) | Conference | 17 | CORE A *approx.* | Adequate | Combines a knowledge-graph index with RAG |
| 16 | Esho, Hoyt, Marshall, Gadewadikar (2026). *Artificial Intelligence Enabled Systems Engineering Modeling With Retrieval Augmented Generation*. Systems Engineering 29(3). [10.1002/sys.70032](https://doi.org/10.1002/sys.70032) | Journal (INCOSE) | 3 | Q1-Q2 *approx.* | Adequate | RAG applied to SE modeling |
| 17 | Wang, Wang, Zhang, Ma, Shao, Chang (2025). *Automated Identification and Representation of System Requirements Based on LLMs and Knowledge Graphs*. Applied Sciences 15(7):3502. [10.3390/app15073502](https://doi.org/10.3390/app15073502) | Journal, open access | 13 | Q2 *approx.* | Adequate | Building a requirements knowledge graph with an LLM |
| 18 | Apvrille, Sultan (2024). *System Architects Are not Alone Anymore: Automatic System Modeling with AI*. MODELSWARD 2024, pp. 27-38. [10.5220/0012320100003645](https://doi.org/10.5220/0012320100003645) | Conference | 29 | CORE rank to check | Adequate | LLM-generated SysML with a knowledge base and feedback loop |
| 19 | Rafique, Shah, Dalecke, Grimm (2025). *Enhancing Model-Based Systems Engineering with Large Language Models*. INCOSE International Symposium 35(1). [10.1002/iis2.70067](https://doi.org/10.1002/iis2.70067) | Conference (INCOSE) | 9 | Not ranked in CORE | Adequate | SysML v2 generation, GPT-4 vs fine-tuned model |
| 20 | Wang, Ge, Liu, Cao, Chen, Hu (2025). *Generating SysML Behavior Models via Large Language Models: an Empirical Study*. Internetware 2025, pp. 366-377. [10.1145/3755881.3755926](https://doi.org/10.1145/3755881.3755926) | Conference | 6 | CORE rank to check | Adequate | Hallucinations in generated SysML models |
| 21 | Stein et al. (2026). *Prompt-Strategy-Driven SysML-v2 Artefact Generation Using Large Language Models for MBSE*. AI (MDPI) 7(8):274. [10.3390/ai7080274](https://doi.org/10.3390/ai7080274) | Journal, open access | 0 (July 2026) | Quartile to check | Weak | Prompt strategies for SysML v2 |
| 22 | Jin et al. (2025). *A System Model Generation Benchmark from Natural Language Requirements* (SysMBench). [arXiv:2508.03215](https://arxiv.org/abs/2508.03215) | Preprint | n/a | n/a | Weak | Benchmark design for OE5 |
| 23 | Edge et al. (2024). *From Local to Global: A GraphRAG Approach to Query-Focused Summarization*. Microsoft Research. [arXiv:2404.16130](https://arxiv.org/abs/2404.16130) | Preprint | n/a | n/a | Weak as a paper, see tool T4 | GraphRAG method |
| 24 | Zadenoori, Dąbrowski, Alhoshan, Zhao, Ferrari (2025). *Large Language Models for Requirements Engineering: A Systematic Literature Review*. [arXiv:2509.11446](https://arxiv.org/abs/2509.11446) | Preprint | n/a | n/a | Weak | Overview of LLM use in RE |
| 25 | Longshore, Bell, Madachy (2024). *Leveraging Generative AI to Modify and Query MBSE Models*. NPS Acquisition Research Symposium, SYM-AM-24-048. [dair.nps.edu](https://dair.nps.edu/handle/123456789/5113) | Grey literature | n/a | n/a | Weak | Querying SysML v2 with RAG |
| 26 | Cibrián, Álvarez-Rodríguez, Mendieta, Llorens (2022). *Discovering traces between textual requirements and logical models in the functional design of Printed Circuit Boards*. IEEE ICPS 2022. [10.1109/ICPS51978.2022.9816910](https://doi.org/10.1109/ICPS51978.2022.9816910) | Conference | 1 | Not ranked *approx.* | Weak | Requirements-to-logical-model traces |
| 27 | Chethan (2026). *Semantic Graph Unification for Industrial Digital Threads*. [arXiv:2608.24918](https://arxiv.org/abs/2608.24918) | Preprint, single author | n/a | n/a | Weak | RDF digital thread exposed to agents through MCP tools |

## Tools and industrial or open-source solutions

| # | Tool | Approach | Standards | Limitation with respect to our problem | Reference |
| --- | --- | --- | --- | --- | --- |
| T1 | OSLC (Open Services for Lifecycle Collaboration) | Linked-data integration of lifecycle tools; each artifact has a URI and links across tools form the digital thread | OSLC RM, QM, AM; W3C RDF | Integration standard, no natural-language access or reasoning | [Digital Threads with OSLC, INCOSE IS 2023 tutorial](https://open-services.net/files/2023/Tutorial_-_Digital_Threads_with_OSLC.pdf) |
| T2 | Syndeia (Intercax) | Commercial digital thread platform federating SysML, PLM and ALM data into a connected graph with query services | SysML, REST APIs | No conversational or generative AI layer | [Syndeia documentation](https://intercax.atlassian.net/wiki/spaces/SYN36/overview) |
| T3 | IBM DOORS Next Requirements AI assistant | RAG-style assistant answering questions on a requirements module (watsonx.ai demonstrator) | OSLC (IBM ELM) | Limited to the text of one requirements module, no graph traversal across models and tests | [IBM community post, 2025](https://community.ibm.com/community/user/sustainability/blogs/daniel-moul/2025/02/13/requirements-ai-assistant-for-doors-next) |
| T4 | Microsoft GraphRAG | Open-source pipeline that builds an entity graph from text with an LLM and answers global questions | None specific | Graph extracted from text by the LLM, not from authoritative engineering links | [graphrag on PyPI](https://pypi.org/p/graphrag), [paper](https://arxiv.org/abs/2404.16130) |
| T5 | SysML v2 Pilot Implementation (OMG Systems Modeling Community) | Reference parser and tooling for the SysML v2 textual notation | SysML v2, KerML | Modeling tool only, no traceability analysis | [GitHub](https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation) |
| T6 | GitHub Copilot SDK | Embeddable agent runtime with custom tools (public preview, April 2026) | None specific | Generic agent runtime, no engineering knowledge | [GitHub changelog](https://github.blog/changelog/2026-04-02-copilot-sdk-in-public-preview/) |

## Positioning

No work found combines the three elements of our proposal: (1) a digital thread linking requirements, SysML v2 model and tests in a standards-based graph, (2) an LLM agent restricted to deterministic tools on that graph, with mandatory citations, and (3) an evaluation against manual analysis on traceability and impact questions. The closest work (Quast et al., 2026) covers question answering on architecture models only.
