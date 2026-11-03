# Spec Delta

## Purpose

Establece las directrices y fronteras arquitectónicas para el consumo de la API desde clientes web, resolviendo la relación con la decisión DD-01 y las garantías de seguridad para el manejo de credenciales.

## ADDED Requirements

### Requirement: Frontera de seguridad para clientes web

Cualquier interfaz web (frontend) desarrollada para interactuar con la API SHALL acceder a los endpoints administrativos y autenticados sin exponer claves estáticas de API (`API_KEY_RECEPCION`, `API_KEY_ODONTOLOGO`) en el código ni en el bundle estático del navegador. Las operaciones públicas de reserva (`POST /reservas` y consulta de disponibilidad) no requieren credenciales, mientras que las operaciones con rol SHALL canalizarse mediante sesiones seguras o proxy autenticado.

#### Scenario: Cliente público no expone secretos

- **WHEN** un usuario accede a la interfaz de reservas públicas
- **THEN** las peticiones al catálogo y disponibilidad se realizan contra endpoints abiertos sin transmitir cabeceras sensibles embebidas en el bundle

#### Scenario: Operaciones de recepcionista protegidas

- **WHEN** un operador recepcionista utiliza una interfaz para dar turnos
- **THEN** la autenticación contra la API no permite la extracción de la API key global por parte de usuarios finales del navegador

