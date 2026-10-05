# BE-29 · Se puede editar el plan de evaluación de un grupo de un periodo cerrado

- Área: Backend
- Commit: 89fb590

## Ubicación
- Endpoint: PATCH /api/evaluations/:id
- Funcionalidad: evaluaciones
- Archivo y línea(s): src/evaluations/evaluations.service.ts:47-49
- Capa: service
- Tipo de bug: validación

## Comportamiento
- Esperado: igual que al crear (`POST /evaluations`), si el periodo del grupo está cerrado se responde `400 El periodo esta cerrado: no se puede modificar el plan de evaluacion`.
- Actual: la evaluación de un periodo cerrado se modifica y se devuelve 200.

## Reproducción (antes del fix)
- Request: `PATCH http://localhost:3001/api/evaluations/6abf0b8bfead57fb41c12ccc`, `Authorization: Bearer <token admin>`, `Content-Type: application/json` (evaluación "Parcial 1" del grupo `6abf0b8bfead57fb41c12c4b`, periodo cerrado)
- Body:
```json
{ "name": "Taller editado BE29" }
```
- Respuesta obtenida: `200` con `"name":"Taller editado BE29"`.

## Causa raíz
`EvaluationsService.update` solo validaba permisos (`assertCanManage`) y notas registradas; faltaba la validación de periodo cerrado que sí tiene `create`.

## Solución
- Cambio aplicado: en `update`, se obtiene el grupo de `assertCanManage`, se carga su periodo y si está `cerrado` se lanza `BadRequestException('El periodo esta cerrado: no se puede modificar el plan de evaluacion')`.
- Verificación: la misma petición devuelve `400` con ese mensaje; editar una evaluación de un grupo del periodo abierto (`6ac3d974f6cb4e89b0cdd950`) sigue devolviendo 200. (El nombre de prueba se restauró a "Parcial 1" en la BD local.)
