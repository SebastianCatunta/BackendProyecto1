# BE-13 · Matricular responde 400 "No se pudo confirmar la matricula" aunque se crea

- Área: Backend
- Commit: 23b06a7

## Ubicación
- Endpoint: POST /api/v1/enrollments
- Funcionalidad: matrículas
- Archivo y línea(s): src/enrollments/enrollments.service.ts:79
- Capa: service
- Tipo de bug: operador/comparación

## Comportamiento
- Esperado: `201` con la matrícula en estado `activa`.
- Actual: `400 No se pudo confirmar la matricula`, pero la matrícula queda creada (`activa`) y el cupo del grupo se consume; el cliente cree que falló.

## Reproducción (antes del fix)
- Request: `POST http://localhost:3001/api/v1/enrollments`, `Authorization: Bearer <token admin>`, `Content-Type: application/json`
- Body:
```json
{ "groupId": "6abf0b8bfead57fb41c12c59", "student": "6abf0b8bfead57fb41c12b6f" }
```
- Respuesta obtenida: `400 BAD_REQUEST "No se pudo confirmar la matricula"`; en Mongo la matrícula existe con `status: "activa"` y `groups.enrolled` pasó de 0 a 1.
- Nota de entorno: para poder probar se cambió solo en la BD local el periodo 2026-2 de `"Abierto"` a `"abierto"` (bug de datos en `database/periods.json`, no corregido aquí).

## Causa raíz
La verificación final estaba invertida: `if (created.status === EnrollmentStatus.Active) throw ...` lanza el error justamente cuando la matrícula sí quedó activa.

## Solución
- Cambio aplicado: `if (created.status !== EnrollmentStatus.Active)`.
- Verificación: la misma petición (con el estudiante `6abf0b8bfead57fb41c12b70`) devuelve `201` con `"status":"activa"`.
