# Matriz de trazabilidad de cambios aprobados

Proyecto: Sistema Integral de Gestión de Tripulaciones. Reunión del CCB: 13/10/2026. Generada por `generar_matriz.py` a partir de `cambios_aprobados.json`, el backlog y las marcas `@trace` del prototipo.

## Vista 1. De la RFC a sus artefactos

| RFC | Decisión | Plazo | Requisitos | Casos de prueba | Módulos | Documentación | Prototipo (código) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **RFC-A3** Bloquear la asignación de pilotos no aptos a vuelos críticos | Aprobada | Extraordinaria: antes del Sprint 4 (hasta 16/10/2026) | HU-07, HU-08, HU-09, RNF-01 | TC-HU08-08 Bloquea al piloto sin simulación vigente en el escenario<br>TC-HU08-09 Bloquea con puntaje bajo el mínimo en vuelo crítico<br>TC-RNF01-05 Solo el operador ejecuta la asignación | Validación previa de la asignación<br>Servicio de ranking | Manual del operador de vuelos | NAV<br>abrirConfirmar<br>distancia<br>masCercano<br>permitido<br>ranking<br>vVueloOperador<br>vVuelos |
| **RFC-A1** Alerta de clima extremo en la comparación de escenarios | Aprobada | Sprint 4 (26/10/2026 – 06/11/2026) | HU-03, HU-05, HU-07, HU-10 | TC-HU03-05 La alerta meteorológica es obligatoria al registrar el vuelo<br>TC-HU07-10 Con alerta SEVERA solo se recomiendan escenarios de clima extremo<br>TC-HU07-11 Con alerta SEVERA y sin escenarios de clima extremo se bloquea la asignación<br>TC-HU10-04 La marca Clima Extremo se calcula y se puede corregir | Registro de vuelos<br>Catálogo de escenarios<br>Servicio de ranking | Manual del operador de vuelos<br>Guía del personal administrativo | distancia<br>fichaVuelo<br>masCercano<br>ranking<br>vTodos<br>vVueloOperador<br>vVueloTripulante |
| **RFC-A2** Notificación automática de la asignación por Teams y correo | Aprobada con condiciones | Sprint 5 (09/11/2026 – 20/11/2026) | HU-08, HU-12, RNF-02 | TC-HU08-07 Al guardar la asignación se envía la notificación por Teams y correo<br>TC-HU12-03 Cada notificación queda registrada con fecha, hora y destinatarios<br>TC-RNF02-04 La auditoría enlaza la asignación con su notificación | Módulo de notificaciones<br>Auditoría de asignaciones | Manual del operador de vuelos<br>Guía del personal administrativo | abrirConfirmar<br>vAuditoria<br>vVueloOperador<br>vVuelos |
| **RFC-C4** Más frecuencia de simulaciones por piloto y escenario | Aprobada (prioridad sobre RFC-C3) | Sprint 4 (26/10/2026 – 06/11/2026) | HU-06, HU-09, HU-11 | TC-HU09-04 La alerta usa la frecuencia configurada (4 meses)<br>TC-HU06-05 Se conservan los resultados de varias simulaciones en el año | Alertas de simulación<br>Modelo de datos de resultados | Manual de entrenamiento | ligarResultado<br>vResultado |
| **RFC-B1** Puntuación por promedio de las últimas 3 simulaciones | Aprobada (paquete PAQ-01 con RFC-C2) | Sprints 4 a 5 (26/10/2026 – 20/11/2026) | HU-06, HU-07, HU-08, HU-11, RNF-02, RNF-05 | TC-HU06-03 Se conservan al menos 3 resultados por piloto y escenario<br>TC-HU07-12 Promedio con 3, 2, 1 y más de 3 resultados<br>TC-HU07-14 Empate de promedios<br>TC-HU08-10 La asignación muestra el promedio y cuántas simulaciones lo forman<br>TC-HU11-05 El reporte histórico muestra la serie completa<br>TC-RNF05-03 La sincronización no pierde ni duplica resultados | Modelo de datos de resultados<br>Servicio de ranking<br>Carga desde el simulador | Manual del operador de vuelos<br>Manual de entrenamiento<br>Guía del personal administrativo | abrirConfirmar<br>distancia<br>ligarResultado<br>masCercano<br>ranking<br>vAuditoria<br>vResultado<br>vVueloOperador<br>vVuelos |
| **RFC-C2** Alineación con NAC-2026: certificación por estabilidad de competencias | Aprobada (paquete PAQ-01 con RFC-B1) | Sprints 4 a 6 (26/10/2026 – 04/12/2026) | HU-06, HU-07, HU-08, HU-11, RNF-02 | TC-HU07-13 Solo los pilotos estables son elegibles para la asignación<br>TC-HU08-11 La asignación explica la estabilidad del piloto<br>TC-REG-01 Regresión completa del motor de asignación<br>TC-HU11-06 El reporte muestra la estabilidad por escenario | Servicio de ranking<br>Modelo de datos de resultados<br>Auditoría de asignaciones | Manual de Certificación Interno v2.0<br>Manual del operador de vuelos | abrirConfirmar<br>distancia<br>ligarResultado<br>masCercano<br>ranking<br>vAuditoria<br>vResultado<br>vVueloOperador<br>vVuelos |

## Vista 2. Del requisito a las RFC aprobadas

| Requisito | Título en el backlog | RFC aprobadas que lo cambian | Elementos del prototipo que lo implementan |
| --- | --- | --- | --- |
| HU-03 | Registrar y actualizar vuelos | RFC-A1 | — |
| HU-05 | Consultar características de un vuelo | RFC-A1 | fichaVuelo, vVueloOperador, vTodos, vVueloTripulante |
| HU-06 | Registrar resultado de simulación | RFC-C4, RFC-B1, RFC-C2 | vResultado, ligarResultado |
| HU-07 | Recomendar tripulación según escenario más aproximado | RFC-A3, RFC-A1, RFC-B1, RFC-C2 | distancia, masCercano, ranking, vVueloOperador |
| HU-08 | Asignar tripulación a un vuelo | RFC-A3, RFC-A2, RFC-B1, RFC-C2 | vVuelos, vVueloOperador, abrirConfirmar |
| HU-09 | Alertar simulación anual pendiente | RFC-A3, RFC-C4 | — |
| HU-10 | Gestionar catálogo de escenarios | RFC-A1 | — |
| HU-11 | Reportes históricos de desempeño | RFC-C4, RFC-B1, RFC-C2 | — |
| HU-12 | Notificación de cambio de asignación | RFC-A2 | — |
| RNF-01 | Seguridad basada en roles | RFC-A3 | NAV, permitido |
| RNF-02 | Auditoría de asignaciones | RFC-A2, RFC-B1, RFC-C2 | abrirConfirmar, vAuditoria |
| RNF-05 | Integridad de la sincronización con el simulador | RFC-B1 | — |

## RFC que no se aprobaron

| RFC | Decisión | Votos | Motivo |
| --- | --- | --- | --- |
| RFC-B2 Fórmula híbrida 70 % simulación y 30 % horas reales | Aplazada | 2 a favor, 2 en contra, 1 abstención | Empate sin mayoría. Faltan las horas de vuelo por piloto (hoy se guardan por tripulación) y Cumplimiento debe confirmar que no contradice NAC-2026. |
| RFC-B3 Eliminar la validación manual del operador | Rechazada | 1 a favor, 4 en contra, 0 abstenciones | El riesgo de seguridad supera el beneficio de eficiencia. Se podrá presentar una RFC nueva de validación por excepción cuando RFC-A3 y RFC-A1 estén en producción. |
| RFC-C1 IA predictiva de escenarios | Rechazada | 0 a favor, 4 en contra, 1 abstención | Modelo de caja negra que no se puede justificar ante auditorías, y no hay datos etiquetados para entrenarlo. |
| RFC-C3 Mejora de la interfaz de consulta | Aplazada | Se priorizó RFC-C4 (3 a 2) | No tiene efecto en seguridad ni cumplimiento. Se revisa al terminar el Sprint 6. |
