# BE-23 · El filtro `active` de usuarios acepta cualquier texto y lo trata como `false`

- Área: Backend
- Commit: cda6b47

## Ubicación
- Endpoint: GET /api/v1/users?active=...
- Funcionalidad: usuarios (listado)
- Archivo y línea(s): src/users/dto/user.dto.ts:56
- Capa: dto/mapper
- Tipo de bug: validación

## Comportamiento
- Esperado: `active` solo admite `true`/`false`; un valor inválido (`abc`) devuelve `400 active must be a boolean value`, como en students, teachers, groups, subjects y programs.
- Actual: `active=abc` se convierte en `false` y devuelve 200 con los usuarios inactivos (4).

## Reproducción (antes del fix)
- Request: `GET http://localhost:3001/api/v1/users?active=abc&limit=1`, `Authorization: Bearer <token admin>`
- Body:
```json
{}
```
- Respuesta obtenida: `200` con `meta.total = 4` (mismo resultado que `active=false`).

## Causa raíz
`UsersQueryDto.active` usaba `@Transform(({ value }) => value === 'true' || value === true)`, que convierte todo lo que no sea `'true'` en `false`, así `@IsBoolean` nunca falla. El resto de DTOs usa el helper `toBoolean`, que deja los valores inválidos sin convertir para que `@IsBoolean` los rechace.

## Solución
- Cambio aplicado: `@Transform(toBoolean)` (import de `../../common/dto/query-helpers`).
- Verificación: `active=true` → 199, `active=false` → 4, `active=abc` → `400 active must be a boolean value`.
