# Proyecto Tripulaciones — Sistema Integral de Gestión de Tripulaciones (TRI)

Rama `tripulaciones` del repositorio de trazabilidad de requisitos. El índice general de los proyectos está en la rama `main`.

## Versiones actuales

Cada artefacto lleva sus metadatos: ID único, versión, estado final, autor o revisor, fecha de cierre y artefactos relacionados. La tabla se genera con `python3 U4A1-Trazabilidad/herramienta.py catalogo` a partir de [U4A1-Trazabilidad/catalogo_artefactos.json](U4A1-Trazabilidad/catalogo_artefactos.json); no se edita a mano.

<!-- METADATOS:INICIO -->
| ID | Artefacto | Tipo | Versión | Estado final | Autor o revisor | Fecha de cierre | Artefactos relacionados |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TRI-PBL-001 | [Product_backlog.html](Backlog/Product_backlog.html) · [Product_backlog.reqw](Backlog/Product_backlog.reqw) | Product Backlog (18 ítems) | 1.0 | Aprobado, 1 iteración | Federico Márquez (autor); revisor: Pendiente (docente) | 13/10/2026 | TRI-RFC-002, TRI-PRO-003, TRI-MTZ-007 |
| TRI-RFC-002 | [RFC_Solicitudes_de_Cambio.pdf](U3A1-RFC/RFC_Solicitudes_de_Cambio.pdf) · [RFC_Solicitudes_de_Cambio.docx](U3A1-RFC/RFC_Solicitudes_de_Cambio.docx) | RFC (10 solicitudes) | 1.0 | Entregado, 1 iteración. Decisiones tomadas en TRI-CCB-006 | Federico Márquez (autor); revisor: Pendiente (docente) | 13/10/2026 | TRI-PBL-001, TRI-CCB-006, TRI-DOC-005 |
| TRI-PRO-003 | [index.html](U3A2-Prototipado/prototipo/index.html) | Prototipo (HTML) | 0.2 | Validado con 30 pruebas automáticas; 7 defectos abiertos (DEF-01, DEF-06 a DEF-11) | Federico Márquez (autor); revisor: Pendiente (docente) | 13/10/2026 | TRI-PBL-001, TRI-PRU-004, TRI-DOC-005, TRI-MTZ-007 |
| TRI-PRU-004 | [test_prototipo.py](U3A2-Prototipado/pruebas/test_prototipo.py) · [resultados_pruebas.json](U3A2-Prototipado/pruebas/resultados_pruebas.json) (+5) | Casos de prueba automatizados | 1.0 | 30 de 30 aprobadas | Federico Márquez (autor); revisor: Pendiente (docente) | 14/10/2026 | TRI-PRO-003, TRI-PBL-001, TRI-MTZ-007 |
| TRI-DOC-005 | [U3A2_Prototipado_CCB_Federico_Marquez.pdf](U3A2-Prototipado/U3A2_Prototipado_CCB_Federico_Marquez.pdf) · [U3A2_Prototipado_CCB_Federico_Marquez.docx](U3A2-Prototipado/U3A2_Prototipado_CCB_Federico_Marquez.docx) | Informe | 1.0 | Entregado, 1 iteración | Federico Márquez (autor); revisor: Pendiente (docente) | 14/10/2026 | TRI-PRO-003, TRI-PRU-004, TRI-CCB-006, TRI-RFC-002 |
| TRI-CCB-006 | [cambios_aprobados.json](U3A2-Prototipado/trazabilidad/cambios_aprobados.json) | Acta del CCB (datos) | 1.0 | Reunión simulada del 13/10/2026; 6 RFC aprobadas, 4 sin aprobar | Federico Márquez (autor); revisor: Pendiente (docente) | 13/10/2026 | TRI-RFC-002, TRI-DOC-005, TRI-MTZ-007 |
| TRI-MTZ-007 | [Matriz_trazabilidad.xlsx](U4A1-Trazabilidad/Matriz_trazabilidad.xlsx) · [Matriz_trazabilidad.md](U3A2-Prototipado/trazabilidad/Matriz_trazabilidad.md) (+1) | Matriz de trazabilidad (generada) | 1.0 | Generada por script; auditada en TRI-AUD-008 | Federico Márquez (autor); revisor: Pendiente (docente) | 15/10/2026 | TRI-PBL-001, TRI-PRO-003, TRI-PRU-004, TRI-CCB-006, TRI-AUD-008, TRI-SCR-009 |
| TRI-AUD-008 | [Auditoria_trazabilidad.md](U4A1-Trazabilidad/Auditoria_trazabilidad.md) · [U4A1_Trazabilidad_Federico_Marquez.pdf](U4A1-Trazabilidad/U4A1_Trazabilidad_Federico_Marquez.pdf) (+1) | Informe de auditoría (generado) | 1.0 | Realizada; hallazgos abiertos con responsable | Federico Márquez (autor); revisor: Pendiente (docente) | 15/10/2026 | TRI-MTZ-007, TRI-SCR-009, TRI-PBL-001 |
| TRI-SCR-009 | [herramienta.py](U4A1-Trazabilidad/herramienta.py) · [generar_matriz.py](U3A2-Prototipado/trazabilidad/generar_matriz.py) (+2) | Script (Python) | 1.0 | Operativa | Federico Márquez (autor); revisor: Pendiente (docente) | 15/10/2026 | TRI-MTZ-007, TRI-AUD-008, TRI-CCB-006 |
<!-- METADATOS:FIN -->

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

Backlog de 18 ítems: 10 con prioridad alta, 5 media y 3 baja. Los IDs siguen el orden de la exportación de ReqView. El detalle y los criterios de aceptación están en [Product_backlog.html](Backlog/Product_backlog.html).

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

Solicitudes registradas en TRI-RFC-002 y decididas por el comité de control de cambios (CCB) el 13/10/2026. La reunión fue una simulación en la que el autor asumió los cinco roles; el acta está en [U3A2-Prototipado/U3A2_Prototipado_CCB_Federico_Marquez.pdf](U3A2-Prototipado/U3A2_Prototipado_CCB_Federico_Marquez.pdf) y los datos en [U3A2-Prototipado/trazabilidad/cambios_aprobados.json](U3A2-Prototipado/trazabilidad/cambios_aprobados.json).

| RFC | Título | Solicitante | Tipo | Prioridad | Decisión del CCB (votos a favor-en contra-abst.) |
| --- | --- | --- | --- | --- | --- |
| RFC-A1 | Alerta de clima extremo en la comparación de escenarios | Cap. Ricardo Méndez | Mejora funcional | Alta | Aprobada (5-0-0), Sprint 4 |
| RFC-A2 | Notificación automática de la asignación por Teams y correo | Gerencia de Gestión Operativa | Mejora funcional | Media | Aprobada con condiciones (4-0-1), Sprint 5 |
| RFC-A3 | Bloquear la asignación de pilotos no aptos a vuelos críticos | Dirección de Seguridad Operacional | Corrección de defecto | Crítica | Aprobada, extraordinaria hasta el 16/10/2026 (5-0-0) |
| RFC-B1 | Puntuación por promedio de las últimas 3 simulaciones | Ing. Sofía Valdés | Mejora funcional | Alta | Aprobada en paquete con C2 (5-0-0), Sprints 4 a 6 |
| RFC-B2 | Fórmula híbrida 70 % simulación y 30 % horas reales | Dirección de Entrenamiento | Mejora funcional | Media | Aplazada (2-2-1): faltan las horas por piloto |
| RFC-B3 | Eliminar la validación manual del operador | Jefatura de Operaciones de Vuelo | Otro: cambio de proceso | Media | Rechazada (1-4-0) |
| RFC-C1 | IA predictiva de escenarios | Transformación Digital | Cambio de arquitectura | Baja | Rechazada (0-4-1) |
| RFC-C2 | Alineación con NAC-2026: certificación por estabilidad | Autoridad de Aviación Civil | Cambio regulatorio | Alta | Aprobada en paquete con B1 (5-0-0), Sprints 4 a 6 |
| RFC-C3 | Mejora de la interfaz de consulta | Experiencia de Usuario | Mejora funcional | Media | Aplazada: se prioriza C4 (3-2) |
| RFC-C4 | Más frecuencia de simulaciones | Dirección de Entrenamiento | Cambio de proceso | Alta | Aprobada (prioridad sobre C3), Sprint 4 |

## 7. Entregas por tarea

Cada tarea del curso tiene su carpeta. Los artefactos de una tarea están dentro de ella.

| Carpeta | Tarea | Contenido |
| --- | --- | --- |
| [Backlog/](Backlog/) | Product Backlog | Backlog de 18 ítems: archivo de ReqView (`.reqw`, fuente) y vista en HTML |
| [U3A1-RFC/](U3A1-RFC/) | U3A1 · Solicitudes de cambio (RFC) | Las 10 RFC en PDF y Word |
| [U3A2-Prototipado/](U3A2-Prototipado/) | U3A2 · Prototipado y CCB | Informe, `prototipo/` (baja fidelidad, HU-04 a HU-08, RNF-01, RNF-02 y RNF-06), `pruebas/` (30 de 30 aprobadas, resultados y capturas) y `trazabilidad/` (decisiones del CCB y matriz de los cambios aprobados) |
| [U4A1-Trazabilidad/](U4A1-Trazabilidad/) | U4A1 · Trazabilidad de un requisito | Informe, herramienta, catálogo de metadatos, matriz en Excel y auditoría |

La prueba con usuarios del informe U3A2 es una simulación con personas ficticias. El CCB también fue una simulación.

## 8. Trazabilidad y auditoría

La cadena **necesidad → requisito → prueba → código → resultado** se genera con un script, sin editar nada a mano:

```
python3 U4A1-Trazabilidad/herramienta.py todo
```

El script lee las marcas `@trace HU-xx` del código del prototipo, el backlog, los resultados de las pruebas y git. Produce [Matriz_trazabilidad.xlsx](U4A1-Trazabilidad/Matriz_trazabilidad.xlsx) y [Auditoria_trazabilidad.md](U4A1-Trazabilidad/Auditoria_trazabilidad.md). Requiere Python 3.9+ y `openpyxl`. Se ejecuta desde la raíz del repositorio, con los cambios ya agregados a git.
