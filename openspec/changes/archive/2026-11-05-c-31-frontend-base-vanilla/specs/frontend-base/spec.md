# Spec Delta

## Purpose

Define el contrato observable de la base de interfaz web estática servida por FastAPI en el mismo origen.

## ADDED Requirements

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

El sistema SHALL permitir navegar entre las pantallas de la interfaz sin recargar la página completa.

#### Scenario: Cambio de pantalla

- **WHEN** el usuario navega a otra sección
- **THEN** solo el contenido principal se actualiza, sin recarga del documento completo