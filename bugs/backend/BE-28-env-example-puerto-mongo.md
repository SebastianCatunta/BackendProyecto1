# BE-28 · `.env.example` apunta MongoDB al puerto 27018, pero Docker expone 27017

- Área: Backend
- Commit: f24f3d2

## Ubicación
- Endpoint: arranque de la API (conexión a MongoDB; afecta a todas las rutas)
- Funcionalidad: configuración
- Archivo y línea(s): .env.example:2
- Capa: config
- Tipo de bug: otro (puerto de la base de datos)

## Comportamiento
- Esperado: al copiar `.env.example` a `.env` (como indica el README) la API se conecta a la MongoDB de `docker-compose.yml`, que publica `27017:27017` y arranca `mongod --port 27017` (el replica set también usa `localhost:27017`).
- Actual: `MONGODB_URI` usa `localhost:27018`, donde no escucha nada; la API no logra conectarse a la BD.

## Reproducción (antes del fix)
- Request: conectar con el `MONGODB_URI` de `.env.example` (`mongodb://localhost:27018/universidad?replicaSet=rs0&directConnection=true`) usando el driver `mongodb` con `serverSelectionTimeoutMS: 3000`, con `npm run db:up` levantado.
- Body:
```json
{}
```
- Respuesta obtenida: `MongoServerSelectionError` (no hay servidor en 27018).

## Causa raíz
En `.env.example` el puerto de `MONGODB_URI` se cambió de 27017 a 27018, distinto del que publica `docker-compose.yml` (en el primer commit del repo era 27017).

## Solución
- Cambio aplicado: `MONGODB_URI=mongodb://localhost:27017/universidad?replicaSet=rs0&directConnection=true`.
- Verificación: la misma conexión con el URI de `.env.example` responde `OK`.
