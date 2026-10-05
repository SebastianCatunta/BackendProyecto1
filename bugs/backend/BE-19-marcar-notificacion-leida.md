# BE-19 · Marcar una notificación como leída no cambia `read`

- Área: Backend
- Commit: [hash corto]

## Ubicación
- Endpoint: PATCH /api/v1/notifications/:id/read
- Funcionalidad: notificaciones
- Archivo y línea(s): src/notifications/notifications.service.ts:69-72
- Capa: service
- Tipo de bug: otro (campo no actualizado)

## Comportamiento
- Esperado: la notificación queda con `read: true` y `readAt`, y el contador `unread` de `GET /notifications/mine` baja.
- Actual: responde 200 con `read: false`; el contador `unread` no cambia.

## Reproducción (antes del fix)
- Request: `PATCH http://localhost:3001/api/v1/notifications/6abf0b8bfead57fb41c12eb9/read`, `Authorization: Bearer <token de juliana.rios123@universidad.edu>`
- Body:
```json
{}
```
- Respuesta obtenida: `200` con `"read":false`; luego `GET /notifications/mine` → `unread: 1`.

## Causa raíz
`markRead` solo asignaba `notification.readAt = new Date()` y guardaba; nunca ponía `notification.read = true`.

## Solución
- Cambio aplicado: se agregó `notification.read = true;` antes de `readAt`.
- Verificación: la misma petición devuelve `"read":true` y `GET /notifications/mine` → `unread: 0`.
