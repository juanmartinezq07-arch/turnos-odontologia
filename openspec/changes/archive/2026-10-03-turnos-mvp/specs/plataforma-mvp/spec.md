# Spec Delta

## Purpose

Fija la base transversal del MVP: invariante anti-solapamiento en la base, auth mínima, errores estables, notificaciones mock, seed ficticio e infraestructura local reproducible.

## ADDED Requirements

### Requirement: Doble EXCLUDE parcial con semántica de borde

La base de datos SHALL aplicar dos constraints `EXCLUDE USING gist` parciales `WHERE (estado = 'activo')` — uno por `profesional_id`, otro por `sillon_id` — sobre `tstzrange(inicio, fin) WITH &&`, más `CHECK (fin > inicio)`, con `btree_gist` instalada primero. El rango SHALL usar semántica `[)` (borde que se toca no choca).

#### Scenario: Constraint bloquea doble commit concurrente

- **WHEN** dos transacciones concurrentes insertan el mismo slot activo del mismo profesional
- **THEN** una hace commit y la otra viola el constraint `RN02_PROFESIONAL`

#### Scenario: Cancelado no bloquea

- **WHEN** existe un turno `cancelado` en un rango y se inserta un activo idéntico
- **THEN** el insert hace commit sin violar constraints

### Requirement: RN05 con decisión documentada (cierra IN-01)

El change SHALL implementar RN05 como índice único parcial funcional `(paciente_id, date(inicio)) WHERE estado='activo'` o como validación en aplicación más test de carrera, y SHALL registrar la opción elegida en `design.md`.

#### Scenario: Decisión trazable

- **WHEN** se revisa `design.md` y la migración 002 o el servicio de reservas
- **THEN** la opción RN05 está implementada y su justificación consta en el diseño

### Requirement: Auth mínima por API keys y guest público

El sistema SHALL exigir API key de recepcionista u odontólogo (desde env `API_KEY_RECEPCION` / `API_KEY_ODONTOLOGO`) en todo endpoint no público, SHALL responder 401 sin credencial, y SHALL dejar sin auth `GET /disponibilidad`, `POST /reservas`, `POST /reservas/{token}/cancelacion`, catálogos y `/docs`.

#### Scenario: Escritura sin credencial rechazada

- **WHEN** se llama `POST /turnos` sin API key
- **THEN** el sistema responde 401

### Requirement: Formato de error estable y mapeo de constraints

Todo error SHALL usar la forma `{code, message}`; la violación de EXCLUDE SHALL mapearse a 409 con `RN02_PROFESIONAL` / `RN02_SILLON` / `RN05` (nunca 500, distinguiendo por nombre de constraint, no por parseo del mensaje); los errores Pydantic SHALL mapearse a 422.

#### Scenario: Violación EXCLUDE es 409 con código

- **WHEN** un insert viola el EXCLUDE de sillón bajo concurrencia
- **THEN** la API responde 409 con `code = RN02_SILLON`

### Requirement: Notificaciones mock best-effort

Toda escritura de turno SHALL invocar `NotificationService.notificar(...)` tras el commit de forma best-effort (`NOTIF_BACKEND=mock`): si falla, SHALL loguear y continuar sin rollback.

#### Scenario: Fallo del mock no revierte el turno

- **WHEN** el mock de notificaciones falla tras un alta válida
- **THEN** el turno sigue persistido y la API responde 201

### Requirement: Catálogos públicos mínimos y documentación

El sistema SHALL exponer `GET /profesionales`, `/sillones`, `/prestaciones` en lectura y SHALL servir `/docs` y `/openapi.json`.

#### Scenario: Reserva armable desde catálogos

- **WHEN** un cliente anónimo pide los tres catálogos y `/openapi.json`
- **THEN** recibe 200 con listados y el esquema OpenAPI

### Requirement: Infra local reproducible y seed ficticio

El repo SHALL incluir `docker-compose.yml` con un único servicio `db` (`postgres:16` pineada, volumen nombrado, healthcheck `pg_isready`, puerto solo en localhost), `.env.example` solo con placeholders (sin secretos reales) y un seed con datos exclusivamente ficticios (nombres tipo "Juan Pérez Demo", teléfonos `11-0000-0000`, mails `@example.com`).

#### Scenario: Levantar demo sin secretos reales

- **WHEN** un desarrollador sigue `docker-compose.yml` + `.env.example` con 2–3 profesionales, 2 sillones, 3 prestaciones, horario Lun–Vie 9–18 + Sáb 9–12, 1 turno activo y 1 cancelado
- **THEN** la API arranca contra `db` y ningún dato real de pacientes existe en el repo
