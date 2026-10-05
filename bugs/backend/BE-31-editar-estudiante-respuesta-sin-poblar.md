# BE-31 · Editar estudiante devuelve `user` y `program` como IDs sin poblar

- Área: Backend
- Commit: f39a3b9

## Ubicación
- Endpoint: PATCH /api/students/:id
- Funcionalidad: estudiantes
- Archivo y línea(s): src/students/students.service.ts:77-79
- Capa: service
- Tipo de bug: mapeo DTO

## Comportamiento
- Esperado: la respuesta tiene la misma forma que `GET /students/:id`: `user: { _id, name, email }` y `program: { _id, code, name }` (igual que `PATCH /teachers/:id`, que devuelve la facultad poblada).
- Actual: devuelve `"user":"6abf0b8bfead57fb41c12ab2"` y `"program":"6abf0b8bfead57fb41c1290c"` (solo IDs); el cliente pierde nombre, correo y programa tras editar.

## Reproducción (antes del fix)
- Request: `PATCH http://localhost:3001/api/students/6abf0b8bfead57fb41c12b84`, `Authorization: Bearer <token admin>`, `Content-Type: application/json`
- Body:
```json
{ "active": true }
```
- Respuesta obtenida: `200` con `"user":"6abf0b8bfead57fb41c12ab2"` y `"program":"6abf0b8bfead57fb41c1290c"`.

## Causa raíz
`StudentsService.update` hacía `findByIdAndUpdate(...).exec()` sin los `populate` que usan `findOne` y `findByUserId`.

## Solución
- Cambio aplicado: se agregaron `.populate('user', 'name email')` y `.populate('program', 'code name')` antes de `.exec()`.
- Verificación: la misma petición devuelve `user` con nombre y correo, y `program` con `code: "ISIS"` y `name`.
