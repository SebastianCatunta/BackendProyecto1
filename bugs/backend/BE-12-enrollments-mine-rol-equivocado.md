# BE-12 · "Mis matrículas" exige rol docente en vez de estudiante

- Área: Backend
- Commit: [hash corto]

## Ubicación
- Endpoint: GET /api/v1/enrollments/mine
- Funcionalidad: matrículas
- Archivo y línea(s): src/enrollments/enrollments.controller.ts:34
- Capa: controller
- Tipo de bug: auth/roles

## Comportamiento
- Esperado: el estudiante autenticado ve sus matrículas (200). Un docente no tiene matrículas → 403.
- Actual: el estudiante recibe `403 No tienes permisos para esta accion`; solo el docente puede entrar (y falla porque no tiene perfil de estudiante).

## Reproducción (antes del fix)
- Request: `GET http://localhost:3001/api/v1/enrollments/mine?limit=1`, `Authorization: Bearer <token de juliana.rios123@universidad.edu (estudiante)>`
- Body:
```json
{}
```
- Respuesta obtenida: `403 FORBIDDEN`.

## Causa raíz
El handler `mine()` tenía `@Roles(Role.Docente)`; el servicio (`findMine`) busca el perfil de estudiante del usuario, así que el rol correcto es `Estudiante`.

## Solución
- Cambio aplicado: `@Roles(Role.Estudiante)`.
- Verificación: la misma petición devuelve 200 con las matrículas de Juliana Ríos; con token docente devuelve 403.
