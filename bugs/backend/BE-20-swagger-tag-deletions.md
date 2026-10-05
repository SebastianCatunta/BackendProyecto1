# BE-20 · Los endpoints DELETE aparecen en Swagger bajo la etiqueta "deletions21312"

- Área: Backend
- Commit: 98e284f

## Ubicación
- Endpoint: todos los DELETE de DeletionsController (ej. DELETE /api/v1/groups/:id) en la documentación Swagger (`/api/doc`)
- Funcionalidad: eliminaciones / documentación de la API
- Archivo y línea(s): src/deletions/deletions.controller.ts:10
- Capa: controller
- Tipo de bug: otro (metadata Swagger)

## Comportamiento
- Esperado: los endpoints de borrado se agrupan en Swagger bajo la etiqueta `deletions` (como `users`, `groups`, `evaluations`...).
- Actual: aparecen bajo la etiqueta `deletions21312`.

## Reproducción (antes del fix)
- Request: `GET http://localhost:3001/api/doc-json` y leer `paths["/api/v1/groups/{id}"].delete.tags`
- Body:
```json
{}
```
- Respuesta obtenida: `["deletions21312"]`.

## Causa raíz
`@ApiTags('deletions21312')` tenía texto basura añadido al nombre de la etiqueta.

## Solución
- Cambio aplicado: `@ApiTags('deletions')`.
- Verificación: la misma petición devuelve `["deletions"]`.
