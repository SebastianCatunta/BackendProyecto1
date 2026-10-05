# BE-04 · Los roles (@Roles) no se aplican: cualquier usuario accede a rutas de admin

- Área: Backend
- Commit: 95e4a04

## Ubicación
- Endpoint: todas las rutas con `@Roles(...)` (ej. GET /api/v1/users)
- Funcionalidad: autorización por roles
- Archivo y línea(s): src/auth/auth.module.ts:30-34 (providers)
- Capa: seguridad
- Tipo de bug: auth/roles

## Comportamiento
- Esperado: un estudiante que llama `GET /users` (solo admin) recibe 403 `No tienes permisos para esta accion`.
- Actual: devuelve 200 con la lista de usuarios; `@Roles` no tiene efecto.

## Reproducción (antes del fix)
- Request: `GET http://localhost:3001/api/v1/users?limit=1`, `Authorization: Bearer <token de juliana.rios123@universidad.edu (estudiante)>`
- Body:
```json
{}
```
- Respuesta obtenida: `200 OK` con `data` de usuarios.

## Causa raíz
`RolesGuard` existe pero no está registrado en ningún sitio (ni `APP_GUARD` ni `@UseGuards`), así que la metadata de `@Roles` nunca se evalúa.

## Solución
- Cambio aplicado: se registró `{ provide: APP_GUARD, useClass: RolesGuard }` en `AuthModule`, después de `JwtAuthGuard` (para que `request.user` ya exista).
- Verificación: la misma petición con token de estudiante devuelve `403 FORBIDDEN`; con token de admin devuelve 200.
