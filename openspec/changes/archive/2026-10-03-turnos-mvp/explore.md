# Explore — C-01 turnos-mvp (resumen del relevamiento)

## Estado inicial

Repo greenfield al momento de proponer: solo fundación (`.active-orchestrator-state.json`
con Discovery cerrado), `knowledge-base/` (10 canónicos), `CHANGES.md` (C-01 único) y
reglas del agente (`AGENTS.md`/`CLAUDE.md`). Sin código de aplicación, sin specs previas,
sin base de datos.

## Problema a resolver

La gestión de turnos en consultorios es manual/fragmentada y produce solapamientos por
profesional y por sillón/box. El Discovery encontró que ningún competidor argentino
publica la doble validación simultánea, y que una validación solo en la capa de
aplicación deja una ventana de carrera ante reservas concurrentes.

## Decisión de alcance (Ajustar aplicado en Propose)

La primera propuesta cubría CU01+CU02+CU03/CU04 (guest, cancelación, agenda). Al revisar
el spec se recortó a **CU01**: alta evitando solapamientos (RN02 en Postgres como
invariante; RN01/RN03 como soporte). CU02/CU03/CU04 quedaron como trabajo futuro.
Si ese recorte no se hacía, el change dejaba de ser "una sola funcionalidad" y no se
terminaba en plazo.
