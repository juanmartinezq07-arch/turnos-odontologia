# Flujos Principales

Cada flujo es extremo a extremo. Actores: `P` = paciente guest, `R` = recepcionista, `O` = odontólogo/a.

## Flujo 1: Reserva guest sobre disponibilidad real (CU02 + US-003)

**Disparador**: P abre el enlace público. **Actor**: P (sin auth).

**Pasos**:
1. P pide `GET /disponibilidad?profesional_id=&fecha=&prestacion_id=` → API computa slots desde `HorarioAtencion` menos turnos `activos`.
2. P elige slot y manda `POST /reservas` con datos mínimos + ids + `inicio`.
3. API valida RN01 (calcula `fin`), RN03 (no pasado/fuera de horario), RN05 (un activo por día).
4. API intenta `INSERT` → PostgreSQL chequea ambos `EXCLUDE` (RN02). Si hay carrera, una sola gana.
5. Si commit ok → API llama `NotificationService.notificar(reserva)` (mock, best-effort) y devuelve 201 + token de cancelación.
6. Si viola EXCLUDE → traduce a 409 `RN02_PROFESIONAL` o `RN02_SILLON`.

**Secuencia (caso feliz)**:
```
P → API: GET /disponibilidad
API → DB: SELECT turnos activos + horario
API → P: slots[]
P → API: POST /reservas
API → DB: INSERT turno (chequea EXCLUDE x2)
DB → API: ok
API → Mock: notificar() (no bloquea)
API → P: 201 + token
```

**Casos de error**:
- Slot tomado entre consulta y alta → 409 con regla indicada, P re-consulta disponibilidad.
- Doble request concurrente → una 201, otra 409 (testeado).
- Datos clínicos en el payload → 422 (no se persiste nada clínico).

## Flujo 2: Alta por recepcionista (CU01 + US-001)

**Disparador**: llamado o mensaje del paciente. **Actor**: R (autenticada).

**Pasos**:
1. R consulta disponibilidad igual que P (mismo endpoint, con auth).
2. R manda `POST /turnos` con profesional + sillón + prestación + paciente.
3. Mismas validaciones y mismo `INSERT` con doble EXCLUDE que el flujo 1.
4. 201 + notificación mock; 409/422 según regla violada con código machine-readable.

**Casos de error**: mismos que flujo 1 + 401 si falta credencial de consultorio.

## Flujo 3: Cancelación y reprogramación (CU03 + US-004/US-005)

**Disparador**: paciente avisa o R detecta hueco. **Actor**: R o P con token.

**Pasos (cancelación)**:
1. R (o P con token) pide cancelación → API verifica estado `activo`.
2. API hace `UPDATE turno SET estado='cancelado', cancelled_at=now()`.
3. El `WHERE (estado='activo')` de los EXCLUDE deja de contar ese rango → slot liberado.
4. Notificación mock de cancelación. El slot reaparece en disponibilidad.

**Pasos (reprogramación)**:
1. R pide mover a nuevo `inicio` → API abre transacción.
2. Marca el original `cancelado` y trata de insertar el nuevo con el mismo paciente/recurso.
3. Si el nuevo viola RN02/RN03/RN05 → rollback total, el original sigue activo.
4. Si ok → commit, dos notificaciones mock (cancelación + nueva reserva).

**Casos de error**:
- Cancelar algo ya cancelado → 409/422 idempotente según defina el change (no duplica el efecto).
- Reprogramar al pasado → 422, sin tocar el original.

## Flujo 4: Agenda del día del odontólogo (CU04 + US-006)

**Disparador**: O arranca su jornada. **Actor**: O (autenticado).

**Pasos**:
1. O pide `GET /agenda?profesional_id=propio&fecha=hoy`.
2. API verifica que pide su propia agenda (autorización mínima).
3. Devuelve turnos activos ordenados por `inicio` con prestación (y su duración), sillón y paciente.
4. Los cancelados no aparecen salvo `?incluir_cancelados=true`.

**Casos de error**:
- Pedir agenda ajena → 403.
- Fecha inválida → 422.
