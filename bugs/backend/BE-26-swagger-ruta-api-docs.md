# BE-26 · La documentación Swagger no está en /api/docs (404)

- Área: Backend
- Commit: 09bbe31

## Ubicación
- Endpoint: GET /api/docs (Swagger UI)
- Funcionalidad: documentación de la API
- Archivo y línea(s): src/main.ts:26
- Capa: config
- Tipo de bug: otro (ruta mal configurada)

## Comportamiento
- Esperado: Swagger UI en `/api/docs`, como indican el README, `scripts/list-endpoints.js` ("Documentacion interactiva: `/api/docs`").
- Actual: `GET /api/docs` → 404; Swagger quedó publicado en `/api/doc`.

## Reproducción (antes del fix)
- Request: `GET http://localhost:3001/api/docs`
- Body:
```json
{}
```
- Respuesta obtenida: `404 NOT_FOUND`.

## Causa raíz
`SwaggerModule.setup('api/doc', ...)` en lugar de `'api/docs'`.

## Solución
- Cambio aplicado: `SwaggerModule.setup('api/docs', app, ...)`.
- Verificación: `GET http://localhost:3001/api/docs` → 200 (Swagger UI).
