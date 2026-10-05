# BE-30 · El filtro `campus` de facultades distingue mayúsculas y exige texto exacto

- Área: Backend
- Commit: 991946c

## Ubicación
- Endpoint: GET /api/faculties?campus=...
- Funcionalidad: facultades (listado)
- Archivo y línea(s): src/faculties/faculties.service.ts:28
- Capa: service
- Tipo de bug: query

## Comportamiento
- Esperado: como el resto de filtros de texto del sistema (`textPattern`: sin distinguir mayúsculas), `campus=bogotá`, `Bogotá` y `BOGOTÁ` devuelven las mismas facultades.
- Actual: `campus=Bogotá` → 4, `campus=bogotá` → 0, `campus=BOGOTÁ` → 0.

## Reproducción (antes del fix)
- Request: `GET http://localhost:3001/api/faculties?campus=bogot%C3%A1&limit=1`, `Authorization: Bearer <token admin>`
- Body:
```json
{}
```
- Respuesta obtenida: `200` con `meta.total = 0` (con `Bogotá` el total es 4).

## Causa raíz
El filtro usaba igualdad exacta `{ campus: query.campus }` en lugar del helper `textPattern`, que usan programs, subjects, students y teachers.

## Solución
- Cambio aplicado: `{ campus: textPattern(query.campus) }` (import de `../common/dto/query-helpers`).
- Verificación: `Bogotá`, `bogotá` y `BOGOTÁ` → 5; `Medellín` → 3. (Ahora también aparece la facultad guardada como `"Bogotá "` con espacio final, un error de datos aparte.)
