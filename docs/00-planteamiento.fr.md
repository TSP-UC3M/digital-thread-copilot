# digital-thread-copilot

!!! note "Traduction"
    Cette page est une traduction. La version de référence est la version anglaise.

!!! note "Statut : objectifs validés"
    Le professeur a validé les objectifs OE1 à OE5 en cours le 19 novembre 2026 et a demandé des choix concrets. L'architecture, ses patrons de conception, l'ontologie et le format de chaque artefact sont désormais nommés sur cette page et dans la page d'architecture (`docs/02-architecture.md`, ADR-0017, en anglais). L'hypothèse, l'objectif OE4 et les chiffres de l'évaluation ont été révisés en novembre 2026 (décisions de périmètre consignées dans l'[ADR-0001](adr/0001-project-framing.md)).

**Titres candidats :** 1) `digital-thread-copilot` 2) `trace-copilot` 3) `kg-engineering-copilot`
**Retenu :** `digital-thread-copilot`

- **Domaine :** Ingénierie numérique et ingénierie des systèmes basée sur les modèles (MBSE).
- **Sujet :** Copilote conversationnel qui interroge le fil numérique (digital thread) d'un système et agit dessus (exigences, modèle SysML v2 et tests), représenté sous forme de graphe de connaissances.
- **Symptôme :** Répondre aux questions de traçabilité et d'impact (« quels tests vérifient cette exigence de sécurité ? », « qu'est-ce qui est impacté si je change la dose maximale de bolus ? ») oblige à naviguer à la main entre plusieurs outils et documents. C'est lent et des artefacts impactés sont oubliés.
- **Cause :** Les artefacts sont stockés en silos, dans des formats hétérogènes, et leurs relations ne sont ni explicites ni interrogeables de façon unifiée. Les assistants d'IA génériques n'ont pas accès à ce contexte et inventent donc des réponses.
- **Intérêt :** Réduire le temps consacré à l'analyse de traçabilité et d'impact, et éviter qu'un changement laisse des tests ou des exigences non revus. Dans les systèmes critiques comme les pompes à perfusion médicales, une trace oubliée peut blesser un patient et bloquer la certification.
- **Hypothèse :** Si les questions de traçabilité, d'impact et de couverture sur un fil numérique sont traitées par un copilote LLM limité à des outils déterministes sur un graphe de connaissances des artefacts, alors ses réponses citent les bons artefacts avec un rappel (recall) et une précision d'au moins 0,90 et un taux d'hallucination d'au plus 5 %, et avec un rappel significativement plus élevé que celui du même LLM recevant tous les artefacts sous forme de texte dans son contexte, sans graphe ni outils (test apparié sur les mêmes questions, p < 0,05). Observation secondaire, indicative : avec le copilote, les ingénieurs répondent au moins 50 % plus vite que par la recherche manuelle (3 participants, 10 questions chacun).

## Résumé

Dans les projets d'ingénierie des systèmes, les questions de traçabilité et d'impact se traitent en naviguant à la main entre des exigences, des modèles et des tests stockés en silos. Ce projet propose `digital-thread-copilot`, un copilote d'IA générative qui intègre ces artefacts dans un graphe de connaissances RDF aligné sur des standards (SysML v2, ReqIF, OSLC) et les interroge via des outils déterministes (SPARQL, parcours du graphe, exécution de tests). Il peut aussi rédiger un cas de test pour une exigence qu'aucun test ne vérifie ; ce brouillon est validé avant d'être ajouté au dépôt. Chaque réponse cite les identifiants des artefacts sur lesquels elle s'appuie. La proposition sera évaluée sur le fil numérique de la pompe à perfusion Generic Patient Controlled Analgesia (GPCA), référence publique de la recherche sur les dispositifs médicaux, avec un jeu de 20 questions de référence. On mesurera la précision, le rappel et le taux d'hallucination par rapport au même LLM sans graphe ni outils et, à titre indicatif, le temps de réponse par rapport à la recherche manuelle.

## Introduction

Dans le cadre de l'ingénierie numérique et du MBSE **(DOMAINE)**, le cycle de vie d'un système produit des exigences, des modèles logiques et des cas de test qui doivent rester reliés dans un fil numérique. En pratique, répondre à des questions comme « quels tests vérifient cette exigence ? » ou « qu'est-ce qui est impacté si je change ce composant ? » oblige à parcourir à la main plusieurs outils et documents, ce qui est lent et source d'oublis **(SYMPTÔME)**. La racine du problème est que les artefacts sont stockés en silos, dans des formats hétérogènes, et que leurs relations ne sont ni explicites ni interrogeables de façon unifiée, alors que les assistants d'IA génériques n'ont pas ce contexte **(CAUSE)**.

Ce travail vise à développer un copilote qui interroge le fil numérique, représenté comme graphe de connaissances, et agit dessus **(OBJECTIF)**. Nous posons que les réponses de ce copilote citent les bons artefacts avec un rappel et une précision d'au moins 0,90 et un taux d'hallucination d'au plus 5 %, et avec un rappel significativement plus élevé que celui du même LLM recevant tous les artefacts sous forme de texte, sans graphe ni outils **(HYPOTHÈSE)**. Résoudre ce problème est important car l'analyse d'impact conditionne la vérification, la validation et la certification du système, en particulier pour des dispositifs critiques comme les pompes à perfusion, dont le logiciel est encadré par des normes comme IEC 62304 **(IMPORTANCE DE RÉSOUDRE LE PROBLÈME)**. S'il n'est pas résolu, des changements à l'impact non détecté entraînent des reprises, des tests non relancés, des non-conformités et, dans le pire des cas, des dangers pour le patient **(CONSÉQUENCES DE NE PAS RÉSOUDRE LE PROBLÈME)**. Le résoudre apporte des réponses plus rapides, plus complètes et traçables jusqu'à leurs sources **(BÉNÉFICES DE RÉSOUDRE LE PROBLÈME)**.

Il existe des outils de gestion du cycle de vie basés sur OSLC, des plateformes commerciales de fil numérique et des travaux récents combinant LLM et graphes de connaissances, mais soit ils n'offrent pas d'interface conversationnelle, soit ils ne fondent pas leurs réponses sur des relations explicites entre artefacts (voir l'état de l'art préliminaire) **(TRAVAUX EXISTANTS)**. Notre proposition intègre les exigences, le modèle SysML v2 et les tests dans un graphe RDF, et expose au LLM un ensemble d'outils déterministes en l'obligeant à citer les artefacts utilisés **(SOLUTION PROPOSÉE)**. L'hypothèse sera testée avec 20 questions de référence sur le fil numérique de la pompe à perfusion GPCA, en mesurant la précision, le rappel et le taux d'hallucination, et le temps à titre indicatif **(PARAMÈTRES POUR CORROBORER L'HYPOTHÈSE)**.

## Objectifs

**Objectif général :** Développer un copilote d'ingénierie fondé sur l'IA générative qui interroge un fil numérique représenté comme graphe de connaissances et agit dessus, pour que les questions de traçabilité et d'impact reçoivent des réponses rapides, exhaustives et fondées sur les artefacts du projet.

| ID | Objectif spécifique | Résultat dans le dépôt | Critère d'acceptation | Trace vers |
| --- | --- | --- | --- | --- |
| OE1 | Analyser l'état de l'art sur le fil numérique, les graphes de connaissances et les LLM appliqués au MBSE | `docs/01-state-of-the-art.md` | 8 travaux avec DOI ou URL vérifiés (au moins 3 articles et 1 outil), sélectionnés par une recherche systématique dans IEEE Xplore et Scopus complétée par d'autres méthodes documentées ; 3 travaux lus en entier et un tableau comparatif | Cause, Travaux existants |
| OE2 | Concevoir l'architecture du système et l'ontologie du fil numérique | `docs/02-architecture.md`, ADR, `ontology/digital-thread.ttl`, `shapes/digital-thread-shapes.ttl` | Architecture hexagonale (ports et adaptateurs) décrite par les vues de l'ISO/IEC/IEEE 42010 aux niveaux C4, chaque patron de conception relié à son paquet (ADR-0017) ; ontologie en OWL 2 (Turtle), alignée sur OSLC RM et QM 2.1, couvrant exigence, élément de modèle, cas de test, résultat de test et méthode de vérification, avec les relations satisfait, vérifie, dépend de et rend compte de ; les formes SHACL valident le cas d'étude sans erreur et détectent chaque exemple défectueux | Cause, Solution proposée |
| OE3 | Implémenter l'import des artefacts dans le graphe de connaissances | `src/digital_thread_copilot/ingest/`, `data/gpca/` | Chaîne d'import (lecture, conversion en RDF, validation SHACL, chargement) pour 3 types d'artefacts : exigences en YAML validé par JSON Schema, avec un export ReqIF 1.2 ; modèle SysML v2 en notation textuelle ; cas de test en YAML et leurs résultats en JUnit XML ; 100 % des artefacts du cas d'étude chargés ; tests unitaires en CI | Cause |
| OE4 | Implémenter le copilote connecté au dépôt d'ingénierie, avec des outils déterministes, la génération de cas de test et des garde-fous | `src/digital_thread_copilot/copilot/`, `src/digital_thread_copilot/ui/` (chat web Chainlit) | Le copilote lit les artefacts versionnés dans le dépôt ; au moins 5 outils (recherche, trace, impact, exécution des tests, lacunes de couverture) ; un brouillon de cas de test généré pour une exigence non couverte est validé avant d'être proposé ; chaque réponse cite des identifiants existants ; les actions d'écriture demandent une confirmation et sont journalisées ; chat web ; démonstration de traçabilité de bout en bout (exigence, élément de modèle, test, résultat) ; tests fonctionnels en CI. Extensions, réalisées seulement si le temps le permet : extraits SysML v2 et rapports de traçabilité générés ; vue du sous-graphe interrogé et de la trace ; réimport à chaque changement d'un artefact | Hypothèse, Solution proposée |
| OE5 | Évaluer l'hypothèse avec un jeu de questions de référence | `eval/`, `docs/05-evaluation.md` | 20 questions avec réponses de référence ; métriques calculées automatiquement en CI ; décision documentée d'accepter ou de rejeter l'hypothèse | Hypothèse, Paramètres |

## État de l'art préliminaire

- **Chaîne de recherche :** `("digital thread" OR "authoritative source of truth") AND ("knowledge graph" OR ontology) AND ("large language model" OR LLM OR "generative AI") AND (MBSE OR SysML OR traceability)`
- **Date de consultation :** _à compléter_
- **Bases consultées :** _à compléter (par exemple IEEE Xplore et Scopus, via la bibliothèque de l'UC3M)_

| Travail | Approche | Standards | Limite par rapport à notre problème | Référence (DOI ou URL) |
| --- | --- | --- | --- | --- |
| _à compléter_ | | | | |

> Règle du groupe : aucune référence n'est ajoutée sans vérification de son DOI ou de son URL.

## Proposition

1. **Fil numérique :** exigences de sécurité, architecture logique et artefacts de vérification de la pompe à perfusion GPCA. Les exigences sont écrites en YAML, validées par JSON Schema et exportées en ReqIF 1.2, une partie de l'architecture publiée (AADL, Simulink/Stateflow) est traduite en modèle logique SysML v2, et les cas de test sont dérivés du matériel de vérification publié. Le tout est chargé dans un graphe RDF avec une ontologie légère en OWL 2 (Turtle, `ontology/digital-thread.ttl`) alignée sur OSLC et SysML v2, contrôlée par des formes SHACL.
2. **Connexion au dépôt d'ingénierie :** les artefacts sont versionnés dans le dépôt Git et chargés dans le graphe au démarrage du système. Extension : réimport à chaque changement, pour que le copilote travaille toujours sur l'état actuel du projet.
3. **Outils déterministes :** recherche d'exigences, requêtes de traces (SPARQL), analyse d'impact par parcours du graphe et exécution des tests.
4. **Génération d'artefacts :** à la demande, le copilote rédige un cas de test pour une exigence qu'aucun test ne vérifie. Le brouillon est validé par rapport à son schéma et n'est ajouté au dépôt qu'après confirmation de l'ingénieur. Extension : extraits SysML v2, validés avec l'analyseur SysML v2, et rapports de traçabilité.
5. **Agent :** LLM orchestré avec le GitHub Copilot SDK selon le patron ReAct (raisonner, appeler un outil, lire son résultat, répondre) : il choisit et appelle les outils et cite toujours les artefacts utilisés.
6. **Garde-fous :** réponses rejetées si elles ne sont pas fondées sur le graphe, séparation des outils de lecture et d'écriture, confirmation des actions et journalisation.
7. **Interface :** chat web construit avec Chainlit, couche fine sans logique. Extension : une vue du sous-graphe interrogé et de la trace de bout en bout (exigence, élément de modèle, test, résultat).
8. **Architecture :** hexagonale (ports et adaptateurs) : le graphe et les outils forment le cœur ; l'import (Pipes and Filters, un adaptateur par format), l'export ReqIF, le fournisseur de modèle (Strategy : modèle réel ou rejeu) et l'interface sont des adaptateurs. Le garde-fou est une chaîne de validateurs (Chain of Responsibility) et chaque écriture est une commande confirmée et journalisée (Command). Détail : `docs/02-architecture.md` et ADR-0017.

## Validation de la proposition

- **Cas d'étude :** fil numérique de la pompe à perfusion GPCA, construit à partir des artefacts publics du projet Generic Infusion Pump (FDA, Université de Pennsylvanie, Université du Minnesota) : un sous-ensemble de 12 exigences de sécurité, les éléments du modèle SysML v2 correspondants et les 12 cas de test qui les vérifient. Les documents originaux sont référencés par lien, pas copiés, car aucune licence n'est indiquée.
- **Jeu de données :** 20 questions de traçabilité, d'impact et de couverture avec leurs réponses de référence.
- **Métriques :** précision et rappel des artefacts cités, taux d'hallucination (artefacts inexistants ou relations fausses), temps par question (s). Métrique secondaire, seulement mesurée (sans seuil, l'hypothèse n'en dépend pas) : taux de validité des cas de test générés (part qui passe la validation du premier coup).
- **Seuils :** rappel et précision d'au moins 0,90 ; taux d'hallucination d'au plus 5 % ; rappel significativement plus élevé que celui de la configuration de référence (ii) ci-dessous (test apparié sur les mêmes questions, p < 0,05). À titre indicatif seulement, hors critère d'acceptation : temps réduit d'au moins 50 % par rapport au processus manuel.
- **Procédure :** les 20 questions sont exécutées 3 fois sur trois configurations qui utilisent le même modèle, la même version et les mêmes paramètres : le copilote ; (i) le LLM avec la question seule, rapporté comme borne inférieure ; (ii) le LLM avec le texte de tous les artefacts dans son contexte, sans graphe ni outils. Le critère compare le copilote à (ii). Séparément, 3 participants extérieurs au groupe répondent chacun à 10 questions, la moitié à la main et l'autre moitié avec le copilote (ordre croisé). Menace à la validité : le cas d'étude est petit, tous les artefacts tiennent donc dans le contexte de (ii) et l'écart peut être faible.

## Standards utilisés

| Standard | Usage dans le projet |
| --- | --- |
| SysML v2 | Modèle logique du système (notation textuelle) |
| ReqIF 1.2 (OMG) | Export des exigences, écrites en YAML et validées par JSON Schema |
| OWL 2 / RDF (Turtle) | Ontologie `ontology/digital-thread.ttl` et graphe de connaissances |
| SPARQL | Requêtes de traçabilité et d'impact |
| SHACL | Validation de l'intégrité du graphe (`shapes/digital-thread-shapes.ttl`) |
| JUnit XML | Résultats de test chargés dans le graphe |
| ISO/IEC/IEEE 42010 | Description de l'architecture par vues (`docs/02-architecture.md`) |
| OSLC (RM, QM) | Vocabulaire des liens de traçabilité entre exigences et tests |
| JSON Schema | Validation des fichiers d'exigences et de cas de test ; définition des outils de l'agent |
| AADL | Architecture d'origine du cas d'étude GPCA, traduite en partie en SysML v2 |
| IEC 62304, ISO 14971 | Contexte uniquement : cycle de vie du logiciel des dispositifs médicaux et gestion des risques, qui motivent la traçabilité dans le cas d'étude |

## Déclaration d'usage de l'IA

- _Outil :_ Claude (Anthropic). _Usage :_ proposition de structure, brouillon de rédaction et traduction du planteamiento, revus et validés par le groupe.
- _Outil :_ Claude (Anthropic). _Dates :_ 15 et 16 novembre 2026. _Usage (cadrage du projet) :_ diagnostic de l'échec du workflow de documentation et rédaction de son correctif ; estimations d'effort et scénarios de périmètre ; tableaux d'options avec une recommandation pour chaque décision de cadrage ; proposition de scinder l'hypothèse en un critère principal et un critère secondaire, et proposition de définition du critère principal (seuils, configurations de référence, test apparié) ; listes de vérification des références ; relecture indépendante du cadrage par un second agent d'IA. _Revue par le groupe :_ chaque décision a été prise par un membre du groupe à partir des options présentées, et le cadrage est soumis à l'approbation des trois membres dans l'ADR-0001 (`docs/adr/0001-project-framing.md`). La demande de validation envoyée au professeur le 15 novembre 2026 a été rédigée par le groupe.
- Les usages ultérieurs sont listés sur la page [Usage de l'IA](ai-usage.md) (en anglais).

L'hypothèse et les objectifs sont des décisions du groupe.

## Références

Sources du cas d'étude (URL vérifiées le 22/10/2026) :

- University of Pennsylvania, *The Generic Infusion Pump (GIP) project*. https://rtg.cis.upenn.edu/gip-UPenn/
- University of Minnesota, *GPCA artifacts: system requirements, AADL and Simulink/Stateflow models, verification suite* (2015). https://crisys.cs.umn.edu/gpca.shtml
- *Generic Infusion Pump Hazard Analysis and Safety Requirements, Version 1.0*, Technical Report MS-CIS-08-31, University of Pennsylvania, 2009. https://repository.upenn.edu/cis_reports/893
- Object Management Group, *SysML v2 release repository* (modèles d'exemple, dont le Simple Vehicle Model de l'annexe A ; EPL 2.0). https://github.com/systems-modeling/sysml-v2-release

_Références de l'état de l'art : à compléter, uniquement avec un DOI ou une URL vérifiés._
