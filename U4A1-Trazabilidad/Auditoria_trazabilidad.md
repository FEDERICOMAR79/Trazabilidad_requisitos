# Auditoría de trazabilidad end-to-end

Generada por `U4A1-Trazabilidad/herramienta.py auditoria`. Fecha de la matriz: 15/10/2026.

Cadena auditada: **necesidad de negocio → requisito → caso de prueba → código → resultado**.

## Resultado

- Requisitos auditados: 18 (HU y RNF del backlog).
- Con la cadena completa: **8 de 18** (HU-04, HU-05, HU-06, HU-07, HU-08, RNF-01, RNF-02, RNF-06).
- Hallazgos: 21 en total; 10 abiertos o por resolver, 11 cerrados o aceptados.
- Severidad de los abiertos: 1 alto, 8 medio, 1 bajo.

## Cadena por requisito

| Requisito | Necesidad | Prueba | Código | Resultado | Cadena completa |
| --- | --- | --- | --- | --- | --- |
| HU-01 | ✓ | ✗ | ✗ | ✗ | No |
| HU-02 | ✓ | ✗ | ✗ | ✗ | No |
| HU-03 | ✓ | ✗ | ✗ | ✗ | No |
| HU-04 | ✓ | ✓ | ✓ | ✓ | Sí |
| HU-05 | ✓ | ✓ | ✓ | ✓ | Sí |
| HU-06 | ✓ | ✓ | ✓ | ✓ | Sí |
| HU-07 | ✓ | ✓ | ✓ | ✓ | Sí |
| HU-08 | ✓ | ✓ | ✓ | ✓ | Sí |
| HU-09 | ✓ | ✗ | ✗ | ✗ | No |
| HU-10 | ✓ | ✗ | ✗ | ✗ | No |
| HU-11 | ✓ | ✗ | ✗ | ✗ | No |
| HU-12 | ✓ | ✗ | ✗ | ✗ | No |
| RNF-01 | ✓ | ✓ | ✓ | ✓ | Sí |
| RNF-02 | ✓ | ✓ | ✓ | ✓ | Sí |
| RNF-03 | ✓ | ✗ | ✗ | ✗ | No |
| RNF-04 | ✓ | ✗ | ✗ | ✗ | No |
| RNF-05 | ✓ | ✗ | ✗ | ✗ | No |
| RNF-06 | ✓ | ✓ | ✓ | ✓ | Sí |

## Hallazgos

| ID | Tipo de ruptura | Elemento | Detalle | Severidad | Estado | Responsable | Acción |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AUD-01 | RFC → prueba | RFC-A3 | 3 casos de prueba propuestos sin implementar (TC-HU08-08, TC-HU08-09, TC-RNF01-05). | Alto | Abierto | QA Lead | Escribirlos al construir el cambio. Plazo: Extraordinaria: antes del Sprint 4 (hasta 16/10/2026). |
| AUD-02 | Artefacto ausente | M-02 | El Vision Board (fuente de las necesidades NEG-01 a NEG-05) no está en el repositorio propio. | Medio | Abierto | Autor | Agregar el Vision Board como artefacto TRI-VIS y enlazarlo desde las necesidades. |
| AUD-03 | Backlog desactualizado | M-03 | El backlog (v1.0) no refleja las decisiones del CCB del 13/10/2026 (por ejemplo, el promedio de 3 simulaciones de RFC-B1 y el motivo obligatorio de RFC-A3). | Medio | Abierto | Analista de requisitos | Publicar backlog v1.1 con los criterios de aceptación de las RFC aprobadas. |
| AUD-04 | Código → requisito | vEvaluacion | La función vEvaluacion del prototipo no tiene marca @trace: implementa una pantalla sin requisito en el backlog (consulta de escenarios y evaluación del piloto, que el caso describe). | Medio | Abierto | Analista de requisitos | Agregar una historia de usuario al backlog para la consulta de escenarios y marcar la función. |
| AUD-05 | RFC → prueba | RFC-A1 | 4 casos de prueba propuestos sin implementar (TC-HU03-05, TC-HU07-10, TC-HU07-11, TC-HU10-04). | Medio | Abierto | QA Lead | Escribirlos al construir el cambio. Plazo: Sprint 4 (26/10/2026 – 06/11/2026). |
| AUD-06 | RFC → prueba | RFC-A2 | 3 casos de prueba propuestos sin implementar (TC-HU08-07, TC-HU12-03, TC-RNF02-04). | Medio | Abierto | QA Lead | Escribirlos al construir el cambio. Plazo: Sprint 5 (09/11/2026 – 20/11/2026). |
| AUD-07 | RFC → prueba | RFC-C4 | 2 casos de prueba propuestos sin implementar (TC-HU09-04, TC-HU06-05). | Medio | Abierto | QA Lead | Escribirlos al construir el cambio. Plazo: Sprint 4 (26/10/2026 – 06/11/2026). |
| AUD-08 | RFC → prueba | RFC-B1 | 6 casos de prueba propuestos sin implementar (TC-HU06-03, TC-HU07-12, TC-HU07-14, TC-HU08-10, TC-HU11-05, TC-RNF05-03). | Medio | Abierto | QA Lead | Escribirlos al construir el cambio. Plazo: Sprints 4 a 5 (26/10/2026 – 20/11/2026). |
| AUD-09 | RFC → prueba | RFC-C2 | 4 casos de prueba propuestos sin implementar (TC-HU07-13, TC-HU08-11, TC-REG-01, TC-HU11-06). | Medio | Abierto | QA Lead | Escribirlos al construir el cambio. Plazo: Sprints 4 a 6 (26/10/2026 – 04/12/2026). |
| AUD-10 | Contradicción entre fuentes | M-01 | El caso de estudio dice que el resultado nuevo elimina el anterior; el criterio de aceptación de HU-06 lo conserva en el historial. RFC-B1 adopta la versión con historial. | Medio | Cerrado | Analista de requisitos | Resuelto en RFC-B1 (U3A1) y verificado en la prueba P22. |
| AUD-11 | Requisito → código | HU-01 Registrar y actualizar tripulantes | Sin código en el prototipo. Registro administrativo; no cambia la decisión de asignación que valida el prototipo (U3A2, sección 7.1). | Medio | Aceptado (fuera de alcance) | Product Owner | Planificar su construcción tras el prototipo. |
| AUD-12 | Requisito → código | HU-02 Registrar y actualizar tripulaciones | Sin código en el prototipo. Registro administrativo; fuera del alcance del prototipo (U3A2, sección 7.1). | Medio | Aceptado (fuera de alcance) | Product Owner | Planificar su construcción tras el prototipo. |
| AUD-13 | Requisito → código | HU-03 Registrar y actualizar vuelos | Sin código en el prototipo. Registro administrativo; fuera del alcance del prototipo (U3A2, sección 7.1). | Medio | Aceptado (fuera de alcance) | Product Owner | Planificar su construcción tras el prototipo. |
| AUD-14 | Prueba → requisito | P19, P20, P26, P27, P28, P30 | Pruebas sin requisito del backlog: consulta de escenarios (P19, P20) y pruebas transversales de defectos y calidad (P26 a P28, P30). | Bajo | Abierto | QA Lead | Relacionar P19 y P20 con la historia nueva; las demás quedan como pruebas de regresión. |
| AUD-15 | Requisito → código | HU-09 Alertar simulación anual pendiente | Sin código en el prototipo. Alerta de simulación anual; requiere calendario y notificaciones (RFC-A3, CCB 13/10/2026). | Bajo | Aceptado (fuera de alcance) | Product Owner | Planificar su construcción tras el prototipo. |
| AUD-16 | Requisito → código | HU-10 Gestionar catálogo de escenarios | Sin código en el prototipo. Gestión del catálogo; el prototipo trae escenarios fijos. | Bajo | Aceptado (fuera de alcance) | Product Owner | Planificar su construcción tras el prototipo. |
| AUD-17 | Requisito → código | HU-11 Reportes históricos de desempeño | Sin código en el prototipo. Reportes históricos; dependen del histórico de RFC-B1. | Bajo | Aceptado (fuera de alcance) | Product Owner | Planificar su construcción tras el prototipo. |
| AUD-18 | Requisito → código | HU-12 Notificación de cambio de asignación | Sin código en el prototipo. Notificaciones; dependen de RFC-A2 (Sprint 5). | Bajo | Aceptado (fuera de alcance) | Product Owner | Planificar su construcción tras el prototipo. |
| AUD-19 | Requisito → código | RNF-03 Disponibilidad continua | Sin código en el prototipo. Disponibilidad 24/7; no medible en un prototipo local. | Bajo | Aceptado (fuera de alcance) | Product Owner | Planificar su construcción tras el prototipo. |
| AUD-20 | Requisito → código | RNF-04 Rendimiento en consultas | Sin código en el prototipo. Rendimiento; sin backend no hay tiempos reales que medir. | Bajo | Aceptado (fuera de alcance) | Product Owner | Planificar su construcción tras el prototipo. |
| AUD-21 | Requisito → código | RNF-05 Integridad de la sincronización con el simulador | Sin código en el prototipo. Sincronización con el simulador; el simulador es externo y el prototipo no se conecta. | Bajo | Aceptado (fuera de alcance) | Product Owner | Planificar su construcción tras el prototipo. |
