# BE-08 · GET /groups/mine devuelve 400 "ID invalido" (lo captura `:id`)

- Área: Backend
- Commit: fc820dd

## Ubicación
- Endpoint: GET /api/v1/groups/mine
- Funcionalidad: grupos (mis grupos del docente)
- Archivo y línea(s): src/groups/groups.controller.ts:31-43
- Capa: controller
- Tipo de bug: otro (orden de rutas)

## Comportamiento
- Esperado: el docente autenticado obtiene la lista paginada de sus grupos (200).
- Actual: `400 BAD_REQUEST` `ID invalido`, porque `mine` se procesa como `:id`.

## Reproducción (antes del fix)
- Request: `GET http://localhost:3001/api/v1/groups/mine?limit=1`, `Authorization: Bearer <token de juliana.mendoza34@universidad.edu (docente)>`
- Body:
```json
{}
```
- Respuesta obtenida: `400` `ID invalido`.

## Causa raíz
`@Get(':id')` estaba declarado antes de `@Get('mine')`; Express resuelve en orden de declaración y `ParseObjectIdPipe` rechaza `mine`.

## Solución
- Cambio aplicado: se movió el handler `mine()` antes de `findOne()` (`:id`).
- Verificación: la misma petición devuelve 200 con `data` de los grupos del docente.
