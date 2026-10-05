# BE-09 · Cambiar contraseña responde OK pero no guarda la nueva clave

- Área: Backend
- Commit: 0763a56

## Ubicación
- Endpoint: PATCH /api/v1/auth/change-password
- Funcionalidad: login / cambio de contraseña
- Archivo y línea(s): src/users/users.service.ts:135
- Capa: service
- Tipo de bug: otro (cambio no persistido)

## Comportamiento
- Esperado: tras el cambio, el login funciona con la clave nueva y la antigua devuelve 401.
- Actual: devuelve 200 con token nuevo, pero la clave nueva da 401 y la antigua sigue funcionando.

## Reproducción (antes del fix)
- Request: login con `prueba.be05b@universidad.edu` / `Clave12345`; luego `PATCH http://localhost:3001/api/v1/auth/change-password`, `Authorization: Bearer <token>`, `Content-Type: application/json`; luego `POST /auth/login` con `Nueva12345`.
- Body:
```json
{ "currentPassword": "Clave12345", "newPassword": "Nueva12345" }
```
- Respuesta obtenida: change-password `200`; login con `Nueva12345` → `401 Credenciales invalidas`; login con `Clave12345` → 200.

## Causa raíz
`UsersService.changePassword` asignaba `passwordHash` y `passwordChangedAt` al documento pero hacía `return user;` sin `save()`, así que nada se escribía en MongoDB.

## Solución
- Cambio aplicado: `return user.save();`
- Verificación: mismo flujo → change-password 200, login con `Nueva12345` 200, login con `Clave12345` 401.
