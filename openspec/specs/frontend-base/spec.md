# frontend-base Specification

## Purpose
Define el contrato observable de la base de interfaz web estática servida por FastAPI en el mismo origen.

## Requirements

### Requirement: Servir interfaz estática en el mismo origen

El sistema SHALL servir los archivos estáticos de la interfaz (HTML, CSS, JavaScript) desde el mismo origen que la API REST, sin requerir CORS ni proceso de build.

#### Scenario: Acceso a la interfaz

- **WHEN** un navegador solicita la ruta raíz o un recurso estático
- **THEN** el servidor responde con el archivo correspondiente con el content-type adecuado

#### Scenario: API no bloqueada por estáticos

- **WHEN** un cliente llama a un endpoint de la API (`/profesionales`, `/turnos`, etc.)
- **THEN** el servidor responde con JSON y no con un archivo estático

### Requirement: Cliente HTTP mapea errores por código

El sistema SHALL exponer un cliente HTTP nativo que parsea las respuestas de error con forma `{code, message}` y expone un error tipado con `code`, `message` y `status`, sin parsear texto libre.

#### Scenario: Error de negocio

- **WHEN** una petición recibe 409 con `{code: "RN02_PROFESIONAL", message: ...}`
- **THEN** el cliente lanza un error con `code === "RN02_PROFESIONAL"` y `status === 409`

### Requirement: Credenciales de rol solo en memoria

El sistema SHALL requerir el ingreso de la API key de rol en tiempo de ejecución y mantenerla únicamente en memoria del navegador; no SHALL persistirla en archivos estáticos ni en almacenamiento persistente del navegador.

#### Scenario: Recarga de página

- **WHEN** el usuario recarga la página
- **THEN** la credencial se pierde y debe reingresarse

### Requirement: Navegación entre pantallas sin recarga completa

El sistema SHALL permitir navegar entre las pantallas de la interfaz sin recargar la página completa, incluyendo la pantalla de agenda diaria.

#### Scenario: Cambio de pantalla

- **WHEN** el usuario navega a otra sección
- **THEN** solo el contenido principal se actualiza, sin recarga del documento completo

### Requirement: Pantalla de agenda diaria

La interfaz SHALL ofrecer una pantalla que consulte `GET /agenda?profesional_id=&fecha=` con credencial de recepcionista u odontólogo y muestre los turnos ordenados por `inicio`, incluyendo prestación (y duración), sillón y paciente, con opción de incluir cancelados.

#### Scenario: Agenda cargada

- **WHEN** el usuario ingresa profesional y fecha válidos con credencial válida
- **THEN** se listan los turnos ordenados por inicio con prestación, sillón y paciente

#### Scenario: Agenda ajena (403)

- **WHEN** un odontólogo consulta la agenda de otro profesional
- **THEN** la UI muestra un mensaje de acceso denegado (código `AGENDA_AJENA`)

#### Scenario: Sin credencial (401)

- **WHEN** se consulta la agenda sin credencial válida
- **THEN** la UI solicita el ingreso de la API key

### Requirement: Pantalla de alta de turno

La interfaz SHALL ofrecer una pantalla que, usando catálogos públicos y `GET /disponibilidad`, permita a la recepcionista crear un turno vía `POST /turnos` enviando solo `inicio` (sin `fin`), con datos mínimos del paciente, y mostrar el resultado o el error por código.

#### Scenario: Alta exitosa

- **WHEN** la recepcionista completa el formulario válido y hay slot disponible
- **THEN** se crea el turno (201) y se muestra confirmación con `fin` calculado

#### Scenario: Conflicto de agenda (409)

- **WHEN** el slot choca con otro turno (profesional/sillón/RN05)
- **THEN** la UI muestra un mensaje específico según el código (`RN02_PROFESIONAL`, `RN02_SILLON`, `RN05`)

#### Scenario: Validación (422)

- **WHEN** el inicio está en el pasado o fuera de horario o faltan campos
- **THEN** la UI muestra el error de validación sin crear el turno

#### Scenario: Sin credencial (401)

- **WHEN** se intenta crear un turno sin credencial de recepción
- **THEN** la UI solicita el ingreso de la API key

### Requirement: Pantalla de cancelación de turno

La interfaz SHALL permitir cancelar un turno activo vía `POST /turnos/{id}/cancelacion` y mostrar el estado `cancelado` con `cancelled_at`.

#### Scenario: Cancelación exitosa

- **WHEN** la recepcionista cancela un turno activo
- **THEN** la UI muestra el turno como `cancelado` con `cancelled_at`

#### Scenario: Idempotencia

- **WHEN** se cancela un turno ya cancelado
- **THEN** la UI muestra el mismo `cancelled_at` sin error

### Requirement: Pantalla de reprogramación de turno

La interfaz SHALL permitir reprogramar un turno activo vía `POST /turnos/{id}/reprogramacion` enviando el nuevo `inicio` (y opcionalmente `sillon_id`), mostrando original (cancelado) y nuevo (activo).

#### Scenario: Reprogramación exitosa

- **WHEN** el destino está libre
- **THEN** la UI muestra el original cancelado y el nuevo activo

#### Scenario: Fallo con rollback

- **WHEN** el destino viola RN02/RN03/RN05
- **THEN** la UI muestra el error y deja claro que el original sigue activo

### Requirement: Flujo de reserva pública guest

La interfaz SHALL ofrecer un flujo sin autenticación: catálogos → disponibilidad → `POST /reservas` → mostrar y guardar el `token_cancelacion` → cancelación con token.

#### Scenario: Reserva exitosa

- **WHEN** el guest completa el flujo con datos válidos
- **THEN** se crea la reserva (201) y se muestra el token de cancelación

#### Scenario: Cancelación con token

- **WHEN** el guest cancela con su token
- **THEN** la reserva se cancela y el slot se libera

#### Scenario: Conflicto (409)

- **WHEN** el slot ya está ocupado
- **THEN** la UI muestra el error por código (RN02_*, RN05)
