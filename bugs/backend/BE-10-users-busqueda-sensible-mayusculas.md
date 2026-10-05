# BE-10 · La búsqueda de usuarios (q) distingue mayúsculas/minúsculas

- Área: Backend
- Commit: [hash corto]

## Ubicación
- Endpoint: GET /api/v1/users?q=...
- Funcionalidad: usuarios (listado / búsqueda)
- Archivo y línea(s): src/users/users.service.ts:55
- Capa: service
- Tipo de bug: query

## Comportamiento
- Esperado: `q` busca en nombre y correo sin importar mayúsculas (igual que el resto de búsquedas del sistema): `Rivera`, `rivera` y `RIVERA` devuelven los mismos 10 usuarios.
- Actual: `Rivera` → 10, `rivera` → 4 (solo coincidencias en el correo), `RIVERA` → 0.

## Reproducción (antes del fix)
- Request: `GET http://localhost:3001/api/v1/users?q=RIVERA&limit=3`, `Authorization: Bearer <token admin>`
- Body:
```json
{}
```
- Respuesta obtenida: `200` con `meta.total = 0` (con `q=Rivera` el total es 10).

## Causa raíz
La `RegExp` del filtro se construía sin la bandera `'i'` (a diferencia de `findIdsByText` y `textPattern`, que sí la usan).

## Solución
- Cambio aplicado: `new RegExp(escapeRegex(query.q.trim()), 'i')`.
- Verificación: `q=Rivera`, `q=rivera` y `q=RIVERA` devuelven `meta.total = 10`.
