# BE-22 · Cancelar matrícula responde 201 Created en vez de 200 OK

- Área: Backend
- Commit: [hash corto]

## Ubicación
- Endpoint: POST /api/v1/enrollments/:id/cancel
- Funcionalidad: matrículas
- Archivo y línea(s): src/enrollments/enrollments.controller.ts:49 (y el import de la línea 1)
- Capa: controller
- Tipo de bug: código HTTP

## Comportamiento
- Esperado: `200 OK`; la acción no crea ningún recurso, solo cambia el estado de una matrícula existente (igual que `POST /periods/:id/close`, `POST /grades/finalize/:id` o `POST /groups/:id/finalize`, que responden 200).
- Actual: `201 Created`.

## Reproducción (antes del fix)
- Request: `POST http://localhost:3001/api/v1/enrollments/6ac3d8f476bdeb43c3c6832c/cancel`, `Authorization: Bearer <token admin>` (matrícula activa)
- Body:
```json
{}
```
- Respuesta obtenida: `201` con la matrícula en estado `cancelada`.

## Causa raíz
Faltaba `@HttpCode(200)` en el handler `cancel`; Nest responde 201 por defecto en `@Post()`.

## Solución
- Cambio aplicado: se agregó `@HttpCode(200)` (e `HttpCode` al import de `@nestjs/common`).
- Verificación: tras reactivar la matrícula, la misma petición devuelve `200`.
