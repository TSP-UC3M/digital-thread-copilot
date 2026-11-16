# Preliminary state of the art

!!! warning "Draft"
    Candidate list prepared for group selection from a web search, before the search protocol below was fixed. The group still has to (1) run the search in the two bibliographic databases of the protocol, (2) select the works to keep, (3) read the three closest works in full, and (4) update citation counts from Google Scholar.

## Search protocol

Protocol fixed on 2026-11-16, before any query in a bibliographic database. It is a scoped review carried out by three students in a few hours, not a full systematic literature review; its structure follows the guidelines of Kitchenham and Charters [M3], complemented by [M4], and its reporting follows the flow of PRISMA 2020 [M1].

### Question

Which published approaches let an engineer query or act on a digital thread (requirements, system models, tests) through a large language model, and how do they ground their answers in the links between artifacts?

Each work is read for: (a) the artifacts and standards involved; (b) the grounding mechanism (retrieval over text, knowledge graph, tools); (c) how the approach is evaluated, against which baseline and with which metrics.

### Sources

| Source | Access | Fields searched |
| --- | --- | --- |
| IEEE Xplore | UC3M library | All Metadata (command search) |
| Scopus | UC3M library | Title, abstract, keywords |
| Other methods | See below | |

### Search strings

Period: 2020 to 2026. The question concerns systems built on large language models, and we take GPT-3, described in 2020 [M6], as the first model usable for the tasks studied here; this starting point is our choice, not a claim of that paper. Earlier foundational works, for example on the digital thread or on traceability, are not excluded from the state of the art: they enter through snowballing or other methods and are labelled as such. Language: English.

S1, main string:

- Scopus: `TITLE-ABS-KEY ( ( "digital thread" OR "authoritative source of truth" ) AND ( "knowledge graph" OR ontology ) AND ( "large language model" OR LLM OR "generative AI" ) AND ( MBSE OR SysML OR traceability ) ) AND PUBYEAR > 2019`
- IEEE Xplore: `("All Metadata":"digital thread" OR "All Metadata":"authoritative source of truth") AND ("All Metadata":"knowledge graph" OR "All Metadata":ontology) AND ("All Metadata":"large language model" OR "All Metadata":LLM OR "All Metadata":"generative AI") AND ("All Metadata":MBSE OR "All Metadata":SysML OR "All Metadata":traceability)`, years 2020 to 2026

S2, wider string (S1 has four conjunctive groups and is expected to return few records):

- Scopus: `TITLE-ABS-KEY ( ( "large language model" OR LLM OR "generative AI" OR "retrieval-augmented generation" ) AND ( MBSE OR SysML OR "model-based systems engineering" OR "digital thread" ) AND ( traceability OR "knowledge graph" OR "impact analysis" OR "question answering" ) ) AND PUBYEAR > 2019`
- IEEE Xplore: `("All Metadata":"large language model" OR "All Metadata":LLM OR "All Metadata":"generative AI" OR "All Metadata":"retrieval-augmented generation") AND ("All Metadata":MBSE OR "All Metadata":SysML OR "All Metadata":"model-based systems engineering" OR "All Metadata":"digital thread") AND ("All Metadata":traceability OR "All Metadata":"knowledge graph" OR "All Metadata":"impact analysis" OR "All Metadata":"question answering")`, years 2020 to 2026 (string written in full on 2026-11-16, as run; the protocol frozen before the queries described it as "the same three groups with All Metadata")

Refinement. There is no fixed cap on the number of records. If a string returns more than 100 records in one database, the string is refined until the volume is at most 100, and every iteration is recorded (string as run, date, number of records, reason for the change). A refinement may only add or tighten a group of terms; it never removes records after reading them. A cap is a last resort: if one is used, the sorting criterion (relevance as ranked by the database) and the number of records left unscreened are reported as a threat to validity.

### Record of the queries

| Database | String and iteration | Date | Records returned | Reason for the change | Export file |
| --- | --- | --- | --- | --- | --- |
| IEEE Xplore | S1, iteration 1 (Command Search, years 2020 to 2026) | 2026-11-16, about 20:13 | 1 | None | `ieee-s1.csv` |
| IEEE Xplore | S2, iteration 1 (Command Search, years 2020 to 2026) | 2026-11-16, about 20:13 | 13 | None | `ieee-s2.csv` |
| Scopus | S1, iteration 1 (Advanced search, Documents) | 2026-11-16, before 20:19 | 0 | None | None (no record) |
| Scopus | S2, iteration 1 (Advanced search, Documents) | 2026-11-16, about 20:19 | 50 | None | `scopus-s2.csv` |

Queries run by Ferdinand Lacroix after the protocol was merged (pull request 6). Times are those of the export files, Europe/Paris. No string returned more than 100 records, so no refinement was made. Records identified: 64; after removal of duplicates between the result sets (by DOI, then by normalised title): 53.

Reduced exports (title, year, source, type, DOI, origin) are kept in `references/search-2026-11-16/` so that the counts can be recomputed.

Deviations from the protocol as frozen:

- Two invalid attempts were made and are not counted. The Scopus S1 string was pasted by mistake into IEEE Xplore. The Scopus S1 string was first run in the basic search, which wrapped it in a second `TITLE-ABS-KEY` so that `PUBYEAR` ended up inside it; it was run again in the advanced search, which returned 0 record, the only result counted.
- The IEEE Xplore S2 string was written in full only when it was run.
- The protocol said that the exports would be kept in the repository. Only reduced exports are published, because the repository is public and the terms of use of the databases for full exports with abstracts were not established; the reason is given in the README of that folder.
- The Scopus strings have no upper year bound. The 6 records dated 2027 are excluded under inclusion criterion 3 and counted in the flow with that reason.

Interpretation of the criteria, fixed on 2026-11-16 before the screening and given to both screeners: a record that describes a whole proceedings volume (type "Conference review" in Scopus) is not an individual work and is excluded under exclusion criterion 1. The protocol does not name this case; 12 of the 53 records are of this type.

Screening procedure (communicated to both screeners on 2026-11-16 before screening; committed after). The protocol frozen before the queries lists the criteria but neither the order in which they are applied nor what to do in case of doubt. Both screeners received and applied the following steps; an excluded record is counted under one criterion, the first that applies in this order:

1. Whole proceedings volume, editorial, tutorial or position text without results: exclude, exclusion criterion 1. Year outside 2020 to 2026 or not in English: exclude, inclusion criterion 3.
2. No large language model or generative AI: exclude, inclusion criterion 1.
3. The model does not work on engineering artifacts (requirements, system models, tests, or their links): code only, exclusion criterion 4; manufacturing or operations data only, exclusion criterion 2; otherwise inclusion criterion 1.
4. None of traceability, impact analysis, question answering over models, knowledge graph or ontology of the artifacts, generation of artifacts with validation: exclude, inclusion criterion 2.
5. No evaluation or demonstration on a set of artifacts: exclude, exclusion criterion 1.
6. Otherwise include. In case of doubt from the abstract alone, the record is included and flagged; the doubt is settled on the full text.

The evidence that this procedure predates the screening is its sending to the second screener, not a commit: it was written into this page after the double screening of the sample.

### Selection

Inclusion criteria (all must hold):

1. The work uses a large language model on systems engineering or software engineering artifacts (requirements, models, tests, or the links between them).
2. It addresses at least one of: traceability, impact analysis, question answering over models, a knowledge graph or ontology of the artifacts, generation of model or test artifacts with validation.
3. It is a journal article, a conference paper or a preprint with identifiable authors, in English, dated 2020 to 2026.

Exclusion criteria (any one excludes):

1. No evaluation or demonstration on a set of artifacts (position papers, editorials, tutorials).
2. The digital thread or the knowledge graph concerns manufacturing or operations data only, with no engineering artifacts.
3. Full text not accessible through UC3M, or duplicate of a record already kept (the journal version is kept over the preprint).
4. Code generation or code completion only.

Steps:

1. Remove duplicates between the result sets.
2. Screen titles and abstracts against the criteria, by one member. A second member, the one who does not run the searches, independently screens a random 20 % of the titles, drawn with a recorded seed. The agreement is reported as Cohen's kappa [M5] together with the 2 x 2 table of decisions, without a qualitative label; disagreements are resolved by discussion and counted.
3. Read the full text of the remaining records.
4. Apply the quality criteria of the next section to each.
5. Keep 8 works, of which at least 3 papers and 1 tool. When more than 8 pass, they are ranked by verdict (Strong before Adequate), then by the number of reading points (a) to (c) they answer, then by year. The 3 closest works are read in full.

### Other methods

Counted separately in the flow, never merged with the database counts:

- the candidates of the web search of 2026-10-29 (strings and sources: main string above and the complementary strings `"large language model" AND SysML`, `"retrieval-augmented generation" AND traceability`, `"knowledge graph" AND "large language model" AND roadmap`, `"digital thread" AND review`; web search, publisher pages and Crossref metadata) that the two databases do not return;
- backward and forward snowballing from the works kept, limited to one level [M2];
- tools and standards, which are not indexed as papers and are found on vendor or project sites.

For each of the 8 works kept, the comparison table states its origin: IEEE Xplore, Scopus, both, or other method.

### Flow to report

| Stage | Databases | Other methods |
| --- | --- | --- |
| Records identified | per database and string | per method |
| Duplicates removed | | |
| Records screened (title and abstract) | | |
| Records excluded, with the count per exclusion criterion | | |
| Full texts assessed | | |
| Full texts excluded, with reasons | | |
| Works included | | |

### Threats to validity

- Two databases and two strings: relevant works indexed elsewhere are found only through other methods. Only 2 of the 20 works with a DOI in the candidate list of 2026-10-29 are returned by the two databases.
- The Scopus strings set no upper bound on the year, so records dated 2027 were returned and had to be excluded at screening.
- Recent field: many relevant works are preprints, which our quality criteria grade Weak.
- Screening mostly by one person; the 20 % double screening only estimates the agreement, and on a small sample Cohen's kappa is unstable.
- Refining the strings after seeing the number of results can bias the search towards expected works; every iteration is recorded for that reason.
- The candidate list of 2026-10-29 was seen before this protocol was written, which can bias the criteria.
- Citation counts and rankings are read on a given date and change.

### Methodological references

Checked on 2026-11-16. BibTeX entries: `docs/references.bib`.

| # | Reference | Type | Citations (source) | Venue quality | Verdict |
| --- | --- | --- | --- | --- | --- |
| M1 | M. J. Page et al., "The PRISMA 2020 statement: an updated guideline for reporting systematic reviews," *BMJ*, vol. 372, n71, 2021, doi: [10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71) | Journal article, peer reviewed | 194 613 (Google Scholar), 87 502 (Crossref) | SJR 2025: Q1 | Strong |
| M2 | C. Wohlin, "Guidelines for snowballing in systematic literature studies and a replication in software engineering," in *Proc. 18th Int. Conf. Evaluation and Assessment in Software Engineering (EASE '14)*, 2014, pp. 1-10, doi: [10.1145/2601248.2601268](https://doi.org/10.1145/2601248.2601268) | Conference paper | 2 880 (Crossref) | ICORE2026: A | Strong |
| M3 | B. Kitchenham and S. Charters, "Guidelines for performing systematic literature reviews in software engineering," version 2.3, Keele University and University of Durham, EBSE Tech. Rep. EBSE-2007-01, Jul. 2007. [Online]. Available: <https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf> | Technical report, not peer reviewed | Not in Crossref | Not applicable | Adequate |
| M4 | B. A. Kitchenham, D. Budgen, and P. Brereton, *Evidence-Based Software Engineering and Systematic Reviews*. Boca Raton, FL, USA: CRC Press, 2016, ISBN 978-1-4822-2866-3 (electronic edition; the print edition is dated November 2015 by booksellers) | Book | Not applicable | Not applicable | Adequate |
| M5 | J. Cohen, "A coefficient of agreement for nominal scales," *Educational and Psychological Measurement*, vol. 20, no. 1, pp. 37-46, 1960, doi: [10.1177/001316446002000104](https://doi.org/10.1177/001316446002000104) | Journal article | 32 214 (Crossref) | SJR quartile not read yet | Strong, pending the quartile |
| M6 | T. B. Brown et al., "Language models are few-shot learners," in *Advances in Neural Information Processing Systems 33 (NeurIPS 2020)*, 2020, pp. 1877-1901, arXiv: [2005.14165](https://arxiv.org/abs/2005.14165) | Conference paper | Not in Crossref | CORE rank not read yet | Strong, pending the rank |

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
