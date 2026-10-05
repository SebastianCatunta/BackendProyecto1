# BE-25 · La API ignora la variable PORT y escucha siempre en 3001

- Área: Backend
- Commit: 8f45cf7

## Ubicación
- Endpoint: arranque de la API (todas las rutas)
- Funcionalidad: configuración
- Archivo y línea(s): src/main.ts:28
- Capa: config
- Tipo de bug: otro (clave de configuración y puerto por defecto erróneos)

## Comportamiento
- Esperado: la API escucha en `PORT` (variable validada en `env.validation.ts`, definida en `.env.example` como 3000; por defecto 3000, como dicen el README, `scripts/list-endpoints.js` y la colección Postman del repo). El frontend usa el 3001.
- Actual: lee una variable inexistente `APP_PORT` y cae siempre en 3001 (el puerto del frontend); `PORT` no tiene efecto.

## Reproducción (antes del fix)
- Request: `PORT=3005 node dist/main.js` y luego `GET http://localhost:3005/api/v1/health`
- Body:
```json
{}
```
- Respuesta obtenida: el proceso intenta escuchar en 3001 (`EADDRINUSE: address already in use :::3001`) y `localhost:3005` no responde.

## Causa raíz
`const port = Number(process.env.APP_PORT ?? 3001);` usa una clave que no existe en la configuración y un valor por defecto incorrecto.

## Solución
- Cambio aplicado: `const port = Number(process.env.PORT ?? 3000);`
- Verificación: `PORT=3005 node dist/main.js` → `GET localhost:3005/.../health` 200. En la máquina local (puerto 3000 ocupado por otra app) se usa `PORT=3001` en el `.env` local y la API sigue en 3001.
