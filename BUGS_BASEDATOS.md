# Bugs Base de Datos

Datos del seed (`database/*.json`, los que carga `npm run db:import`). Diagnóstico estático con la skill `mongodb-bug-fixer` (severidad y categoría según su guía). **No se ejecutó ninguna escritura sobre la BD en vivo**: para ver los arreglos en la app hay que reimportar con `npm run db:import`.

## Bug #1 — Rol con mayúscula: "Docente"
- **Archivo:** `database/users.json`
- **Severidad / categoría:** high / invalid-data
- **Problema:** Laura López tenía `role: "Docente"`; el enum del schema es `admin|docente|estudiante`, así que el guard de roles nunca la reconocía como docente.
- **Antes:** `"role":"Docente"`
- **Después:** `"role":"docente"`
- **Cómo verificar:** Tras `npm run db:import`, iniciar sesión como laura.lopez89@universidad.edu: entra a /docente.

## Bug #2 — Correo con mayúsculas (no se podía iniciar sesión)
- **Archivo:** `database/users.json`
- **Severidad / categoría:** high / invalid-data
- **Problema:** `Laura.Lopez89@universidad.edu` estaba guardado con mayúsculas; el schema usa `lowercase: true` y el login busca en minúsculas, así que nunca encontraba al usuario ("Credenciales invalidas").
- **Antes:** `"email":"Laura.Lopez89@universidad.edu"`
- **Después:** `"email":"laura.lopez89@universidad.edu"`
- **Cómo verificar:** Tras `npm run db:import`, login con laura.lopez89@universidad.edu / Secret123! responde 200.

## Bug #3 — Usuario docente de prueba inactivo
- **Archivo:** `database/users.json`
- **Severidad / categoría:** medium / invalid-data
- **Problema:** El README presenta a Laura López como docente de prueba, pero su usuario tenía `active: false`.
- **Antes:** `"active":false`
- **Después:** `"active":true`
- **Cómo verificar:** Tras `npm run db:import`, iniciar sesión como Laura: no aparece "usuario inactivo".

## Bug #4 — Hash de contraseña corrupto (juliana.herrera147)
- **Archivo:** `database/users.json`
- **Severidad / categoría:** high / invalid-data
- **Problema:** Su `passwordHash` medía 59 caracteres (un bcrypt válido mide 60), así que bcrypt nunca validaba la clave y la estudiante de prueba no podía entrar. Los otros 200 usuarios comparten el hash de `Secret123!`.
- **Antes:** hash de 59 caracteres
- **Después:** hash bcrypt de `Secret123!` (60 caracteres, el mismo que el resto)
- **Cómo verificar:** Tras `npm run db:import`, login con juliana.herrera147@universidad.edu / Secret123! responde 200.

## Bug #5 — Administrador sin nombre
- **Archivo:** `database/users.json`
- **Severidad / categoría:** low / missing-field
- **Problema:** El usuario admin tenía `name` vacío; el menú lateral y "Mi cuenta" mostraban un nombre en blanco y el avatar con "?".
- **Antes:** `"name":""`
- **Después:** `"name":"Administrador"`
- **Cómo verificar:** Tras `npm run db:import`, entrar como admin: abajo del menú dice "Administrador" con avatar "A".

## Bug #6 — Matrícula duplicada (mismo estudiante y grupo)
- **Archivo:** `database/enrollments.json`
- **Severidad / categoría:** high / duplicate-data
- **Problema:** La matrícula `6ac057b2…f3c2` repetía estudiante + grupo de `…dfb`. Viola el índice único `{student, group}` del schema y duplicaba la materia en "Mis materias".
- **Antes:** 2 matrículas de E20210046 en el grupo `…c3e`
- **Después:** se elimina el duplicado `…f3c2` y se conserva la original `…dfb`
- **Cómo verificar:** Tras `npm run db:import`, no hay error de índice duplicado y la materia aparece una sola vez.

## Bug #7 — Matrícula con materia distinta a la de su grupo
- **Archivo:** `database/enrollments.json`
- **Severidad / categoría:** medium / inconsistent-denormalized-data
- **Problema:** La matrícula `…dfb` apuntaba a la materia `…9c0`, pero su grupo es de `…99d`. Historial y notas mostraban otra materia.
- **Antes:** `subject` = `…9c0`
- **Después:** `subject` = `…99d` (la del grupo)
- **Cómo verificar:** Tras `npm run db:import`, en "Mis materias" de E20210046 la materia coincide con la del grupo.

## Bug #8 — Matrícula en un periodo distinto al de su grupo
- **Archivo:** `database/enrollments.json`
- **Severidad / categoría:** medium / inconsistent-denormalized-data
- **Problema:** La matrícula `…e1a` tenía el periodo `…a34` (cerrado), pero su grupo es del periodo `…a35` (2026-2, abierto). Quedaba "activa" en un periodo cerrado.
- **Antes:** `period` = `…a34`
- **Después:** `period` = `…a35`
- **Cómo verificar:** Tras `npm run db:import`, la matrícula aparece en el periodo 2026-2 y se puede cancelar.

## Bug #9 — Matrícula "activa" con nota final en periodo cerrado
- **Archivo:** `database/enrollments.json`
- **Severidad / categoría:** medium / invalid-data
- **Problema:** La matrícula `…d25` tenía `finalGrade: 3.38` y estado `activa` en un periodo cerrado. Con nota ≥ 3.0 debe estar aprobada.
- **Antes:** `"status":"activa"`
- **Después:** `"status":"aprobada"`
- **Cómo verificar:** Tras `npm run db:import`, en el historial del estudiante esa materia aparece "Aprobada" con 3.4.

## Bug #10 — Contador `enrolled` inflado (grupo …c3a)
- **Archivo:** `database/groups.json`
- **Severidad / categoría:** high / inconsistent-denormalized-data
- **Problema:** `enrolled` decía 35 con capacidad 32 (sobrecupo), pero el grupo tiene 9 matrículas no canceladas. `availableSeats` daba 0 y nadie podía matricularse.
- **Antes:** `"enrolled":35`
- **Después:** `"enrolled":9`
- **Cómo verificar:** Tras `npm run db:import`, en "Matricular" el grupo muestra 23 cupos.

## Bug #11 — Contador `enrolled` inflado (grupo …c3e)
- **Archivo:** `database/groups.json`
- **Severidad / categoría:** high / inconsistent-denormalized-data
- **Problema:** `enrolled` decía 42 con capacidad 39; las matrículas reales (sin el duplicado del #6) son 9.
- **Antes:** `"enrolled":42`
- **Después:** `"enrolled":9`
- **Cómo verificar:** Tras `npm run db:import`, el grupo muestra 9 / 39 en Grupos (admin).

## Bug #12 — Día del horario con acento y mayúscula
- **Archivo:** `database/groups.json`
- **Severidad / categoría:** medium / invalid-data
- **Problema:** Una franja del grupo `…c3a` tenía `day: "Miércoles"`; el enum es `miercoles`, así que la clase no aparecía en el horario.
- **Antes:** `"day":"Miércoles"`
- **Después:** `"day":"miercoles"`
- **Cómo verificar:** Tras `npm run db:import`, en "Horario" la clase aparece en la tarjeta Miércoles.

## Bug #13 — Franja con hora de inicio mayor que la de fin
- **Archivo:** `database/groups.json`
- **Severidad / categoría:** medium / invalid-data
- **Problema:** El grupo `…c64` tenía el jueves de 09:00 a 07:00.
- **Antes:** `"startTime":"09:00","endTime":"07:00"`
- **Después:** `"startTime":"07:00","endTime":"09:00"`
- **Cómo verificar:** Tras `npm run db:import`, el horario muestra Jueves 07:00 – 09:00.

## Bug #14 — Nota fuera de rango 5.7 (…df0)
- **Archivo:** `database/grades.json`
- **Severidad / categoría:** medium / invalid-data
- **Problema:** La escala es 0–5 (`min: 0, max: 5` en el schema). Se ajusta al máximo válido; **confirmar el valor real con el docente**.
- **Antes:** `"value":5.7`
- **Después:** `"value":5`
- **Cómo verificar:** Tras `npm run db:import`, la planilla del grupo muestra 5.0.

## Bug #15 — Nota fuera de rango 5.7 (…dfc)
- **Archivo:** `database/grades.json`
- **Severidad / categoría:** medium / invalid-data
- **Problema:** Mismo caso que el #14 en otra nota.
- **Antes:** `"value":5.7`
- **Después:** `"value":5`
- **Cómo verificar:** Tras `npm run db:import`, igual que el #14.

## Bug #16 — Nota guardada como texto con coma
- **Archivo:** `database/grades.json`
- **Severidad / categoría:** medium / invalid-type
- **Problema:** `value: "4,2"` era un string; el schema espera un número, así que se rompían los cálculos de acumulado.
- **Antes:** `"value":"4,2"`
- **Después:** `"value":4.2`
- **Cómo verificar:** Tras `npm run db:import`, la nota se ve como 4.2 y cuenta en el acumulado.

## Bug #17 — Nota ligada a una evaluación de otro grupo
- **Archivo:** `database/grades.json`
- **Severidad / categoría:** medium / broken-reference
- **Problema:** La nota `…dfd` (matrícula del grupo `…c3e`) apuntaba a "Parcial 2" del grupo `…c73`, así que no aparecía en la planilla del grupo correcto.
- **Antes:** `evaluation` = `…e11` (grupo …c73)
- **Después:** `evaluation` = `…df2` (Parcial 2 del grupo …c3e)
- **Cómo verificar:** Tras `npm run db:import`, en la planilla del grupo …c3e, la columna Parcial 2 muestra la nota.

## Bug #18 — Estudiante con programa inexistente
- **Archivo:** `database/students.json`
- **Severidad / categoría:** high / orphan-reference
- **Problema:** El estudiante E20210046 apuntaba al programa `6ac057b2…f3c4`, que no existe, así que historial y malla fallaban.
- **Antes:** `program` = `6ac057b2…f3c4`
- **Después:** `program` = `…942` (programa de la mayoría de sus materias)
- **Cómo verificar:** Tras `npm run db:import`, como E20210046, "Malla curricular" e "Historial" cargan.

## Bug #19 — Decano inexistente en FAC-COM
- **Archivo:** `database/faculties.json`
- **Severidad / categoría:** low / orphan-reference
- **Problema:** `dean` apuntaba al docente `6ac057b2…f3c3`, que no existe.
- **Antes:** `dean` = `6ac057b2…f3c3`
- **Después:** `dean` = `…b33` (docente de esa facultad); **confirmar el decano real**
- **Cómo verificar:** Tras `npm run db:import`, la facultad FAC-COM no tiene referencias rotas.

## Bug #20 — Código de programa duplicado (DERE)
- **Archivo:** `database/programs.json`
- **Severidad / categoría:** high / duplicate-data
- **Problema:** "Derecho (jornada nocturna)" repetía el código `DERE`; el schema exige `unique`, así que hay error E11000 al crear el índice.
- **Antes:** `"code":"DERE"`
- **Después:** `"code":"DERE-NOC"`
- **Cómo verificar:** Tras `npm run db:import`, Programas muestra ambos con códigos distintos.

## Bug #21 — Materia con 0 créditos (ODON105)
- **Archivo:** `database/subjects.json`
- **Severidad / categoría:** medium / invalid-data
- **Problema:** `credits: 0` viola `min: 1`; los créditos matriculados y el promedio ponderado no la contaban. Se usa 3, el valor más común; **confirmar con el plan de estudios**.
- **Antes:** `"credits":0`
- **Después:** `"credits":3`
- **Cómo verificar:** Tras `npm run db:import`, ODON105 muestra 3 créditos en Materias y en la malla.

## Bug #22 — Materia prerrequisito de sí misma (MAT101)
- **Archivo:** `database/subjects.json`
- **Severidad / categoría:** high / invalid-data
- **Problema:** MAT101 se tenía a sí misma en `prerequisites`, así que nadie podía matricularla (el prerrequisito nunca se cumple).
- **Antes:** `prerequisites` incluía MAT101
- **Después:** se quita la autorreferencia
- **Cómo verificar:** Tras `npm run db:import`, en la malla, MAT101 ya no dice "Requiere: MAT101".

## Bug #23 — Plan de evaluación que suma 110%
- **Archivo:** `database/evaluations.json`
- **Severidad / categoría:** high / invalid-data
- **Problema:** El grupo `…c3a` tenía Taller 30% (25+25+30+30 = 110). Los otros 24 grupos usan 25/25/20/30, y con un plan distinto de 100 no se puede finalizar el grupo.
- **Antes:** Taller `"weight":30`
- **Después:** Taller `"weight":20`
- **Cómo verificar:** Tras `npm run db:import`, en "Evaluaciones" la suma es 100% y "Finalizar grupo" se habilita.

## Bug #24 — Estado de periodo con mayúscula
- **Archivo:** `database/periods.json`
- **Severidad / categoría:** critical / invalid-data
- **Problema:** El periodo 2026-2 tenía `status: "Abierto"`; el enum es `abierto`. No había ningún periodo abierto, así que la matrícula y los reportes decían "No hay un periodo abierto".
- **Antes:** `"status":"Abierto"`
- **Después:** `"status":"abierto"`
- **Cómo verificar:** Tras `npm run db:import`, "Periodo actual" en el inicio muestra 2026-2.

## Bug #25 — Tipo de notificación inexistente
- **Archivo:** `database/notifications.json`
- **Severidad / categoría:** medium / invalid-data
- **Problema:** `type: "aviso_urgente"` no está en el enum; la lista del front fallaba al buscar su ícono (`TYPE[n.type]` era undefined).
- **Antes:** `"type":"aviso_urgente"`
- **Después:** `"type":"aviso"`
- **Cómo verificar:** Tras `npm run db:import`, el destinatario abre "Notificaciones" sin error.

## Bugs de frontera (requieren coordinar con backend)
- Ninguno pendiente: el equipo de backend ya corrigió el prefijo `/api` y el puerto.

## Sospechosos (no modificados)
- Salón **B-104** (capacidad 22) asignado a grupos con cupo 32 (`…c3a`) y 25 (`…c99`). No está claro si el error es la capacidad del salón o el cupo del grupo.
- 40 notas en `grades.json` con `createdAt` posterior a `updatedAt`. Parece un artefacto del generador del seed y no afecta a la app.
