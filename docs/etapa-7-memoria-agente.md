# Etapa 7 — Memoria del agente (Engram)

> Qué se implementó, cómo se comprueba, y la misma explicación en palabras
> de niño. La parte 1 es para la defensa; la parte 2 para entender de verdad.

---

# Parte 1 — Qué se implementó (para la defensa)

## 1.1 El problema que resuelve

Un agente de código arranca cada sesión sin recuerdo. Cierra la ventana y
olvida: por qué se eligió PostgreSQL y no SQLite, qué significaba RN02, qué
decisiones ya se tomaron y cuáles se descartaron. La siguiente sesión vuelve a
tirar todo lo mismo desde cero, y a veces decide distinto — no porque tenga
razones nuevas, sino porque no se acuerda de las anteriores.

Engram es la capa que corta ese amnesia: guarda las decisiones y hallazgos
como datos recuperables, fuera del repo.

## 1.2 Qué se guardó (7 memorias, proyecto `turnos-odontologia`)

| # | Tipo | Título | Qué aporta |
|---|------|--------|-----------|
| 1 | `decision` | Alcance real de C-01 tras el recorte | C-01 quedó en **CU01 + RN02**. CU02/CU03/CU04 fuera. La migración `003` dropeó el índice RN05 y las columnas `token_cancelacion` / `cancelled_at`. |
| 2 | `discovery` | **AGENTS.md y skill-registry están desactualizados** | Describen el alcance original completo. En `tests/` **no existe** `test_reserva_guest.py`; en `app/api/v1/` solo hay `turnos.py`. |
| 3 | `decision` | Invariante RN02 — doble EXCLUDE | Dos `EXCLUDE USING gist` sobre `tstzrange(inicio, fin)`, parciales con `WHERE estado='activo'`, + `btree_gist`, + `CHECK (fin > inicio)`. `IntegrityError` → 409 con código por **nombre del constraint**. |
| 4 | `decision` | Stack y decisiones DD-01 a DD-07 | FastAPI + PG16, API pura sin frontend, escala chica, mock de notificaciones, sin ficha clínica. |
| 5 | `convention` | **Restricción legal — Ley 25.326** | Prohibido guardar datos reales de pacientes (Art. 5.1 / 8 / 12.1). Solo ficticios. Aplica **también a la memoria del agente**. |
| 6 | `convention` | Workflow SDD y reglas duras | Nunca commitear sin pedido, Conventional Commits, routers finos, `timestamptz`, nunca tocar el `step` del orquestador. |
| 7 | `discovery` | Puntos abiertos y ambiente | IN-01 / IN-02, y que **Docker no está corriendo** → la suite contra Postgres no se puede ejecutar hasta levantarlo. |

Cada memoria lleva al final una línea `PROVENIENCIA:` que dice **de qué
archivo salió cada afirmación**. Eso es deliberado: si mañana una memoria
contradice al código, se sabe cuál de los dos miente.

> La memoria 2 es el hallazgo más valioso de la etapa y salió de esta misma
> implementación: al verificar el alcance contra los archivos reales antes de
> guardar, se detectó que `AGENTS.md` y `.atl/skill-registry.md` seguieron
> describiendo el alcance original que ya se había recortado.

## 1.3 Evidencia para el video (comandos reales, ejecutados)

**Antes de la etapa** — la memoria estaba configurada pero vacía:

```
$ engram stats
  Sessions:     0
  Observations: 0
  Projects:     none yet
```

**Después de guardar** — el store poblado:

```
$ engram stats
  Sessions:     1
  Observations: 7
  Projects:     turnos-odontologia
  Database:     C:\Users\Usuario\.engram/engram.db
```

**Consulta de recuperación desde una sesión nueva** — el agente pide el
contexto y lo recibe sin haber leído ningún archivo del proyecto:

```
$ engram search "RN02 solapamiento EXCLUDE" --project turnos-odontologia
Found 1 memories:

[1] #3 (decision) — Invariante RN02 - doble EXCLUDE en Postgres
    RN02 (no solapamiento) es la invariante CENTRAL del proyecto y vive en la
    BASE DE DATOS, no en Python. Implementacion: dos constraints EXCLUDE USING
    gist sobre tstzrange(inicio, fin) WITH && -- uno por profesional_id y otro
    por sillon_id -- ambos parciales con WHERE (estado = 'activo')...
    2026-10-14 19:49:14 | project: turnos-odontologia | scope: project
```

Y con contexto genérico, `engram context` devuelve las 7.

## 1.4 Por qué esto evita que el agente arranque de cero

Sin memoria, el agente necesita ~6 lecturas para reconstruir el contexto
(`AGENTS.md`, `CHANGES.md`, 11 archivos de KB, `alembic/versions/`) — y aun
así puede deducir mal el alcance actual.

Con memoria, abre el proyecto y hace **una** consulta. Trae, ya digerido:
la invariante central con su implementación exacta, las decisiones de stack
con su justificación, las restricciones legales, el workflow, y — lo más
importante — el aviso de que dos documentos del repo están viejos. Arranca
informado en segundos y, sobre todo, **arranca con lo correcto**.

El orden importa: la memoria se recuperó *antes* de escribir código, así que
guió el trabajo. En vez de inventar un `POST /reservas` porque `AGENTS.md` lo
mencionaba, el agente leyó la memoria 2 y supo que ese endpoint no existe.

## 1.5 Dónde vive la memoria (y por qué el repo quedó intacto)

```
C:\Users\Usuario\.engram\engram.db     ← todo: sesiones, memorias, prompts
```

**Fuera del repositorio.** Engram no crea ni edita archivos del proyecto. El
único comando que escribiría dentro es `engram sync` (opt-in, genera `.engram/`
con chunks), y en este proyecto **no se corrió** — así que `git status` quedó
limpio y solo se versiona esta documentación.

Como prevención por si alguien corre `sync` más adelante, `.engram/` ya está en
`.gitignore`. Eso protege la regla dura de no commitear secretos ni datos de
pacientes.

** proyecto explícito:** las memorias se guardaron con
`--project turnos-odontologia`, no con detección automática del directorio
(el repo está anidado en un path con espacios y autodetección es frágil).