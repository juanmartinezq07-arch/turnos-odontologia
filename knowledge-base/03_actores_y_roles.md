# Actores y Roles

## Actores del sistema

| Actor | Descripción | Cómo interactúa |
|-------|-------------|-----------------|
| Recepcionista / Asistente | Opera la agenda global del consultorio. Es el único rol con escritura privilegiada | Cliente HTTP autenticado (básico en MVP, ej. API key o usuario fijo). Crea, cancela y reprograma turnos |
| Odontólogo/a | Profesional que atiende. Consulta su agenda | Cliente HTTP autenticado, solo lectura sobre su agenda (+ prestaciones asignadas) |
| Paciente (guest, sin cuenta) | Persona que reserva por enlace público | HTTP sin autenticación, solo `GET /disponibilidad` y `POST /reservas` + cancelación con token de reserva |
| Sistema / Tests | Actor técnico que verifica la invariante | pytest + httpx contra la API y contra la DB |

**Decisión de alcance (de Discovery, se mantiene):** el paciente **no se autentica**. La reserva es guest booking por enlace público. Esto evita RBAC de paciente y mantiene simple el modelo inicial. El riesgo de ocupación indiscriminada (R3) se mitiga no guardando ficha clínica ni datos sensibles y exigiendo confirmación por canal (mock en MVP).

No hay actor "administrador" en el MVP. La gestión de profesionales/sillones/prestaciones se hace por seed + endpoints mínimos o carga inicial, no por un panel.

## RBAC — Matriz de permisos

| Rol | Turnos (alta) | Reserva pública | Agenda / disponibilidad (lectura) | Cancelación / reprogramación | Catálogos (profesionales, sillones, prestaciones) |
|-----|---------------|-----------------|-----------------------------------|------------------------------|---------------------------------------------------|
| Recepcionista | Sí (todos los profesionales) | — | Sí (global) | Sí | Lectura (escritura solo por seed/admin mínimo) |
| Odontólogo/a | No | — | Sí (solo la propia) | No | Lectura |
| Paciente guest | No | Sí (solo crear la propia + cancelar con token) | Sí (disponibilidad pública) | Solo la propia con token | Lectura pública de catálogos para reservar |
| Anónimo total | No | No (sin enlace/rate-limit) | Solo disponibilidad pública | No | Solo lectura pública mínima |

Autorización en MVP: distinción simple por rol/credencial (API key o usuario fijo por rol). Sin OAuth, sin JWT completo, sin RBAC configurable. Multi-sucursal y roles configurables quedan en backlog.

## Rutas públicas

Sin autenticación:

- `GET /disponibilidad` — consulta de slots reales.
- `POST /reservas` — alta guest (con validación de rate-limit básica y datos mínimos del paciente).
- `POST /reservas/{token}/cancelacion` — cancelación guest con token opaco entregado al reservar.
- `GET /profesionales`, `GET /sillones`, `GET /prestaciones` — lectura mínima para que el flujo público pueda armar la reserva.
- `GET /docs`, `GET /openapi.json` — documentación generada por FastAPI (útil para la demo).

Todo lo demás exige credencial de consultorio (recepcionista u odontólogo según matriz).
