# BE-06 · Editar usuario rechaza el campo `name` (DTO con nombre de campo erróneo)

- Área: Backend
- Commit: [hash corto]

## Ubicación
- Endpoint: PATCH /api/v1/users/:id
- Funcionalidad: usuarios
- Archivo y línea(s): src/users/dto/user.dto.ts:14
- Capa: dto/mapper
- Tipo de bug: mapeo DTO

## Comportamiento
- Esperado: el admin puede cambiar el nombre de un usuario enviando `{ "name": "..." }` → 200 con el usuario actualizado.
- Actual: `400 BAD_REQUEST` `property name should not exist`.

## Reproducción (antes del fix)
- Request: `PATCH http://localhost:3001/api/v1/users/6ac3d74697eedd4177fad8f8`, `Authorization: Bearer <token admin>`, `Content-Type: application/json`
- Body:
```json
{ "name": "Nombre Editado" }
```
- Respuesta obtenida: `400` `["property name should not exist"]`.

## Causa raíz
En `UpdateUserDto` la propiedad se llamaba `namesssss` en vez de `name`; con `forbidNonWhitelisted` el campo real `name` se rechaza.

## Solución
- Cambio aplicado: se renombró la propiedad a `name?: string`.
- Verificación: la misma petición devuelve 200 con `"name":"Nombre Editado"`.
