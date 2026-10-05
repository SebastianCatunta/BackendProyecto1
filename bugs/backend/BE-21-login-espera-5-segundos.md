# BE-21 · Todo login tarda 5 segundos, incluso con credenciales correctas

- Área: Backend
- Commit: 37a5cb1

## Ubicación
- Endpoint: POST /api/v1/auth/login
- Funcionalidad: login
- Archivo y línea(s): src/auth/auth.service.ts:18
- Capa: service
- Tipo de bug: otro (rendimiento / lógica de anti fuerza bruta)

## Comportamiento
- Esperado: el freno contra fuerza bruta solo castiga los intentos fallidos; un login correcto responde de inmediato.
- Actual: cada login, correcto o no, espera 5 s antes de comprobar las credenciales.

## Reproducción (antes del fix)
- Request: `POST http://localhost:3001/api/v1/auth/login`, `Content-Type: application/json`
- Body:
```json
{ "email": "admin@universidad.edu", "password": "Secret123!" }
```
- Respuesta obtenida: `200` con `accessToken` en `5.10 s` (`curl -w %{time_total}`).

## Causa raíz
`await this.slowDownAttempts()` (setTimeout de 5000 ms) se ejecutaba al inicio de `login()` para todas las peticiones, en lugar de solo cuando las credenciales son inválidas.

## Solución
- Cambio aplicado: la espera se movió dentro del `if (!user || !valid || !user.active)`, justo antes de lanzar el 401.
- Verificación: la misma petición responde 200 en `0.10 s`; con `"password": "mala"` responde 401 en `5.08 s` (el freno sigue activo para fallos).
