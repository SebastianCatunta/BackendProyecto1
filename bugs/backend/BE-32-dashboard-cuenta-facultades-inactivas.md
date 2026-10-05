# BE-32 · El tablero cuenta también las facultades inactivas

- Área: Backend
- Commit: 35d36b7

## Ubicación
- Endpoint: GET /api/reports/dashboard
- Funcionalidad: reportes
- Archivo y línea(s): src/reports/reports.service.ts:44
- Capa: service
- Tipo de bug: query

## Comportamiento
- Esperado: el tablero cuenta solo registros activos, igual que estudiantes, docentes, programas, materias, salones y grupos (todos con `{ active: true }`); con una facultad desactivada, `faculties` baja de 10 a 9.
- Actual: `faculties` sigue en 10 aunque haya una facultad inactiva.

## Reproducción (antes del fix)
- Request: `PATCH http://localhost:3001/api/faculties/6abf0b8bfead57fb41c12b03` con `{ "active": false }` y luego `GET http://localhost:3001/api/reports/dashboard`, `Authorization: Bearer <token admin>`
- Body:
```json
{ "active": false }
```
- Respuesta obtenida: dashboard `200` con `"faculties": 10` (hay 10 facultades, 1 inactiva).

## Causa raíz
`dashboard()` usaba `facultyModel.countDocuments()` sin filtro, a diferencia de los demás conteos, que usan `{ active: true }`.

## Solución
- Cambio aplicado: `this.facultyModel.countDocuments({ active: true })`.
- Verificación: con la facultad desactivada el tablero devuelve `"faculties": 9`; al reactivarla vuelve a 10 (la facultad se dejó activa otra vez).
