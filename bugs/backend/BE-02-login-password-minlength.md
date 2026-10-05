# BE-02 · Login rechaza contraseñas válidas por exigir mínimo 12 caracteres

- Área: Backend
- Commit: PENDIENTE

## Ubicación
- Endpoint: POST /api/v1/auth/login
- Funcionalidad: login
- Archivo y línea(s): src/auth/dto/login.dto.ts:12 (y el import en la línea 2)
- Capa: dto/mapper
- Tipo de bug: validación

## Comportamiento
- Esperado: el login acepta las credenciales de los usuarios existentes (clave de prueba `Secret123!`, 10 caracteres) y devuelve 200 con `accessToken`. Una clave incorrecta devuelve 401.
- Actual: devuelve 400 por validación de longitud antes de comprobar las credenciales; nadie con una clave de menos de 12 caracteres puede iniciar sesión.

## Reproducción (antes del fix)
- Request: `POST http://localhost:3001/api/v1/auth/login`, `Content-Type: application/json`
- Body:
```json
{ "email": "admin@universidad.edu", "password": "Secret123!" }
```
- Respuesta obtenida: `400 BAD_REQUEST`, `"password must be longer than or equal to 12 characters"`.

## Causa raíz
`LoginDto` tenía `@MinLength(12)` en `password`. El login no debe imponer una longitud mínima (eso es de creación y cambio de clave, que usan 8), y las claves existentes y el ejemplo de Swagger (`Admin12345`) tienen 10 caracteres.

## Solución
- Cambio aplicado: se eliminó `@MinLength(12)` y el import `MinLength` de `login.dto.ts`.
- Verificación: la misma petición devuelve 200 con `accessToken`; con `"password": "mala"` devuelve 401 `Credenciales invalidas`.
