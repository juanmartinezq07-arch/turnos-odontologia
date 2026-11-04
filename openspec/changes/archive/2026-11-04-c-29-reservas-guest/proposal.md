# Proposal: Reservas Públicas Guest (US-003, US-004)

## Why

El portal público de autoservicio para pacientes (guest) necesita permitir la reserva de turnos sin requerir que el paciente inicie sesión ni posea cuenta previa. Asimismo, para permitir que el paciente cancele su propio turno sin comprometer turnos ajenos, el sistema debe emitir un `token_cancelacion` único y seguro que autorice exclusivamente la cancelación del turno asociado.

## What Changes

1. **Endpoint Público `POST /reservas`**:
   - Acceso sin cabecera de autenticación (`require_recepcion`).
   - Request con datos de contacto del paciente (`nombre`, `telefono` y/o `email`), `profesional_id`, `prestacion_id`, `inicio`, y `sillon_id` opcional.
   - Si `sillon_id` es nulo, el sistema auto-asigna el primer sillón libre que satisfaga `RN02_SILLON` en el rango `[inicio, fin)`.
   - Generación de `token_cancelacion` seguro (UUID v4 o token opaco URL-safe).
   - Retorno 201 Created con los datos del turno y el `token_cancelacion`.

2. **Endpoint Público `POST /reservas/{token}/cancelacion`**:
   - Acceso público parametrizado por token.
   - Cancela el turno asociado (`estado = 'cancelado'`, `cancelled_at = now()`) liberando el slot para nuevos turnos.
   - Idempotente si ya fue cancelado. Devuelve 404 si el token es inexistente.

3. **Invariantes y Mitigación de Abuso**:
   - Validación estricta de concurrencia y solapamiento (`RN01`, `RN02`, `RN03`, `RN05`).
   - Rate limiting en memoria para el endpoint de reserva (`RESERVA_RATE_LIMIT = 10/min` por IP o global de prueba) devolviendo 429 ante abuso.
   - Cumplimiento de **Ley 25.326**: `extra="forbid"` para rechazar cualquier dato clínico o innecesario.
