# BE-17 · No se puede registrar una nota de 5.0 (máximo validado en 4.5)

- Área: Backend
- Commit: [hash corto]

## Ubicación
- Endpoint: PUT /api/v1/grades (y PUT /api/v1/grades/bulk)
- Funcionalidad: notas
- Archivo y línea(s): src/grades/dto/grade.dto.ts:18
- Capa: dto/mapper
- Tipo de bug: validación

## Comportamiento
- Esperado: la escala es 0.0 – 5.0 (lo dice el propio `@ApiProperty`: `maximum: 5`); una nota de 5 se guarda (200). Más de 5 → 400.
- Actual: `400 value must not be greater than 4.5`.

## Reproducción (antes del fix)
- Request: `PUT http://localhost:3001/api/v1/grades`, `Authorization: Bearer <token admin>`, `Content-Type: application/json`
- Body:
```json
{ "enrollment": "6ac3d98df6cb4e89b0cdd965", "evaluation": "6ac3d9618c0aff08d58e7d07", "value": 5 }
```
- Respuesta obtenida: `400 BAD_REQUEST ["value must not be greater than 4.5"]`.

## Causa raíz
`UpsertGradeDto.value` tenía `@Max(4.5)` en lugar de `@Max(5)`.

## Solución
- Cambio aplicado: `@Max(5)`.
- Verificación: la misma petición devuelve 200 con la nota guardada; con `"value": 5.1` devuelve `400 value must not be greater than 5`.
