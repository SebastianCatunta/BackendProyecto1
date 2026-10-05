# BE-16 · Crear evaluación responde 400 aunque la evaluación se crea

- Área: Backend
- Commit: 18eae3f

## Ubicación
- Endpoint: POST /api/v1/evaluations
- Funcionalidad: evaluaciones
- Archivo y línea(s): src/evaluations/evaluations.controller.ts:21
- Capa: controller
- Tipo de bug: código HTTP

## Comportamiento
- Esperado: `201 Created` con la evaluación creada.
- Actual: `400 Bad Request` con la evaluación en el body (sí se guarda).

## Reproducción (antes del fix)
- Request: `POST http://localhost:3001/api/v1/evaluations`, `Authorization: Bearer <token admin>`, `Content-Type: application/json`
- Body:
```json
{ "group": "6abf0b8bfead57fb41c12c59", "name": "Quiz BE16", "weight": 10 }
```
- Respuesta obtenida: `400` con `{"group":"6abf0b8bfead57fb41c12c59","name":"Quiz BE16","weight":10,"_id":"6ac3d9618c0aff08d58e7d07",...}`.

## Causa raíz
El handler `create` tenía `@HttpCode(HttpStatus.BAD_REQUEST)`, que fuerza 400 en la respuesta exitosa.

## Solución
- Cambio aplicado: se eliminó `@HttpCode(HttpStatus.BAD_REQUEST)` (Nest usa 201 en `@Post()`).
- Verificación: la misma petición (otro nombre) devuelve `201` con la evaluación creada.
