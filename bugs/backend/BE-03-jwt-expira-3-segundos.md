# BE-03 · El token JWT expira a los 3 segundos en vez de 1 hora

- Área: Backend
- Commit: [hash corto]

## Ubicación
- Endpoint: POST /api/v1/auth/login (y todas las rutas protegidas)
- Funcionalidad: login / autenticación
- Archivo y línea(s): src/auth/auth.module.ts:21
- Capa: config
- Tipo de bug: otro (unidad de tiempo en la expiración del token)

## Comportamiento
- Esperado: el token dura `JWT_EXPIRES_IN_SECONDS` segundos (3600 = 1 hora): `exp - iat = 3600`.
- Actual: `exp - iat = 3`; a los 3 segundos cualquier petición con el token devuelve 401.

## Reproducción (antes del fix)
- Request: `POST http://localhost:3001/api/v1/auth/login`, `Content-Type: application/json`; luego, 4 s después, `GET http://localhost:3001/api/v1/auth/me` con `Authorization: Bearer <token>`
- Body:
```json
{ "email": "admin@universidad.edu", "password": "Secret123!" }
```
- Respuesta obtenida: payload del token con `exp - iat = 3`; `GET /auth/me` → `401 UNAUTHORIZED`.

## Causa raíz
`expiresIn` se pasaba como `String(3600)` = `"3600"`. jsonwebtoken interpreta un string numérico sin unidad como milisegundos (librería `ms`), así que 3600 ms ≈ 3 s.

## Solución
- Cambio aplicado: `expiresIn: Number(config.getOrThrow<number>('JWT_EXPIRES_IN_SECONDS'))` (número = segundos).
- Verificación: la misma petición devuelve un token con `exp - iat = 3600`; `GET /auth/me` 4 s después devuelve 200 con los datos del usuario.
