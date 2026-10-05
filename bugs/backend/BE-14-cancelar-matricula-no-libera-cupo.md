# BE-14 · Cancelar una matrícula no libera el cupo del grupo

- Área: Backend
- Commit: 81d2d07

## Ubicación
- Endpoint: POST /api/v1/enrollments/:id/cancel
- Funcionalidad: matrículas
- Archivo y línea(s): src/enrollments/enrollments.service.ts:96-100
- Capa: service
- Tipo de bug: cálculo

## Comportamiento
- Esperado: al cancelar una matrícula activa, `groups.enrolled` del grupo baja en 1 (el endpoint dice "libera el cupo").
- Actual: la matrícula pasa a `cancelada` pero `enrolled` no cambia; el grupo pierde cupos para siempre.

## Reproducción (antes del fix)
- Request: `POST http://localhost:3001/api/v1/enrollments/6ac3d8f476bdeb43c3c6832c/cancel`, `Authorization: Bearer <token admin>`
- Body:
```json
{}
```
- Respuesta obtenida: matrícula `cancelada`; `groups.enrolled` del grupo `6abf0b8bfead57fb41c12c59` antes = 2, después = 2.

## Causa raíz
La transacción de `cancel()` solo guardaba el nuevo estado de la matrícula; faltaba el `$inc: { enrolled: -1 }` del grupo (el inverso del `$inc: 1` que hace `reserveSeat`).

## Solución
- Cambio aplicado: dentro de la misma transacción, `groupModel.updateOne({ _id: enrollment.group }, { $inc: { enrolled: -1 } }, { session })`.
- Verificación: cancelando la otra matrícula activa del grupo (`6ac3d8df6e7b485db8a49529`), `enrolled` pasa de 2 a 1.
