# BE-07 · GET /users/me nunca llega a su handler (lo captura `:id`)

- Área: Backend
- Commit: [hash corto]

## Ubicación
- Endpoint: GET /api/v1/users/me
- Funcionalidad: usuarios (perfil propio)
- Archivo y línea(s): src/users/users.controller.ts:40-53
- Capa: controller
- Tipo de bug: otro (orden de rutas)

## Comportamiento
- Esperado: cualquier usuario autenticado obtiene su propio perfil (200).
- Actual: la ruta `GET :id` está declarada antes que `GET me`, así que `me` se toma como ID: el estudiante/docente recibe 403 (ruta solo admin) y el admin recibe 400 `ID invalido`.

## Reproducción (antes del fix)
- Request: `GET http://localhost:3001/api/v1/users/me`, `Authorization: Bearer <token de juliana.rios123@universidad.edu (estudiante)>`
- Body:
```json
{}
```
- Respuesta obtenida: `403 FORBIDDEN` `No tienes permisos para esta accion`.

## Causa raíz
Express resuelve las rutas en orden de declaración; `@Get(':id')` estaba antes de `@Get('me')` (el propio comentario dice que `me` debe ir antes).

## Solución
- Cambio aplicado: se movió el handler `me()` antes de `findOne()` (`:id`).
- Verificación: la misma petición devuelve 200 con el usuario `juliana.rios123@universidad.edu`.
