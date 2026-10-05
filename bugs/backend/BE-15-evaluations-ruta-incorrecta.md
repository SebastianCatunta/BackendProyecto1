# BE-15 · El módulo de evaluaciones está publicado en /evaluationslalala

- Área: Backend
- Commit: [hash corto]

## Ubicación
- Endpoint: GET/POST /api/v1/evaluations, GET/PATCH /api/v1/evaluations/:id
- Funcionalidad: evaluaciones
- Archivo y línea(s): src/evaluations/evaluations.controller.ts:14
- Capa: controller
- Tipo de bug: otro (ruta mal mapeada)

## Comportamiento
- Esperado: `GET /api/v1/evaluations` lista las evaluaciones (200).
- Actual: `404 Cannot GET /api/v1/evaluations`; las rutas solo existen bajo `/api/v1/evaluationslalala`.

## Reproducción (antes del fix)
- Request: `GET http://localhost:3001/api/v1/evaluations?limit=1`, `Authorization: Bearer <token admin>`
- Body:
```json
{}
```
- Respuesta obtenida: `404 NOT_FOUND`.

## Causa raíz
`@Controller('evaluationslalala')` en lugar de `@Controller('evaluations')` (el `DELETE /evaluations/:id` de DeletionsController sí usa la ruta correcta).

## Solución
- Cambio aplicado: `@Controller('evaluations')`.
- Verificación: la misma petición devuelve 200 con `data` de evaluaciones.
