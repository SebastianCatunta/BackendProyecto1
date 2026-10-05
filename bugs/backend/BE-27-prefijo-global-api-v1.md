# BE-27 · Prefijo global `/api/v1` en vez de `/api`: las rutas documentadas dan 404

- Área: Backend
- Commit: 7e8a8c5

## Ubicación
- Endpoint: todas las rutas (ej. POST /api/auth/login, GET /api/health)
- Funcionalidad: configuración
- Archivo y línea(s): src/main.ts:10
- Capa: config
- Tipo de bug: otro (ruta base mal configurada)

## Comportamiento
- Esperado: todas las rutas empiezan con `/api`, como indican el README ("API en http://localhost:3000/api"), `scripts/list-endpoints.js` ("todas las rutas empiezan con `/api`", "`POST /api/auth/login`") y la colección Postman del repo (`{{baseUrl}}/api/auth/login`).
- Actual: `POST /api/auth/login` → 404; las rutas solo existen bajo `/api/v1`.

## Reproducción (antes del fix)
- Request: `POST http://localhost:3001/api/auth/login`, `Content-Type: application/json`
- Body:
```json
{ "email": "admin@universidad.edu", "password": "Secret123!" }
```
- Respuesta obtenida: `404 NOT_FOUND`.

## Causa raíz
`app.setGlobalPrefix('api/v1')` en lugar de `app.setGlobalPrefix('api')`.

## Solución
- Cambio aplicado: `app.setGlobalPrefix('api')`.
- Verificación: la misma petición devuelve 200 con `accessToken`; `GET /api/health` 200; Swagger en `/api/docs` 200.
- Nota: los reportes BE-01 a BE-26 muestran URLs con `/api/v1` porque se reprodujeron antes de este fix; con el código corregido la ruta es `/api/...`.
