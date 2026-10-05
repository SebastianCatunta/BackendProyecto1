# BE-05 · Crear usuario responde 400 aunque el usuario se crea

- Área: Backend
- Commit: [hash corto]

## Ubicación
- Endpoint: POST /api/v1/users
- Funcionalidad: usuarios
- Archivo y línea(s): src/users/users.controller.ts:28
- Capa: controller
- Tipo de bug: código HTTP

## Comportamiento
- Esperado: `201 Created` con `{ id, name, email, role }`.
- Actual: `400 Bad Request` con el usuario en el body (sí se guarda en la BD); el cliente lo interpreta como error.

## Reproducción (antes del fix)
- Request: `POST http://localhost:3001/api/v1/users`, `Authorization: Bearer <token admin>`, `Content-Type: application/json`
- Body:
```json
{ "name": "Prueba BE05", "email": "prueba.be05@universidad.edu", "password": "Clave12345" }
```
- Respuesta obtenida: `400` con `{"id":"...","name":"Prueba BE05","email":"prueba.be05@universidad.edu","role":"estudiante"}`.

## Causa raíz
El método `create` tenía `@HttpCode(400)`, que fuerza el status de la respuesta exitosa a 400.

## Solución
- Cambio aplicado: se eliminó `@HttpCode(400)`; Nest usa 201 por defecto en `@Post()`.
- Verificación: la misma petición (con otro correo) devuelve `201` con el usuario creado. Un correo repetido sigue dando 409.
