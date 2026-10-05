# BE-28 · CORS no está habilitado: el frontend (otro origen) no puede llamar a la API

- Área: Backend
- Commit: [hash corto]

## Ubicación
- Endpoint: todas las rutas (preflight `OPTIONS`)
- Funcionalidad: configuración / integración con el frontend
- Archivo y línea(s): src/main.ts:10-11
- Capa: config
- Tipo de bug: otro (CORS)

## Comportamiento
- Esperado: el frontend corre en otro origen (README: frontend en `http://localhost:3001`, API en `:3000`), así que el preflight CORS debe responder 204 con `Access-Control-Allow-Origin`, y el navegador debe permitir las peticiones con `Authorization`.
- Actual: `OPTIONS` devuelve 404 sin cabeceras CORS; el navegador bloquea todas las llamadas del frontend.

## Reproducción (antes del fix)
- Request: `OPTIONS http://localhost:3001/api/auth/login`, headers `Origin: http://localhost:3001`, `Access-Control-Request-Method: POST`, `Access-Control-Request-Headers: content-type,authorization`
- Body:
```json
{}
```
- Respuesta obtenida: `404 Cannot OPTIONS /api/auth/login`, sin `Access-Control-Allow-Origin`.

## Causa raíz
`main.ts` no llamaba a `app.enableCors()`, así que Express no responde al preflight ni agrega las cabeceras CORS.

## Solución
- Cambio aplicado: `app.enableCors();` después de `setGlobalPrefix`.
- Verificación: la misma petición devuelve `204` con `Access-Control-Allow-Origin: *`, `Access-Control-Allow-Methods: GET,HEAD,PUT,PATCH,POST,DELETE` y `Access-Control-Allow-Headers: content-type,authorization`.
