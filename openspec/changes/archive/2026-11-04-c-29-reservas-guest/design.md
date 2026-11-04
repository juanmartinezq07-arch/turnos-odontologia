# Design: Reservas Públicas Guest (C-29)

## Contexto y Decisiones Arquitecturales

El endpoint `POST /reservas` permite que pacientes no autenticados soliciten turnos directamente. Para evitar carreras de concurrencia y mantener la robustez del modelo de datos:
1. **Auto-asignación de sillón**: Si `sillon_id` es None, se consultan los sillones activos y se evalúa cuál no tiene solapamientos activos en `[inicio, fin)`. Si ninguno está libre, se rechaza tempranamente con `409 RN02_SILLON`. Si dos transacciones eligen el mismo sillón simultáneamente, el constraint `EXCLUDE USING gist (sillon_id WITH =, tstzrange(...) WITH &&) WHERE (estado = 'activo')` de PostgreSQL garantiza que una triunfe (201) y la otra sea abortada (409).
2. **Generación de Token**: Se genera con `secrets.token_urlsafe(32)` o `str(uuid.uuid4())`, garantizando entropía criptográfica y unicidad. La columna `token_cancelacion` ya fue creada con `UNIQUE` en la migración 005 (`C-21`).
3. **Cancelación por Token**: `POST /reservas/{token}/cancelacion` busca el turno por `token_cancelacion`. Si existe, aplica la lógica ya probada de `cancelar_turno` (idempotencia y registro de `cancelled_at`).
4. **Rate Limiting**: Se implementa un middleware o dependencia ligera en memoria basada en buckets por IP cliente (`10 requests / 60s`).
5. **Privacidad (Ley 25.326)**: Pydantic v2 con `ConfigDict(extra="forbid")`.

## Componentes y Cambios

1. **Schemas** (`backend/app/schemas/reserva.py`):
   - `ReservaCreate`: `profesional_id: UUID`, `prestacion_id: UUID`, `inicio: datetime`, `sillon_id: UUID | None = None`, `paciente: PacienteIn`.
   - `ReservaOut`: incluye todos los campos de `TurnoOut` más `token_cancelacion: str`.
2. **Lógica de Aplicación** (`backend/app/application/reservas.py`):
   - `crear_reserva_guest(...)`
   - `cancelar_reserva_por_token(...)`
   - `autoasignar_sillon(...)`
3. **Rutas API** (`backend/app/api/v1/reservas.py`):
   - `POST /reservas` (status 201)
   - `POST /reservas/{token}/cancelacion` (status 200)
