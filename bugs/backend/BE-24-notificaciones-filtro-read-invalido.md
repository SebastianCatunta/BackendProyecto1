# BE-24 · El filtro `read` de mis notificaciones acepta cualquier texto y lo trata como `false`

- Área: Backend
- Commit: 383539b

## Ubicación
- Endpoint: GET /api/v1/notifications/mine?read=...
- Funcionalidad: notificaciones
- Archivo y línea(s): src/notifications/dto/notification.dto.ts:27
- Capa: dto/mapper
- Tipo de bug: validación

## Comportamiento
- Esperado: `read` solo admite `true`/`false`; `read=abc` devuelve `400 read must be a boolean value` (como el resto de filtros booleanos).
- Actual: `read=abc` se convierte en `false` y devuelve 200 con las no leídas.

## Reproducción (antes del fix)
- Request: `GET http://localhost:3001/api/v1/notifications/mine?read=abc&limit=1`, `Authorization: Bearer <token de juliana.rios123@universidad.edu>`
- Body:
```json
{}
```
- Respuesta obtenida: `200` con `meta.total = 0` (igual que `read=false`).

## Causa raíz
`NotificationsQueryDto.read` usaba `@Transform(({ value }) => value === 'true' || value === true)`, que convierte cualquier valor distinto de `'true'` en `false` y anula `@IsBoolean`.

## Solución
- Cambio aplicado: `@Transform(toBoolean)` (import de `../../common/dto/query-helpers`).
- Verificación: `read=true` → 1, `read=false` → 0, `read=abc` → `400 read must be a boolean value`.
