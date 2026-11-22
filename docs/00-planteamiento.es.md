# digital-thread-copilot

!!! note "Traducción"
    Esta página es una traducción. La versión de referencia es la versión en inglés.

!!! note "Estado: objetivos validados"
    El profesor validó los objetivos OE1 a OE5 en clase el 19 de noviembre de 2026 y pidió elecciones concretas. La arquitectura, sus patrones de diseño, la ontología y el formato de cada artefacto se nombran ahora en esta página y en la página de arquitectura (`docs/02-architecture.md`, ADR-0017, en inglés). La hipótesis, el objetivo OE4 y las cifras de la evaluación se revisaron en noviembre de 2026 (decisiones de alcance recogidas en el [ADR-0001](adr/0001-project-framing.md)).

**Títulos candidatos:** 1) `digital-thread-copilot` 2) `trace-copilot` 3) `kg-engineering-copilot`
**Elegido:** `digital-thread-copilot`

- **Área:** Ingeniería digital e ingeniería de sistemas basada en modelos (MBSE).
- **Tema:** Copiloto conversacional que consulta y actúa sobre el hilo digital de un sistema (requisitos, modelo SysML v2 y pruebas) representado como grafo de conocimiento.
- **Síntoma:** Responder a preguntas de trazabilidad e impacto ("¿qué pruebas verifican este requisito de seguridad?", "¿qué se ve afectado si cambio la dosis máxima de bolo?") obliga a navegar a mano entre varias herramientas y documentos. Es lento y se omiten artefactos afectados.
- **Causa:** Los artefactos viven en silos con formatos heterogéneos y sus relaciones no son explícitas ni consultables de forma unificada. Los asistentes de IA genéricos no tienen acceso a ese contexto, por lo que inventan respuestas.
- **Interés:** Reducir el tiempo dedicado al análisis de trazabilidad e impacto y evitar que un cambio deje pruebas o requisitos sin revisar. En sistemas críticos como las bombas de infusión médicas, una traza omitida puede dañar a un paciente y bloquear la certificación.
- **Hipótesis:** Si las preguntas de trazabilidad, impacto y cobertura sobre un hilo digital se responden con un copiloto LLM limitado a herramientas deterministas sobre un grafo de conocimiento de los artefactos, entonces sus respuestas citan los artefactos correctos con una exhaustividad (recall) y una precisión de al menos 0,90 y una tasa de alucinación de como máximo el 5 %, y con una exhaustividad significativamente mayor que la del mismo LLM con todos los artefactos como texto en su contexto, sin grafo ni herramientas (prueba pareada sobre las mismas preguntas, p < 0,05). Observación secundaria, indicativa: con el copiloto se responde al menos un 50 % más rápido que con la búsqueda manual (3 participantes, 10 preguntas cada uno).

## Resumen

En los proyectos de ingeniería de sistemas, las preguntas de trazabilidad e impacto se responden navegando a mano entre requisitos, modelos y pruebas almacenados en silos. Este proyecto propone `digital-thread-copilot`, un copiloto de IA generativa que integra estos artefactos en un grafo de conocimiento RDF alineado con estándares (SysML v2, ReqIF, OSLC) y los consulta mediante herramientas deterministas (SPARQL, recorrido del grafo, ejecución de pruebas). También puede redactar un caso de prueba para un requisito que ninguna prueba verifica; el borrador se valida antes de añadirse al repositorio. Cada respuesta cita los identificadores de los artefactos en los que se basa. La propuesta se evaluará sobre el hilo digital de la bomba de infusión Generic Patient Controlled Analgesia (GPCA), una referencia pública de investigación en dispositivos médicos, con un conjunto de 20 preguntas de referencia, midiendo precisión, exhaustividad y tasa de alucinación frente al mismo LLM sin grafo ni herramientas y, a título indicativo, el tiempo de respuesta frente a la búsqueda manual.

## Introducción

En el marco de la ingeniería digital y la MBSE **(ÁREA)**, el ciclo de vida de un sistema produce requisitos, modelos lógicos y casos de prueba que deben permanecer conectados en un hilo digital. En la práctica, responder a preguntas como "¿qué pruebas verifican este requisito?" o "¿qué se ve afectado si cambio este componente?" exige recorrer a mano varias herramientas y documentos, lo que es lento y propenso a omisiones **(SÍNTOMA)**. El origen del problema es que los artefactos se almacenan en silos con formatos heterogéneos y sus relaciones no son explícitas ni consultables de forma unificada, mientras que los asistentes de IA genéricos carecen de ese contexto **(CAUSA)**.

Este trabajo busca desarrollar un copiloto que consulte y actúe sobre el hilo digital representado como grafo de conocimiento **(OBJETIVO)**. Se plantea que las respuestas de este copiloto citan los artefactos correctos con una exhaustividad y una precisión de al menos 0,90 y una tasa de alucinación de como máximo el 5 %, y con una exhaustividad significativamente mayor que la del mismo LLM con todos los artefactos como texto, sin grafo ni herramientas **(HIPÓTESIS)**. Resolver este problema es importante porque el análisis de impacto condiciona la verificación, la validación y la certificación del sistema, especialmente en dispositivos críticos como las bombas de infusión, cuyo software está regulado por normas como IEC 62304 **(IMPORTANCIA DE RESOLVER EL PROBLEMA)**. Si no se resuelve, los cambios con impacto no detectado provocan retrabajo, pruebas que no se vuelven a ejecutar, no conformidades y, en el peor caso, peligros para el paciente **(CONSECUENCIAS DE NO RESOLVER EL PROBLEMA)**. Resolverlo aporta respuestas más rápidas, más completas y trazables hasta sus fuentes **(BENEFICIOS DE RESOLVER EL PROBLEMA)**.

Existen herramientas de gestión del ciclo de vida basadas en OSLC, plataformas comerciales de hilo digital y trabajos recientes que combinan LLM y grafos de conocimiento, pero o no ofrecen una interfaz conversacional, o no fundamentan sus respuestas en relaciones explícitas entre artefactos (ver Estado de la cuestión preliminar) **(TRABAJOS EXISTENTES)**. Nuestra propuesta integra requisitos, modelo SysML v2 y pruebas en un grafo RDF y expone al LLM un conjunto de herramientas deterministas, obligándole a citar los artefactos que utiliza **(SOLUCIÓN PROPUESTA)**. La hipótesis se corroborará con 20 preguntas de referencia sobre el hilo digital de la bomba de infusión GPCA, midiendo precisión, exhaustividad y tasa de alucinación, y el tiempo a título indicativo **(PARÁMETROS PARA CORROBORAR LA HIPÓTESIS)**.

## Objetivos

**Objetivo general:** Desarrollar un copiloto de ingeniería basado en IA generativa que consulte y actúe sobre un hilo digital representado como grafo de conocimiento, para que las preguntas de trazabilidad e impacto se respondan de forma rápida, exhaustiva y fundamentada en los artefactos del proyecto.

| ID | Objetivo específico | Resultado en el repositorio | Criterio de aceptación | Traza a |
| --- | --- | --- | --- | --- |
| OE1 | Analizar el estado de la cuestión sobre hilo digital, grafos de conocimiento y LLM aplicados a MBSE | `docs/01-state-of-the-art.md` | 8 trabajos con DOI o URL verificados (al menos 3 artículos y 1 herramienta), seleccionados mediante una búsqueda sistemática en IEEE Xplore y Scopus completada con otros métodos documentados; 3 trabajos leídos completos y tabla comparativa | Causa, Trabajos existentes |
| OE2 | Diseñar la arquitectura del sistema y la ontología del hilo digital | `docs/02-architecture.md`, ADRs, `ontology/digital-thread.ttl`, `shapes/digital-thread-shapes.ttl` | Arquitectura hexagonal (puertos y adaptadores) descrita con las vistas de ISO/IEC/IEEE 42010 en los niveles C4, cada patrón de diseño ligado a su paquete (ADR-0017); ontología en OWL 2 (Turtle), alineada con OSLC RM y QM 2.1, que cubre requisito, elemento de modelo, caso de prueba, resultado de prueba y método de verificación con las relaciones satisface, verifica, depende de e informa sobre; las formas SHACL validan el caso de estudio sin errores y detectan cada ejemplo defectuoso | Causa, Solución propuesta |
| OE3 | Implementar la ingesta de artefactos en el grafo de conocimiento | `src/digital_thread_copilot/ingest/`, `data/gpca/` | Cadena de ingesta (lectura, conversión a RDF, validación SHACL, carga) para 3 tipos de artefactos: requisitos en YAML validado con JSON Schema, con exportación a ReqIF 1.2; modelo SysML v2 en notación textual; casos de prueba en YAML y sus resultados en JUnit XML; el 100 % de los artefactos del caso de estudio cargados; pruebas unitarias en CI | Causa |
| OE4 | Implementar el copiloto conectado al repositorio de ingeniería, con herramientas deterministas, generación de casos de prueba y guardarraíles | `src/digital_thread_copilot/copilot/`, `src/digital_thread_copilot/ui/` (chat web Chainlit) | El copiloto lee los artefactos versionados en el repositorio; al menos 5 herramientas (búsqueda, traza, impacto, ejecución de pruebas, lagunas de cobertura); un borrador de caso de prueba generado para un requisito no cubierto se valida antes de proponerse; toda respuesta cita IDs existentes; las acciones de escritura requieren confirmación y quedan registradas; chat web; demostración de trazabilidad de extremo a extremo (requisito, elemento de modelo, prueba, resultado); pruebas funcionales en CI. Extensiones, realizadas solo si hay tiempo: fragmentos SysML v2 e informes de trazabilidad generados; vista del subgrafo consultado y de la traza; reingesta con cada cambio de un artefacto | Hipótesis, Solución propuesta |
| OE5 | Evaluar la hipótesis con un conjunto de preguntas de referencia | `eval/`, `docs/05-evaluation.md` | 20 preguntas con respuesta de referencia; métricas calculadas automáticamente en CI; decisión documentada de aceptar o rechazar la hipótesis | Hipótesis, Parámetros |

## Estado de la cuestión preliminar

- **Cadena de búsqueda:** `("digital thread" OR "authoritative source of truth") AND ("knowledge graph" OR ontology) AND ("large language model" OR LLM OR "generative AI") AND (MBSE OR SysML OR traceability)`
- **Fecha de consulta:** _por completar_
- **Bases consultadas:** _por completar (p. ej. IEEE Xplore y Scopus, a través de la biblioteca UC3M)_

| Trabajo | Enfoque | Estándares | Limitación respecto a nuestro problema | Referencia (DOI o URL) |
| --- | --- | --- | --- | --- |
| _por completar_ | | | | |

> Regla del grupo: no se añade ninguna referencia sin comprobar su DOI o URL.

## Propuesta

1. **Hilo digital:** requisitos de seguridad, arquitectura lógica y artefactos de verificación de la bomba de infusión GPCA. Los requisitos se escriben en YAML, se validan con JSON Schema y se exportan a ReqIF 1.2, parte de la arquitectura publicada (AADL, Simulink/Stateflow) se traduce a un modelo lógico SysML v2 y los casos de prueba se derivan del material de verificación publicado. Todo se carga en un grafo RDF con una ontología ligera en OWL 2 (Turtle, `ontology/digital-thread.ttl`) alineada con OSLC y SysML v2 y controlada por formas SHACL.
2. **Conexión con el repositorio de ingeniería:** los artefactos se versionan en el repositorio Git y se cargan en el grafo al arrancar el sistema. Extensión: reingesta con cada cambio, de modo que el copiloto trabaje siempre sobre el estado actual del proyecto.
3. **Herramientas deterministas:** búsqueda de requisitos, consultas de trazas (SPARQL), análisis de impacto por recorrido del grafo y ejecución de pruebas.
4. **Generación de artefactos:** a petición, el copiloto redacta un caso de prueba para un requisito que ninguna prueba verifica. El borrador se valida frente a su esquema y solo se añade al repositorio tras la confirmación del ingeniero. Extensión: fragmentos SysML v2, validados con el analizador SysML v2, e informes de trazabilidad.
5. **Agente:** LLM orquestado con GitHub Copilot SDK según el patrón ReAct (razonar, llamar a una herramienta, leer su resultado, responder): elige y llama a las herramientas y cita siempre los artefactos utilizados.
6. **Guardarraíles:** respuestas rechazadas si no están fundamentadas en el grafo, separación de herramientas de lectura y escritura, confirmación de acciones y registro.
7. **Interfaz:** chat web construido con Chainlit, una capa fina sin lógica. Extensión: una vista del subgrafo consultado y de la traza de extremo a extremo (requisito, elemento de modelo, prueba, resultado).
8. **Arquitectura:** hexagonal (puertos y adaptadores): el grafo y las herramientas forman el núcleo; la ingesta (Pipes and Filters, un adaptador por formato), la exportación ReqIF, el proveedor del modelo (Strategy: modelo real o reproducción) y la interfaz son adaptadores. El guardarraíl es una cadena de validadores (Chain of Responsibility) y cada escritura es un comando confirmado y registrado (Command). Detalle: `docs/02-architecture.md` y ADR-0017.

## Validación de la propuesta

- **Caso de estudio:** hilo digital de la bomba de infusión GPCA, construido a partir de los artefactos públicos del proyecto Generic Infusion Pump (FDA, Universidad de Pensilvania, Universidad de Minnesota): un subconjunto de 12 requisitos de seguridad, los elementos del modelo SysML v2 correspondientes y los 12 casos de prueba que los verifican. Los documentos originales se enlazan, no se copian, ya que no se indica ninguna licencia.
- **Conjunto de datos:** 20 preguntas de trazabilidad, impacto y cobertura con su respuesta de referencia.
- **Métricas:** precisión y exhaustividad de los artefactos citados, tasa de alucinación (artefactos inexistentes o relaciones falsas), tiempo por pregunta (s). Métrica secundaria, solo medida (sin umbral, la hipótesis no depende de ella): tasa de validez de los casos de prueba generados (proporción que supera la validación al primer intento).
- **Umbrales:** exhaustividad y precisión de al menos 0,90; tasa de alucinación de como máximo un 5 %; exhaustividad significativamente mayor que la de la configuración de referencia (ii) indicada abajo (prueba pareada sobre las mismas preguntas, p < 0,05). Solo a título indicativo, fuera del criterio de aceptación: tiempo reducido al menos un 50 % frente al proceso manual.
- **Procedimiento:** las 20 preguntas se ejecutan 3 veces en tres configuraciones que usan el mismo modelo, la misma versión y los mismos parámetros: el copiloto; (i) el LLM solo con la pregunta, presentado como cota inferior; (ii) el LLM con el texto de todos los artefactos en su contexto, sin grafo ni herramientas. El criterio compara el copiloto con (ii). Por separado, 3 participantes externos al grupo responden cada uno a 10 preguntas, la mitad a mano y la otra mitad con el copiloto (orden cruzado). Amenaza a la validez: el caso de estudio es pequeño, por lo que todos los artefactos caben en el contexto de (ii) y la diferencia puede ser pequeña.

## Estándares implicados

| Estándar | Uso en el proyecto |
| --- | --- |
| SysML v2 | Modelo lógico del sistema (notación textual) |
| ReqIF 1.2 (OMG) | Exportación de los requisitos, escritos en YAML y validados con JSON Schema |
| OWL 2 / RDF (Turtle) | Ontología `ontology/digital-thread.ttl` y grafo de conocimiento |
| SPARQL | Consultas de trazabilidad e impacto |
| SHACL | Validación de la integridad del grafo (`shapes/digital-thread-shapes.ttl`) |
| JUnit XML | Resultados de prueba cargados en el grafo |
| ISO/IEC/IEEE 42010 | Descripción de la arquitectura por vistas (`docs/02-architecture.md`) |
| OSLC (RM, QM) | Vocabulario de enlaces de trazabilidad entre requisitos y pruebas |
| JSON Schema | Validación de los ficheros de requisitos y casos de prueba; definición de las herramientas del agente |
| AADL | Arquitectura de origen del caso de estudio GPCA, traducida en parte a SysML v2 |
| IEC 62304, ISO 14971 | Solo contexto: ciclo de vida del software de dispositivos médicos y gestión de riesgos, que motivan la trazabilidad en el caso de estudio |

## Declaración de uso de IA

- _Herramienta:_ Claude (Anthropic). _Uso:_ propuesta de estructura, borrador de redacción y traducción del planteamiento, revisados y validados por el grupo.
- _Herramienta:_ Claude (Anthropic). _Fechas:_ 15 y 16 de noviembre de 2026. _Uso (encuadre del proyecto):_ diagnóstico del fallo del workflow de documentación y redacción de su corrección; estimaciones de esfuerzo y escenarios de alcance; tablas de opciones con una recomendación para cada decisión de encuadre; propuesta de separar la hipótesis en un criterio principal y uno secundario, y propuesta de definición del criterio principal (umbrales, configuraciones de referencia, prueba pareada); listas de verificación de las referencias; revisión independiente del encuadre por un segundo agente de IA. _Revisión por el grupo:_ cada decisión fue tomada por un miembro del grupo a partir de las opciones presentadas, y el encuadre se somete a la aprobación de los tres miembros en el ADR-0001 (`docs/adr/0001-project-framing.md`). La solicitud de validación enviada al profesor el 15 de noviembre de 2026 fue redactada por el grupo.
- Los usos posteriores se recogen en la página [Uso de la IA](ai-usage.md) (en inglés).

La hipótesis y los objetivos son decisión del grupo.

## Referencias

Fuentes del caso de estudio (URL comprobadas el 22/10/2026):

- University of Pennsylvania, *The Generic Infusion Pump (GIP) project*. https://rtg.cis.upenn.edu/gip-UPenn/
- University of Minnesota, *GPCA artifacts: system requirements, AADL and Simulink/Stateflow models, verification suite* (2015). https://crisys.cs.umn.edu/gpca.shtml
- *Generic Infusion Pump Hazard Analysis and Safety Requirements, Version 1.0*, Technical Report MS-CIS-08-31, University of Pennsylvania, 2009. https://repository.upenn.edu/cis_reports/893
- Object Management Group, *SysML v2 release repository* (modelos de ejemplo, incluido el Simple Vehicle Model del anexo A; EPL 2.0). https://github.com/systems-modeling/sysml-v2-release

_Referencias del estado de la cuestión: por completar, solo con DOI o URL verificados._
