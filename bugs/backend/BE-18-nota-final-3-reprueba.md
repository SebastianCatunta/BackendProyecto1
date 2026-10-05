# BE-18 · Una nota final de exactamente 3.0 queda como reprobada

- Área: Backend
- Commit: 1a10949

## Ubicación
- Endpoint: POST /api/v1/grades/finalize/:enrollmentId (y POST /api/v1/groups/:id/finalize, que lo reutiliza)
- Funcionalidad: notas / nota final
- Archivo y línea(s): src/grades/grades.service.ts:132
- Capa: service
- Tipo de bug: operador/comparación

## Comportamiento
- Esperado: `PASSING_GRADE = 3.0` es la nota mínima para aprobar; con nota final 3.0 la matrícula queda `aprobada`.
- Actual: con nota final 3.0 queda `reprobada`.

## Reproducción (antes del fix)
- Request: con el grupo `6abf0b8bfead57fb41c12c59` con evaluaciones que suman 100% y todas las notas de la matrícula `6ac3d98df6cb4e89b0cdd965` en 3.0: `POST http://localhost:3001/api/v1/grades/finalize/6ac3d98df6cb4e89b0cdd965`, `Authorization: Bearer <token admin>`
- Body:
```json
{}
```
- Respuesta obtenida: `200 {"id":"6ac3d98df6cb4e89b0cdd965","finalGrade":3,"status":"reprobada"}`.

## Causa raíz
La comparación usaba `finalGrade > PASSING_GRADE` (estricto); la nota mínima para aprobar debe incluirse: `>=`.

## Solución
- Cambio aplicado: `finalGrade >= PASSING_GRADE ? Passed : Failed`.
- Verificación: mismo escenario con la matrícula `6ac3d8df6e7b485db8a49529` (todas las notas en 3.0) → `{"finalGrade":3,"status":"aprobada"}`.
