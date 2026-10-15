# Trazabilidad de requisitos

Repositorio de los trabajos de la asignatura Ingeniería de Requisitos (UPB): backlog, solicitudes de cambio, prototipo, pruebas y trazabilidad, versionados con Git.

Cada proyecto está en su propia rama. Esta rama (`main`) solo presenta el repositorio: aquí no hay artefactos.

## Proyectos

| Rama | Proyecto | Qué contiene |
| --- | --- | --- |
| [`tripulaciones`](../../tree/tripulaciones) | Sistema integral de gestión de tripulaciones | Backlog, solicitudes de cambio (RFC), prototipo de baja fidelidad con sus pruebas, acta del CCB, matriz de trazabilidad y auditoría |

Los demás proyectos del curso se agregarán como ramas nuevas cuando tengan entregas.

## Cómo está organizada cada rama

Cada rama tiene un `README.md` que cuenta, en este orden:

1. el contexto del proyecto;
2. las necesidades originales;
3. los requisitos priorizados;
4. la validación;
5. la cadena de trazabilidad;
6. la gestión de cambios.

Al comienzo de ese README hay una tabla con las versiones actuales de los artefactos y sus metadatos: ID, versión, estado final, autor o revisor, fecha de cierre y artefactos relacionados.

Dentro de la rama, los archivos van en **una carpeta por tarea**. En `tripulaciones`:

| Carpeta | Tarea | Qué hay dentro |
| --- | --- | --- |
| `Backlog/` | Product Backlog | Backlog de 18 ítems (HTML y CSV de ReqView) |
| `U3A1-RFC/` | U3A1 · Solicitudes de cambio | Las 10 RFC (PDF y Word) |
| `U3A2-Prototipado/` | U3A2 · Prototipado y CCB | Informe, prototipo, pruebas automáticas y acta y matriz del CCB |
| `U4A1-Trazabilidad/` | U4A1 · Trazabilidad de un requisito | Informe, herramienta, catálogo de metadatos, matriz en Excel y auditoría |

## Identificadores de artefactos

Cada artefacto tiene un ID único con el formato `<PROYECTO>-<TIPO>-<NNN>`: la clave del proyecto (por ejemplo `TRI` para tripulaciones), el tipo de artefacto y un consecutivo dentro del proyecto. Tipos usados: `PBL` backlog, `RFC` solicitudes de cambio, `PRO` prototipo, `PRU` pruebas, `DOC` informe, `CCB` acta del comité, `MTZ` matriz, `AUD` auditoría, `SCR` script. Por ejemplo, `TRI-MTZ-007` es la matriz de trazabilidad de tripulaciones.

## Aprendizaje

Reflexión sobre las técnicas que usé en el proyecto Tripulaciones.

### Qué funcionó y por qué repetirlo

| Técnica | Por qué fue adecuada |
| --- | --- |
| Historias de usuario con criterios Dado / Cuando / Entonces | Los criterios guiaron las pruebas automáticas: las 30 pruebas del prototipo verifican comportamientos que ellos describen. |
| RFC con análisis de impacto y votación del CCB | El caso trae reglas que cambian y varios interesados con intereses opuestos. Votar obligó a justificar cada decisión, por ejemplo rechazar la IA de «caja negra» (RFC-C1) o aplazar la fórmula 70/30 (RFC-B2). |
| Marcas `@trace` en el código y un script que genera la matriz | La matriz nunca queda desactualizada respecto al código: si se borra una marca, la auditoría lo muestra. |
| Prototipo de baja fidelidad con pruebas automáticas | Mostró defectos reales antes de construir, como el botón «Asignar» fuera de la pantalla en móvil. |

### Qué falló y cómo se detectó

| Qué falló | Cómo se detectó |
| --- | --- |
| El caso de estudio dice que el resultado nuevo elimina el anterior, pero el criterio de HU-06 lo conserva. Nadie lo había notado. | Al escribir RFC-B1, que necesita el histórico de resultados. |
| El prototipo no resolvía el empate entre tripulaciones: marcaba dos como «Recomendada». | Con una prueba automática sobre el vuelo V104 (DEF-01). |
| Los casos de prueba de las RFC quedaron solo en papel. | En la auditoría: 6 RFC aprobadas con 22 casos de prueba sin implementar. |
| El backlog no recogió las decisiones del CCB y el Vision Board no se guardó en el repositorio. | En la auditoría de trazabilidad. |
| La prueba con usuarios fue simulada, no con personas reales. | Es una limitación declarada en el informe de U3A2. |

### Qué haría diferente desde el inicio

- Especificar la regla de asignación con una tabla de decisión que incluya el desempate, y no dejarla en una frase del enunciado.
- Escribir los casos de prueba como código al mismo tiempo que los criterios de aceptación.
- Poner las marcas de trazabilidad desde la primera línea de código, no al final.
- Guardar todos los artefactos de origen (Vision Board incluido) en el repositorio desde el primer día.
- Probar el prototipo con personas reales antes del CCB.

**Regla general:** si una técnica se puede automatizar y verificar (pruebas, matriz, metadatos), se automatiza; así los errores aparecen antes de la auditoría.
