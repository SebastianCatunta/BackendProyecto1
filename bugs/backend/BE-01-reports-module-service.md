# BE-01 · La API no arranca: ReportsService no está registrado en ReportsModule

- Área: Backend
- Commit: 6a9900c

## Ubicación
- Endpoint: todos (la aplicación no inicia); en particular GET /api/v1/reports/*
- Funcionalidad: reportes / arranque de la aplicación
- Archivo y línea(s): src/reports/reports.module.ts:14 y src/reports/reports.module.ts:32
- Capa: config
- Tipo de bug: otro (inyección de dependencias)

## Comportamiento
- Esperado: la aplicación arranca y ReportsController recibe ReportsService por inyección.
- Actual: Nest aborta el arranque con UnknownDependenciesException y no se levanta ningún endpoint.

## Reproducción (antes del fix)
- Request: `npm run start`, luego `POST http://localhost:3001/api/v1/auth/login`
- Body:
```json
{ "email": "admin@universidad.edu", "password": "Secret123!" }
```
- Respuesta obtenida: el proceso no inicia. Log: `Nest can't resolve dependencies of the ReportsController (?). Please make sure that the argument ReportsService at index [0] is available in the ReportsModule module.` Ningún endpoint responde.

## Causa raíz
El `import { ReportsService }` (línea 14) y `providers: [ReportsService]` (línea 32) estaban comentados, así que el módulo declara el controlador sin su servicio.

## Solución
- Cambio aplicado: descomentar el import y `providers: [ReportsService]` en `reports.module.ts`.
- Verificación: `npm run start` termina con "Nest application successfully started" y las rutas `/api/v1/reports/*` quedan mapeadas.
