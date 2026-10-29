# digital-thread-copilot

!!! note "Traducción"
    Esta página es una traducción. La versión de referencia es la versión en inglés.

**Títulos candidatos:** 1) `digital-thread-copilot` 2) `trace-copilot` 3) `kg-engineering-copilot`
**Elegido:** `digital-thread-copilot`

- **Área:** Ingeniería digital e ingeniería de sistemas basada en modelos (MBSE).
- **Tema:** Copiloto conversacional que consulta y actúa sobre el hilo digital de un sistema (requisitos, modelo SysML v2 y pruebas) representado como grafo de conocimiento.
- **Síntoma:** Responder a preguntas de trazabilidad e impacto ("¿qué pruebas verifican este requisito de seguridad?", "¿qué se ve afectado si cambio la dosis máxima de bolo?") obliga a navegar a mano entre varias herramientas y documentos. Es lento y se omiten artefactos afectados.
- **Causa:** Los artefactos viven en silos con formatos heterogéneos y sus relaciones no son explícitas ni consultables de forma unificada. Los asistentes de IA genéricos no tienen acceso a ese contexto, por lo que inventan respuestas.
- **Interés:** Reducir el tiempo dedicado al análisis de trazabilidad e impacto y evitar que un cambio deje pruebas o requisitos sin revisar. En sistemas críticos como las bombas de infusión médicas, una traza omitida puede dañar a un paciente y bloquear la certificación.
- **Hipótesis:** Si un ingeniero consulta el hilo digital mediante un copiloto LLM fundamentado en un grafo de conocimiento y en herramientas deterministas, entonces responde a preguntas de trazabilidad e impacto al menos un 50 % más rápido y con una exhaustividad (recall) de artefactos de al menos el 90 % (respecto a la búsqueda manual en los artefactos y a un LLM sin acceso al grafo).

## Resumen

En los proyectos de ingeniería de sistemas, las preguntas de trazabilidad e impacto se responden navegando a mano entre requisitos, modelos y pruebas almacenados en silos. Este proyecto propone `digital-thread-copilot`, un copiloto de IA generativa que integra estos artefactos en un grafo de conocimiento RDF alineado con estándares (SysML v2, ReqIF, OSLC) y los consulta mediante herramientas deterministas (SPARQL, recorrido del grafo, ejecución de pruebas). También puede generar nuevos artefactos, como casos de prueba o fragmentos SysML v2, que se validan antes de añadirse al repositorio. Cada respuesta cita los identificadores de los artefactos en los que se basa. La propuesta se evaluará sobre el hilo digital de la bomba de infusión Generic Patient Controlled Analgesia (GPCA), una referencia pública de investigación en dispositivos médicos, con un conjunto de 30 preguntas de referencia, y opcionalmente sobre el Simple Vehicle Model de SysML v2 para comprobar la portabilidad, midiendo tiempo de respuesta, precisión, exhaustividad y tasa de alucinación frente a la búsqueda manual y a un LLM sin acceso al grafo.

## Introducción

En el marco de la ingeniería digital y la MBSE **(ÁREA)**, el ciclo de vida de un sistema produce requisitos, modelos lógicos y casos de prueba que deben permanecer conectados en un hilo digital. En la práctica, responder a preguntas como "¿qué pruebas verifican este requisito?" o "¿qué se ve afectado si cambio este componente?" exige recorrer a mano varias herramientas y documentos, lo que es lento y propenso a omisiones **(SÍNTOMA)**. El origen del problema es que los artefactos se almacenan en silos con formatos heterogéneos y sus relaciones no son explícitas ni consultables de forma unificada, mientras que los asistentes de IA genéricos carecen de ese contexto **(CAUSA)**.

Este trabajo busca desarrollar un copiloto que consulte y actúe sobre el hilo digital representado como grafo de conocimiento **(OBJETIVO)**. Se plantea que, usando este copiloto, un ingeniero responderá al menos un 50 % más rápido y con una exhaustividad de artefactos de al menos el 90 % respecto a la búsqueda manual y a un LLM sin el grafo **(HIPÓTESIS)**. Resolver este problema es importante porque el análisis de impacto condiciona la verificación, la validación y la certificación del sistema, especialmente en dispositivos críticos como las bombas de infusión, cuyo software está regulado por normas como IEC 62304 **(IMPORTANCIA DE RESOLVER EL PROBLEMA)**. Si no se resuelve, los cambios con impacto no detectado provocan retrabajo, pruebas que no se vuelven a ejecutar, no conformidades y, en el peor caso, peligros para el paciente **(CONSECUENCIAS DE NO RESOLVER EL PROBLEMA)**. Resolverlo aporta respuestas más rápidas, más completas y trazables hasta sus fuentes **(BENEFICIOS DE RESOLVER EL PROBLEMA)**.

Existen herramientas de gestión del ciclo de vida basadas en OSLC, plataformas comerciales de hilo digital y trabajos recientes que combinan LLM y grafos de conocimiento, pero o no ofrecen una interfaz conversacional, o no fundamentan sus respuestas en relaciones explícitas entre artefactos (ver Estado de la cuestión preliminar) **(TRABAJOS EXISTENTES)**. Nuestra propuesta integra requisitos, modelo SysML v2 y pruebas en un grafo RDF y expone al LLM un conjunto de herramientas deterministas, obligándole a citar los artefactos que utiliza **(SOLUCIÓN PROPUESTA)**. La hipótesis se corroborará con 30 preguntas de referencia sobre el hilo digital de la bomba de infusión GPCA, midiendo tiempo, precisión, exhaustividad y tasa de alucinación **(PARÁMETROS PARA CORROBORAR LA HIPÓTESIS)**.

## Objetivos

**Objetivo general:** Desarrollar un copiloto de ingeniería basado en IA generativa que consulte y actúe sobre un hilo digital representado como grafo de conocimiento, para que las preguntas de trazabilidad e impacto se respondan de forma rápida, exhaustiva y fundamentada en los artefactos del proyecto.

| ID | Objetivo específico | Resultado en el repositorio | Criterio de aceptación | Traza a |
| --- | --- | --- | --- | --- |
| OE1 | Analizar el estado de la cuestión sobre hilo digital, grafos de conocimiento y LLM aplicados a MBSE | `docs/01-state-of-the-art.md` | Al menos 6 trabajos con DOI o URL verificados (3 artículos y 1 herramienta), 2 bases consultadas, 3 trabajos leídos completos y tabla comparativa | Causa, Trabajos existentes |
| OE2 | Diseñar la arquitectura del sistema y la ontología del hilo digital | `docs/02-architecture.md`, ADRs, `ontology/*.ttl`, `shapes/*.ttl` | La ontología cubre requisito, elemento de modelo y prueba con las relaciones satisface, verifica y depende de; las formas SHACL validan el caso de estudio sin errores | Causa, Solución propuesta |
| OE3 | Implementar la ingesta de artefactos en el grafo de conocimiento | `src/ingest/`, `data/gpca/` | Ingesta de 3 tipos de artefactos (requisitos ReqIF/JSON, modelo SysML v2, casos de prueba); el 100 % de los artefactos del caso de estudio cargados; pruebas unitarias en CI | Causa |
| OE4 | Implementar el copiloto conectado al repositorio de ingeniería, con herramientas deterministas, generación de artefactos y guardarraíles | `src/copilot/`, interfaz web | El copiloto lee los artefactos versionados en el repositorio; al menos 5 herramientas (búsqueda, traza, impacto, ejecución de pruebas, generación de artefactos); los artefactos generados (casos de prueba, fragmentos SysML v2, informes de trazabilidad) se validan antes de proponerse; toda respuesta cita IDs existentes; las acciones de escritura requieren confirmación y quedan registradas; demostración de trazabilidad de extremo a extremo (requisito, elemento de modelo, prueba, resultado); pruebas funcionales en CI | Hipótesis, Solución propuesta |
| OE5 | Evaluar la hipótesis con un conjunto de preguntas de referencia | `eval/`, `docs/05-evaluation.md` | 30 preguntas con respuesta de referencia; métricas calculadas automáticamente en CI; decisión documentada de aceptar o rechazar la hipótesis; opcional: comprobación de portabilidad en el caso de estudio secundario | Hipótesis, Parámetros |

## Estado de la cuestión preliminar

- **Cadena de búsqueda:** `("digital thread" OR "authoritative source of truth") AND ("knowledge graph" OR ontology) AND ("large language model" OR LLM OR "generative AI") AND (MBSE OR SysML OR traceability)`
- **Fecha de consulta:** _por completar_
- **Bases consultadas:** _por completar (p. ej. IEEE Xplore y Scopus, a través de la biblioteca UC3M)_

| Trabajo | Enfoque | Estándares | Limitación respecto a nuestro problema | Referencia (DOI o URL) |
| --- | --- | --- | --- | --- |
| _por completar_ | | | | |

> Regla del grupo: no se añade ninguna referencia sin comprobar su DOI o URL.

## Propuesta

1. **Hilo digital:** requisitos de seguridad, arquitectura lógica y artefactos de verificación de la bomba de infusión GPCA. Los requisitos se codifican en ReqIF/JSON, parte de la arquitectura publicada (AADL, Simulink/Stateflow) se traduce a un modelo lógico SysML v2 y los casos de prueba se derivan del material de verificación publicado. Todo se carga en un grafo RDF con una ontología ligera alineada con OSLC y SysML v2.
2. **Conexión con el repositorio de ingeniería:** los artefactos se versionan en el repositorio Git y se vuelven a ingerir en el grafo con cada cambio, de modo que el copiloto trabaja siempre sobre el estado actual del proyecto.
3. **Herramientas deterministas:** búsqueda de requisitos, consultas de trazas (SPARQL), análisis de impacto por recorrido del grafo y ejecución de pruebas.
4. **Generación de artefactos:** a petición, el copiloto redacta nuevos artefactos (un caso de prueba para un requisito no cubierto, un fragmento SysML v2, un informe de trazabilidad). Cada borrador se valida (SHACL, analizador SysML v2) y solo se añade al repositorio tras la confirmación del ingeniero.
5. **Agente:** LLM orquestado con GitHub Copilot SDK que elige y llama a las herramientas y cita siempre los artefactos utilizados.
6. **Guardarraíles:** respuestas rechazadas si no están fundamentadas en el grafo, separación de herramientas de lectura y escritura, confirmación de acciones y registro.
7. **Interfaz:** chat web con una vista del subgrafo consultado y de la traza de extremo a extremo (requisito, elemento de modelo, prueba, resultado).

## Validación de la propuesta

- **Caso de estudio:** hilo digital de la bomba de infusión GPCA, construido a partir de los artefactos públicos del proyecto Generic Infusion Pump (FDA, Universidad de Pensilvania, Universidad de Minnesota): un subconjunto de unos 20 requisitos de seguridad, los elementos del modelo SysML v2 correspondientes y los casos de prueba que los verifican. Los documentos originales se enlazan, no se copian, ya que no se indica ninguna licencia.
- **Caso de estudio secundario (opcional, si hay tiempo):** el *Simple Vehicle Model* del anexo A de la especificación SysML v2 (repositorio oficial de OMG, licencia EPL 2.0). Solo se usa para comprobar que el copiloto funciona en un segundo sistema, no médico, sin cambios de código, con un conjunto reducido de 10 preguntas.
- **Conjunto de datos:** 30 preguntas de trazabilidad, impacto y cobertura con su respuesta de referencia.
- **Métricas:** tiempo por pregunta (s), precisión y exhaustividad de los artefactos citados, tasa de alucinación (artefactos inexistentes o relaciones falsas). Métrica secundaria, solo medida (sin umbral, la hipótesis no depende de ella): tasa de validez de los artefactos generados (proporción que supera SHACL y el analizador SysML v2 al primer intento).
- **Umbrales:** tiempo reducido al menos un 50 % frente al proceso manual; exhaustividad y precisión de al menos 0,90; tasa de alucinación de como máximo un 5 %.
- **Procedimiento:** al menos 3 participantes externos al grupo responden la mitad de las preguntas a mano y la otra mitad con el copiloto (orden cruzado). Las 30 preguntas se plantean también a un LLM sin acceso al grafo como segunda referencia.

## Estándares implicados

| Estándar | Uso en el proyecto |
| --- | --- |
| SysML v2 | Modelo lógico del sistema (notación textual) |
| ReqIF | Intercambio de requisitos |
| OWL / RDF | Ontología del dominio y grafo de conocimiento |
| SPARQL | Consultas de trazabilidad e impacto |
| SHACL | Validación de la integridad del grafo |
| OSLC (RM, QM) | Vocabulario de enlaces de trazabilidad entre requisitos y pruebas |
| OpenAPI / JSON | Definición de las herramientas del agente |
| AADL | Arquitectura de origen del caso de estudio GPCA, traducida en parte a SysML v2 |
| IEC 62304, ISO 14971 | Solo contexto: ciclo de vida del software de dispositivos médicos y gestión de riesgos, que motivan la trazabilidad en el caso de estudio |

## Declaración de uso de IA

- _Herramienta:_ Claude (Anthropic). _Uso:_ propuesta de estructura, borrador de redacción y traducción del planteamiento, revisados y validados por el grupo.
- _Por completar con cada uso posterior (sinónimos de búsqueda, resúmenes, maquetación de la página, etc.)._

La hipótesis y los objetivos son decisión del grupo.

## Referencias

Fuentes del caso de estudio (URL comprobadas el 22/10/2026):

- University of Pennsylvania, *The Generic Infusion Pump (GIP) project*. https://rtg.cis.upenn.edu/gip-UPenn/
- University of Minnesota, *GPCA artifacts: system requirements, AADL and Simulink/Stateflow models, verification suite* (2015). https://crisys.cs.umn.edu/gpca.shtml
- *Generic Infusion Pump Hazard Analysis and Safety Requirements, Version 1.0*, Technical Report MS-CIS-08-31, University of Pennsylvania, 2009. https://repository.upenn.edu/cis_reports/893
- Object Management Group, *SysML v2 release repository* (modelos de ejemplo, incluido el Simple Vehicle Model del anexo A; EPL 2.0). https://github.com/systems-modeling/sysml-v2-release

_Referencias del estado de la cuestión: por completar, solo con DOI o URL verificados._
