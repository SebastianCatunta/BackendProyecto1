# BE-11 · Un docente puede gestionar grupos que no están a su cargo

- Área: Backend
- Commit: [hash corto]

## Ubicación
- Endpoint: GET /api/v1/groups/:id/roster (y todo lo que usa `assertCanManage`: grade-sheet, finalize, notas, evaluaciones, borrado de notas/evaluaciones)
- Funcionalidad: grupos / notas
- Archivo y línea(s): src/groups/groups.service.ts:98
- Capa: service
- Tipo de bug: auth/roles

## Comportamiento
- Esperado: un docente solo gestiona sus grupos; con un grupo de otro docente recibe 403 `El grupo no esta a tu cargo`. El admin gestiona cualquiera.
- Actual: el docente obtiene 200 con la nómina de un grupo ajeno.

## Reproducción (antes del fix)
- Request: `GET http://localhost:3001/api/v1/groups/6abf0b8bfead57fb41c12c3d/roster`, `Authorization: Bearer <token de juliana.mendoza34@universidad.edu (docente, teacher 6abf0b8bfead57fb41c12b2b)>` — el grupo pertenece al teacher `6abf0b8bfead57fb41c12b60`.
- Body:
```json
{}
```
- Respuesta obtenida: `200` con la nómina del grupo ODON105.

## Causa raíz
`assertCanManage` verificaba la propiedad del grupo cuando `user.role === Role.Estudiante` en lugar de `Role.Docente`, así que para un docente nunca se comprobaba.

## Solución
- Cambio aplicado: la condición pasa a `user.role === Role.Docente`.
- Verificación: la misma petición devuelve `403 El grupo no esta a tu cargo`; con un grupo propio (`6abf0b8bfead57fb41c12c6c`) 200; con token admin 200.
