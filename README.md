# Proyecto Tripulaciones — Sistema Integral de Gestión de Tripulaciones (TRI)

Rama `tripulaciones` del repositorio de trazabilidad de requisitos. El índice general de los proyectos está en la rama `main`.

## Versiones actuales

| ID | Artefacto | Tipo | Versión | Estado final | Autor | Fecha de cierre |
| --- | --- | --- | --- | --- | --- | --- |
| TRI-PBL-001 | [Product_backlog.html](Product_backlog.html) · fuente [Product_backlog_ReqView.csv](Product_backlog_ReqView.csv) | Product Backlog (18 ítems) | 1.0 | Entregado para revisión, 1 iteración | Federico Márquez | 13/10/2026 |
| TRI-RFC-002 | [RFC_Solicitudes_de_Cambio.pdf](RFC_Solicitudes_de_Cambio.pdf) · editable [RFC_Solicitudes_de_Cambio.docx](RFC_Solicitudes_de_Cambio.docx) | Solicitudes de cambio (RFC) | 1.0 | Entregado para revisión, 1 iteración | Federico Márquez | 13/10/2026 |

## 1. Contexto del proyecto

Una aerolínea quiere un sistema para asignar tripulaciones (un piloto y un copiloto) a sus vuelos. La tripulación debe ser la más adecuada según las aptitudes del piloto y las características del vuelo.

- **Consultas.** Las tripulaciones consultan sus vuelos asignados y las características de cualquier vuelo: fecha, origen, destino, y clima y visibilidad previstos.
- **Datos.** El personal administrativo registra tripulantes, tripulaciones y vuelos.
- **Simulador.** Un simulador externo evalúa a cada piloto en escenarios estándar, que son combinaciones de parámetros de visibilidad, meteorología y relieve. Cada piloto debe simular al menos una vez al año en cada escenario. El resultado es un número con fecha.
- **Asignación.** Los operadores de vuelos comparan el vuelo con los escenarios, eligen el más cercano y asignan al piloto con la puntuación más alta en ese escenario.

## 2. Necesidades originales

Las necesidades salen de las historias de usuario del backlog. Cada fila indica quién la tiene, qué necesita y para qué.

| Requisito | Quién | Qué necesita | Para qué |
| --- | --- | --- | --- |
| HU-01 | PersonalAdministrativo | Registrar y actualizar los datos de los tripulantes (pilotos y copilotos) | mantener el personal disponible y correctamente identificado en el sistema |
| HU-02 | PersonalAdministrativo | Registrar y actualizar tripulaciones (parejas piloto-copiloto) | tenerlas disponibles al momento de asignarlas a un vuelo |
| HU-03 | PersonalAdministrativo | Registrar y actualizar los datos de cada vuelo (fecha, origen, destino, condiciones meteorológicas y de visibilidad previstas) | que operadores y tripulación cuenten con información confiable |
| HU-04 | PilotoCopiloto | Consultar mis vuelos asignados | conocer mi programación |
| HU-05 | MiembroTripulacion | Consultar las características de cualquier vuelo | prepararme adecuadamente |
| HU-06 | Piloto | Que el resultado numérico de mi simulación en un escenario quede registrado en el sistema | que se use en las decisiones de asignación |
| HU-07 | OperadorVuelo | Que el sistema identifique el escenario estandarizado más aproximado a un vuelo y me recomiende la tripulación con mayor puntuación en ese escenario | asignar la tripulación más adecuada |
| HU-08 | OperadorVuelo | Asignar la tripulación a un vuelo (confirmando o ajustando la recomendación, con motivo si me aparto de ella) | dejar formalizada la decisión |
| HU-09 | Piloto | Recibir un aviso cuando se acerque la fecha límite para completar la simulación anual de algún escenario | cumplir con la evaluación obligatoria |
| HU-10 | AdministradorSistema | Gestionar (crear/editar) el catálogo de escenarios estandarizados de simulación | mantenerlo actualizado frente a nuevas condiciones operativas |
| HU-11 | OperadorDireccion | Generar reportes históricos de desempeño de pilotos por escenario | apoyar decisiones y evaluaciones periódicas |
| HU-12 | UsuarioSistema | Recibir una notificación cuando cambie mi asignación | enterarme sin tener que consultar manualmente |

## 3. Requisitos priorizados

Backlog de 18 ítems: 10 con prioridad alta, 5 media y 3 baja. Los IDs siguen el orden de la exportación de ReqView. El detalle y los criterios de aceptación están en [Product_backlog.html](Product_backlog.html).

**Historias de usuario**

| ID | Historia | Actor | Prioridad |
| --- | --- | --- | --- |
| HU-01 | Registrar y actualizar tripulantes | PersonalAdministrativo | Alta |
| HU-02 | Registrar y actualizar tripulaciones | PersonalAdministrativo | Alta |
| HU-03 | Registrar y actualizar vuelos | PersonalAdministrativo | Alta |
| HU-04 | Consultar vuelos asignados | PilotoCopiloto | Alta |
| HU-05 | Consultar características de un vuelo | MiembroTripulacion | Alta |
| HU-06 | Registrar resultado de simulación | Piloto | Alta |
| HU-07 | Recomendar tripulación según escenario más aproximado | OperadorVuelo | Alta |
| HU-08 | Asignar tripulación a un vuelo | OperadorVuelo | Alta |
| HU-09 | Alertar simulación anual pendiente | Piloto | Media |
| HU-10 | Gestionar catálogo de escenarios | AdministradorSistema | Media |
| HU-11 | Reportes históricos de desempeño | OperadorDireccion | Baja |
| HU-12 | Notificación de cambio de asignación | UsuarioSistema | Baja |

**Restricciones (requisitos no funcionales)**

| ID | Restricción | Prioridad |
| --- | --- | --- |
| RNF-01 | Seguridad basada en roles | Alta |
| RNF-02 | Auditoría de asignaciones | Alta |
| RNF-03 | Disponibilidad continua | Media |
| RNF-04 | Rendimiento en consultas | Media |
| RNF-05 | Integridad de la sincronización con el simulador | Media |
| RNF-06 | Usabilidad móvil | Baja |

## 4. Validación

Cada ítem del backlog tiene criterios de aceptación en formato Dado / Cuando / Entonces.

Las RFC añaden criterios y pruebas propios:

- **RFC-A1 (escenarios de tormenta).** CA-1: con alerta SEVERA, el sistema recomienda solo escenarios marcados «Clima Extremo». CA-2: con alerta SEVERA y ningún escenario marcado, bloquea la asignación, avisa y registra el evento en la auditoría.
- **RFC-B1.** Casos de prueba nuevos para el promedio con 3, 2, 1 y más de 3 resultados, y para el empate de promedios.
- **RFC-B2.** 16 h de QA: piloto novel sin horas, veterano con horas muy altas y regresión del ranking.
- **RFC-C2.** Pruebas de regresión sobre la asignación, repetición de asignaciones históricas con la regla nueva y prueba de aceptación con operadores.

## 5. Cadena de trazabilidad

Cada escenario del documento «Casos de Estudio: Escenarios de Cambio» (Academia de Operaciones Aéreas) se traza hasta su RFC y hasta los requisitos del backlog que modifica:

| Caso | Origen | RFC | Requisitos afectados |
| --- | --- | --- | --- |
| A1 El Factor Meteorológico | Correo del Cap. Ricardo Méndez | RFC-A1 | HU-03, HU-05, HU-07, HU-10 |
| A2 El Cuello de Botella Administrativo | Informe de Gestión | RFC-A2 | HU-08, HU-12, RNF-02 |
| Actividad 4, nivel inicial | Dirección de Seguridad Operacional | RFC-A3 | HU-07, HU-08, HU-09, RNF-01 |
| B1 La Trampa del «Golpe de Suerte» | Memorando de QA, Ing. Sofía Valdés | RFC-B1 | HU-06, HU-07, HU-08, HU-11, RNF-02, RNF-05 |
| B2 Teoría vs. Práctica | Nota técnica, Dirección de Entrenamiento | RFC-B2 | HU-01, HU-07, HU-08 |
| Actividad 3, nivel intermedio | Jefatura de Operaciones de Vuelo | RFC-B3 | HU-07, HU-08, RNF-01, RNF-02 |
| C1 La Promesa de la IA | Propuesta de Transformación Digital | RFC-C1 | HU-07, HU-10, RNF-02 |
| C2 El Choque Normativo | Circular de la AAC | RFC-C2 | HU-06, HU-07, HU-08, HU-11, RNF-02 |
| Actividad 3, nivel avanzado | Dirección de Entrenamiento / Experiencia de Usuario | RFC-C3, RFC-C4 | HU-04, HU-05, HU-06, HU-09, RNF-06 |

**Dependencia clave.** RFC-C2 (estabilidad de competencias, norma NAC-2026) necesita el histórico de simulaciones que crea RFC-B1, y ese histórico necesita más simulaciones por piloto (RFC-C4). Por eso B1 y C2 se aprueban y ejecutan como un solo paquete de cambio.

## 6. Gestión de cambios

Solicitudes registradas en TRI-RFC-002:

| RFC | Título | Solicitante | Tipo | Prioridad | Decisión / estado |
| --- | --- | --- | --- | --- | --- |
| RFC-A1 | Alerta de clima extremo en la comparación de escenarios | Cap. Ricardo Méndez | Mejora funcional | Alta | Sin decisión registrada |
| RFC-A2 | Notificación automática de la asignación por Teams y correo | Gerencia de Gestión Operativa | Mejora funcional | Media | Sin decisión registrada |
| RFC-A3 | Bloquear la asignación de pilotos no aptos a vuelos críticos | Dirección de Seguridad Operacional | Corrección de defecto | Crítica | Sin decisión registrada |
| RFC-B1 | Puntuación por promedio de las últimas 3 simulaciones | Ing. Sofía Valdés | Mejora funcional | Alta | Sin decisión registrada |
| RFC-B2 | Fórmula híbrida 70 % simulación y 30 % horas reales | Dirección de Entrenamiento | Mejora funcional | Media | Esfuerzo estimado 54 h (L) |
| RFC-B3 | Eliminar la validación manual del operador | Jefatura de Operaciones de Vuelo | Otro: cambio de proceso | Media | Riesgos analizados; se recomienda mantener la validación por excepción |
| RFC-C1 | IA predictiva de escenarios | Transformación Digital | Cambio de arquitectura | Baja | Rechazada (justificación del Tech Lead) |
| RFC-C2 | Alineación con NAC-2026: certificación por estabilidad | Autoridad de Aviación Civil | Cambio regulatorio | Alta | Plan de 9 pasos en los sprints 4 a 6 |
| RFC-C3 | Mejora de la interfaz de consulta | Experiencia de Usuario | Mejora funcional | Media | Aplazada (propuesta del analista) |
| RFC-C4 | Más frecuencia de simulaciones | Dirección de Entrenamiento | Cambio de proceso | Alta | Priorizada (propuesta del analista) |

Las decisiones marcadas como propuesta las toma el comité de control de cambios (CCB). Aquí solo está registrado el voto del analista.
