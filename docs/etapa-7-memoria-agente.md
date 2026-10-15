# Etapa 7 — Memoria del agente (Engram)

> Qué se implementó, cómo se comprueba.

---

# Parte 1 — Qué se implementó 

## 1.1 El problema que resuelve

Un agente de código arranca cada sesión sin recuerdo. Cierra la ventana y
olvida: por qué se eligió PostgreSQL y no SQLite, qué significaba RN02, qué
decisiones ya se tomaron y cuáles se descartaron. La siguiente sesión vuelve a
tirar todo lo mismo desde cero, y a veces decide distinto — no porque tenga
razones nuevas, sino porque no se acuerda de las anteriores.

Engram es la capa que corta ese amnesia: guarda las decisiones y hallazgos
como datos recuperables, fuera del repo.

## 1.2 Qué se guardó (15 observaciones, proyecto `turnos-odontologia`)

> Verificado el 2026-10-15 contra el store real (`C:\Users\bansh\.engram\engram.db`):
> `Sessions: 3, Observations: 28` en total; 15 pertenecen a este proyecto
> (ids #12–#26, del 2026-10-02 al 2026-10-04). La tabla anterior decía 7
> porque se redactó antes del propose/apply/archive.

| # | Tipo | Título | Qué aporta |
|---|------|--------|-----------|
| 12 | `decision` | Alcance TP: mock WhatsApp + guest booking | Un solo change; WhatsApp mockeado tras interfaz; reserva guest sin auth. |
| 13 | `discovery` | Investigación sistemas LatAm + internacionales | 20 sistemas; 19 de 20 no declaran anti-solapamiento público. |
| 14 | `discovery` | Hallazgo: hueco de mercado en doble validación | Ningún competidor argentino publica el control explícito (sostiene R1/RN02). |
| 15 | `decision` | Discovery cerrado: 11 dimensiones + 35% de la nota | `discovery/discovery.md`, 14 competidores, 4 CU, 5 RN, 5 riesgos, 4 preguntas. |
| 16 | `session_summary` | Session summary: turnos-odontologia | Goal, instrucciones e idioma del proyecto fundacional. |
| 17 | `decision` | OPSX: kb completada | `knowledge-base/` completa (10 canónicos + README). |
| 18 | `decision` | OPSX: roadmap completado | `CHANGES.md` con único change C-01 (RN02 EXCLUDE, CU01+CU02). |
| 19 | `discovery` | find-skill: detección de skills de dominio | 10 skills relevantes detectadas, ninguna instalada entonces. |
| 20 | `config` | Skills instaladas TurnosAR | Las 7 globales core (fastapi, tdd, postgres, docker, pytest...). |
| 21 | `config` | skill-registry turnos-odontologia | `.atl/skill-registry.md` con reglas compactas matcheadas a C-01. |
| 22 | `config` | Reglas agente + restricción pacientes | `AGENTS.md`/`CLAUDE.md` idénticos, Ley 25.326 innnegociable. |
| 23 | `decision` | OPSX: fundación cerrada | Registry + reglas + step a done. |
| 24 | `decision` | OPSX: propose completado para turnos-mvp | Proposal + design + 5 specs + 21 tasks, RN02 EXCLUDE. |
| 25 | `decision` | OPSX: apply completado para turnos-mvp | 21/21 tasks (modelos, rules puras, POST /turnos, guest, agenda, mock). |
| 26 | `decision` | OPSX: archive completado para turnos-mvp | Change archivado, 5 specs sincronizadas, `validate --strict` 5/5. |

## 1.3 Evidencia para el video (comandos reales, ejecutados)

**Antes de la etapa** — la memoria estaba configurada pero vacía:

```
$ engram stats
  Sessions:     0
  Observations: 0
  Projects:     none yet
```

**Después de guardar** — el store poblado (verificado 2026-10-15 con el
CLI Go, `~\go\bin\engram.exe`, sobre el mismo `.db`):

```
$ engram stats
  Sessions:     3
  Observations: 28
  Prompts:      0
  Projects:     apolo, turnos-odontologia, tp-sdd-gimnasio
  Database:     C:\Users\bansh\.engram/engram.db
```

**Consulta de recuperación desde una sesión nueva** — el agente pide el
contexto y lo recibe sin haber leído ningún archivo del proyecto:

```
$ engram search "RN02 solapamiento EXCLUDE" --project turnos-odontologia
Found 1 memories:

[1] #16 (session_summary) — Session summary: turnos-odontologia
    ## Goal
    Fundar el proyecto TurnosAR (turnero odontológico, Argentina) con el
    stack OpenSpec/Active Stack, siguiendo el flujo de `active-orchestrator`:
    openspec init → Discovery → Knowledge Base → Roadmap → skills → ...
    2026-10-02 09:49:45 | project: turnos-odontologia | scope: project
```

Y con `engram context` (desde la raíz del repo) lista las 3 sesiones con
sus observaciones recientes — `turnos-odontologia` con sus 15.

> Detalle para la defensa: la sesión quedó registrada con
> `directory=...Metodología I\turnos-odontologia\turnos-odontologia`
> (ruta anidada doble, distinta a la real del repo). Por eso las memorias
> se guardan y consultan con `--project turnos-odontologia` explícito en
> vez de confiar en la autodetección por directorio.
>
> Nota técnica: el CLI imprime por stderr un aviso de update disponible
> (`1.20.0 -> 3.4.0`) que en PowerShell se ve rojo pero no rompe nada.
> No actualizar antes del video: un salto mayor podría migrar el `.db`.

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
C:\Users\bansh\.engram\engram.db     ← todo: sesiones, memorias, prompts
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