# digital-thread-copilot

!!! note "Traduction"
    Cette page est une traduction. La version de référence est la version anglaise.

**Titres candidats :** 1) `digital-thread-copilot` 2) `trace-copilot` 3) `kg-engineering-copilot`
**Retenu :** `digital-thread-copilot`

- **Domaine :** Ingénierie numérique et ingénierie des systèmes basée sur les modèles (MBSE).
- **Sujet :** Copilote conversationnel qui interroge le fil numérique (digital thread) d'un système et agit dessus (exigences, modèle SysML v2 et tests), représenté sous forme de graphe de connaissances.
- **Symptôme :** Répondre aux questions de traçabilité et d'impact (« quels tests vérifient cette exigence de sécurité ? », « qu'est-ce qui est impacté si je change la dose maximale de bolus ? ») oblige à naviguer à la main entre plusieurs outils et documents. C'est lent et des artefacts impactés sont oubliés.
- **Cause :** Les artefacts sont stockés en silos, dans des formats hétérogènes, et leurs relations ne sont ni explicites ni interrogeables de façon unifiée. Les assistants d'IA génériques n'ont pas accès à ce contexte et inventent donc des réponses.
- **Intérêt :** Réduire le temps consacré à l'analyse de traçabilité et d'impact, et éviter qu'un changement laisse des tests ou des exigences non revus. Dans les systèmes critiques comme les pompes à perfusion médicales, une trace oubliée peut blesser un patient et bloquer la certification.
- **Hypothèse :** Si un ingénieur interroge le fil numérique via un copilote LLM fondé sur un graphe de connaissances et des outils déterministes, alors il répond aux questions de traçabilité et d'impact au moins 50 % plus vite et avec un rappel (recall) des artefacts d'au moins 90 % (par rapport à la recherche manuelle dans les artefacts et à un LLM sans accès au graphe).

## Résumé

Dans les projets d'ingénierie des systèmes, les questions de traçabilité et d'impact se traitent en naviguant à la main entre des exigences, des modèles et des tests stockés en silos. Ce projet propose `digital-thread-copilot`, un copilote d'IA générative qui intègre ces artefacts dans un graphe de connaissances RDF aligné sur des standards (SysML v2, ReqIF, OSLC) et les interroge via des outils déterministes (SPARQL, parcours du graphe, exécution de tests). Il peut aussi générer de nouveaux artefacts, comme des cas de test ou des extraits SysML v2, validés avant d'être ajoutés au dépôt. Chaque réponse cite les identifiants des artefacts sur lesquels elle s'appuie. La proposition sera évaluée sur le fil numérique de la pompe à perfusion Generic Patient Controlled Analgesia (GPCA), référence publique de la recherche sur les dispositifs médicaux, avec un jeu de 30 questions de référence, et en option sur le Simple Vehicle Model de SysML v2 pour vérifier la portabilité. On mesurera le temps de réponse, la précision, le rappel et le taux d'hallucination, par rapport à la recherche manuelle et à un LLM sans accès au graphe.

## Introduction

Dans le cadre de l'ingénierie numérique et du MBSE **(DOMAINE)**, le cycle de vie d'un système produit des exigences, des modèles logiques et des cas de test qui doivent rester reliés dans un fil numérique. En pratique, répondre à des questions comme « quels tests vérifient cette exigence ? » ou « qu'est-ce qui est impacté si je change ce composant ? » oblige à parcourir à la main plusieurs outils et documents, ce qui est lent et source d'oublis **(SYMPTÔME)**. La racine du problème est que les artefacts sont stockés en silos, dans des formats hétérogènes, et que leurs relations ne sont ni explicites ni interrogeables de façon unifiée, alors que les assistants d'IA génériques n'ont pas ce contexte **(CAUSE)**.

Ce travail vise à développer un copilote qui interroge le fil numérique, représenté comme graphe de connaissances, et agit dessus **(OBJECTIF)**. Nous posons qu'avec ce copilote, un ingénieur répondra au moins 50 % plus vite et avec un rappel des artefacts d'au moins 90 %, par rapport à la recherche manuelle et à un LLM sans le graphe **(HYPOTHÈSE)**. Résoudre ce problème est important car l'analyse d'impact conditionne la vérification, la validation et la certification du système, en particulier pour des dispositifs critiques comme les pompes à perfusion, dont le logiciel est encadré par des normes comme IEC 62304 **(IMPORTANCE DE RÉSOUDRE LE PROBLÈME)**. S'il n'est pas résolu, des changements à l'impact non détecté entraînent des reprises, des tests non relancés, des non-conformités et, dans le pire des cas, des dangers pour le patient **(CONSÉQUENCES DE NE PAS RÉSOUDRE LE PROBLÈME)**. Le résoudre apporte des réponses plus rapides, plus complètes et traçables jusqu'à leurs sources **(BÉNÉFICES DE RÉSOUDRE LE PROBLÈME)**.

Il existe des outils de gestion du cycle de vie basés sur OSLC, des plateformes commerciales de fil numérique et des travaux récents combinant LLM et graphes de connaissances, mais soit ils n'offrent pas d'interface conversationnelle, soit ils ne fondent pas leurs réponses sur des relations explicites entre artefacts (voir l'état de l'art préliminaire) **(TRAVAUX EXISTANTS)**. Notre proposition intègre les exigences, le modèle SysML v2 et les tests dans un graphe RDF, et expose au LLM un ensemble d'outils déterministes en l'obligeant à citer les artefacts utilisés **(SOLUTION PROPOSÉE)**. L'hypothèse sera testée avec 30 questions de référence sur le fil numérique de la pompe à perfusion GPCA, en mesurant le temps, la précision, le rappel et le taux d'hallucination **(PARAMÈTRES POUR CORROBORER L'HYPOTHÈSE)**.

## Objectifs

**Objectif général :** Développer un copilote d'ingénierie fondé sur l'IA générative qui interroge un fil numérique représenté comme graphe de connaissances et agit dessus, pour que les questions de traçabilité et d'impact reçoivent des réponses rapides, exhaustives et fondées sur les artefacts du projet.

| ID | Objectif spécifique | Résultat dans le dépôt | Critère d'acceptation | Trace vers |
| --- | --- | --- | --- | --- |
| OE1 | Analyser l'état de l'art sur le fil numérique, les graphes de connaissances et les LLM appliqués au MBSE | `docs/01-state-of-the-art.md` | Au moins 6 travaux avec DOI ou URL vérifiés (3 articles et 1 outil), 2 bases consultées, 3 travaux lus en entier et un tableau comparatif | Cause, Travaux existants |
| OE2 | Concevoir l'architecture du système et l'ontologie du fil numérique | `docs/02-architecture.md`, ADR, `ontology/*.ttl`, `shapes/*.ttl` | L'ontologie couvre exigence, élément de modèle et test, avec les relations satisfait, vérifie et dépend de ; les formes SHACL valident le cas d'étude sans erreur | Cause, Solution proposée |
| OE3 | Implémenter l'import des artefacts dans le graphe de connaissances | `src/ingest/`, `data/gpca/` | Import de 3 types d'artefacts (exigences ReqIF/JSON, modèle SysML v2, cas de test) ; 100 % des artefacts du cas d'étude chargés ; tests unitaires en CI | Cause |
| OE4 | Implémenter le copilote connecté au dépôt d'ingénierie, avec des outils déterministes, la génération d'artefacts et des garde-fous | `src/copilot/`, interface web | Le copilote lit les artefacts versionnés dans le dépôt ; au moins 5 outils (recherche, trace, impact, exécution des tests, génération d'artefacts) ; les artefacts générés (cas de test, extraits SysML v2, rapports de traçabilité) sont validés avant d'être proposés ; chaque réponse cite des identifiants existants ; les actions d'écriture demandent une confirmation et sont journalisées ; démonstration de traçabilité de bout en bout (exigence, élément de modèle, test, résultat) ; tests fonctionnels en CI | Hypothèse, Solution proposée |
| OE5 | Évaluer l'hypothèse avec un jeu de questions de référence | `eval/`, `docs/05-evaluation.md` | 30 questions avec réponses de référence ; métriques calculées automatiquement en CI ; décision documentée d'accepter ou de rejeter l'hypothèse ; en option : contrôle de portabilité sur le cas d'étude secondaire | Hypothèse, Paramètres |

## État de l'art préliminaire

- **Chaîne de recherche :** `("digital thread" OR "authoritative source of truth") AND ("knowledge graph" OR ontology) AND ("large language model" OR LLM OR "generative AI") AND (MBSE OR SysML OR traceability)`
- **Date de consultation :** _à compléter_
- **Bases consultées :** _à compléter (par exemple IEEE Xplore et Scopus, via la bibliothèque de l'UC3M)_

| Travail | Approche | Standards | Limite par rapport à notre problème | Référence (DOI ou URL) |
| --- | --- | --- | --- | --- |
| _à compléter_ | | | | |

> Règle du groupe : aucune référence n'est ajoutée sans vérification de son DOI ou de son URL.

## Proposition

1. **Fil numérique :** exigences de sécurité, architecture logique et artefacts de vérification de la pompe à perfusion GPCA. Les exigences sont codées en ReqIF/JSON, une partie de l'architecture publiée (AADL, Simulink/Stateflow) est traduite en modèle logique SysML v2, et les cas de test sont dérivés du matériel de vérification publié. Le tout est chargé dans un graphe RDF avec une ontologie légère alignée sur OSLC et SysML v2.
2. **Connexion au dépôt d'ingénierie :** les artefacts sont versionnés dans le dépôt Git et réimportés dans le graphe à chaque changement, pour que le copilote travaille toujours sur l'état actuel du projet.
3. **Outils déterministes :** recherche d'exigences, requêtes de traces (SPARQL), analyse d'impact par parcours du graphe et exécution des tests.
4. **Génération d'artefacts :** à la demande, le copilote rédige de nouveaux artefacts (un cas de test pour une exigence non couverte, un extrait SysML v2, un rapport de traçabilité). Chaque brouillon est validé (SHACL, analyseur SysML v2) et n'est ajouté au dépôt qu'après confirmation de l'ingénieur.
5. **Agent :** LLM orchestré avec le GitHub Copilot SDK, qui choisit et appelle les outils et cite toujours les artefacts utilisés.
6. **Garde-fous :** réponses rejetées si elles ne sont pas fondées sur le graphe, séparation des outils de lecture et d'écriture, confirmation des actions et journalisation.
7. **Interface :** chat web avec une vue du sous-graphe interrogé et de la trace de bout en bout (exigence, élément de modèle, test, résultat).

## Validation de la proposition

- **Cas d'étude :** fil numérique de la pompe à perfusion GPCA, construit à partir des artefacts publics du projet Generic Infusion Pump (FDA, Université de Pennsylvanie, Université du Minnesota) : un sous-ensemble d'environ 20 exigences de sécurité, les éléments du modèle SysML v2 correspondants et les cas de test qui les vérifient. Les documents originaux sont référencés par lien, pas copiés, car aucune licence n'est indiquée.
- **Cas d'étude secondaire (optionnel, si le temps le permet) :** le *Simple Vehicle Model* de l'annexe A de la spécification SysML v2 (dépôt officiel de l'OMG, licence EPL 2.0). Il sert uniquement à vérifier que le copilote fonctionne sur un second système, non médical, sans modification du code, avec un jeu réduit de 10 questions.
- **Jeu de données :** 30 questions de traçabilité, d'impact et de couverture avec leurs réponses de référence.
- **Métriques :** temps par question (s), précision et rappel des artefacts cités, taux d'hallucination (artefacts inexistants ou relations fausses). Métrique secondaire, seulement mesurée (sans seuil, l'hypothèse n'en dépend pas) : taux de validité des artefacts générés (part qui passe SHACL et l'analyseur SysML v2 du premier coup).
- **Seuils :** temps réduit d'au moins 50 % par rapport au processus manuel ; rappel et précision d'au moins 0,90 ; taux d'hallucination d'au plus 5 %.
- **Procédure :** au moins 3 participants extérieurs au groupe répondent à la moitié des questions à la main et à l'autre moitié avec le copilote (ordre croisé). Les 30 questions sont aussi posées à un LLM sans accès au graphe, comme seconde référence.

## Standards utilisés

| Standard | Usage dans le projet |
| --- | --- |
| SysML v2 | Modèle logique du système (notation textuelle) |
| ReqIF | Échange d'exigences |
| OWL / RDF | Ontologie du domaine et graphe de connaissances |
| SPARQL | Requêtes de traçabilité et d'impact |
| SHACL | Validation de l'intégrité du graphe |
| OSLC (RM, QM) | Vocabulaire des liens de traçabilité entre exigences et tests |
| OpenAPI / JSON | Définition des outils de l'agent |
| AADL | Architecture d'origine du cas d'étude GPCA, traduite en partie en SysML v2 |
| IEC 62304, ISO 14971 | Contexte uniquement : cycle de vie du logiciel des dispositifs médicaux et gestion des risques, qui motivent la traçabilité dans le cas d'étude |

## Déclaration d'usage de l'IA

- _Outil :_ Claude (Anthropic). _Usage :_ proposition de structure, brouillon de rédaction et traduction du planteamiento, revus et validés par le groupe.
- _À compléter à chaque usage ultérieur (synonymes de recherche, résumés, mise en page du site, etc.)._

L'hypothèse et les objectifs sont des décisions du groupe.

## Références

Sources du cas d'étude (URL vérifiées le 22/10/2026) :

- University of Pennsylvania, *The Generic Infusion Pump (GIP) project*. https://rtg.cis.upenn.edu/gip-UPenn/
- University of Minnesota, *GPCA artifacts: system requirements, AADL and Simulink/Stateflow models, verification suite* (2015). https://crisys.cs.umn.edu/gpca.shtml
- *Generic Infusion Pump Hazard Analysis and Safety Requirements, Version 1.0*, Technical Report MS-CIS-08-31, University of Pennsylvania, 2009. https://repository.upenn.edu/cis_reports/893
- Object Management Group, *SysML v2 release repository* (modèles d'exemple, dont le Simple Vehicle Model de l'annexe A ; EPL 2.0). https://github.com/systems-modeling/sysml-v2-release

_Références de l'état de l'art : à compléter, uniquement avec un DOI ou une URL vérifiés._
