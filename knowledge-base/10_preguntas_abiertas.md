# Preguntas Abiertas

## Inconsistencias detectadas

### IN-01 — Anexos de research con intrusiones en inglés
**Documento A dice**: `discovery/discovery.md` y el state están íntegramente en español.
**Documento B dice**: los anexos `docs/discovery/_research-*.md` contienen palabras en inglés sin traducir.
**Impacto**: bajo para la KB (no se usaron como fuente de stack/scale), pero riesgoso si alguien los cita en la demo o en el informe.
**Resolución propuesta**: no tocar los anexos en esta fase; si hay tiempo, pasarles un normalizador de idioma antes del video. La KB no depende de ellos.

### IN-02 — PDF de criterios de cátedra fuera de `docs/`
**Documento A dice**: el PDF de criterios vive fuera de `docs/` para evitar Mode A.
**Documento B dice**: `docs/discovery/` contiene informe + anexos que podrían re-disparar Mode A en futuras corridas.
**Impacto**: medio — una futura corrida de kb-creator sin forzar Mode B volvería a inferir mal stack/scale.
**Resolución propuesta**: toda corrida futura de kb-creator en este repo debe forzar Mode B con las 4 respuestas cerradas de este proyecto. Queda registrado acá como advertencia.

## Preguntas abiertas (priorizadas)

| Prioridad | Pregunta | Bloquea | Decisor |
|-----------|----------|---------|---------|
| Alta | RN05 — implementación definitiva: ¿índice único parcial `(paciente_id, date(inicio)) WHERE activo` o validación en aplicación + test? | Change (migración inicial) | Tech (un integrante) |
| Alta | Concurrencia — ¿pytest con hilos + dos transacciones reales contra Postgres local alcanza como "test de concurrencia real" (Qw)? | Change (tests de RN02) | Cátedra / Tech |
| Media | Consentimiento Ley 25.326 Art. 5.1 (Qy): ¿entidad persistida `Consentimiento` en MVP o requisito documentado para fase 2? Propuesta: documentado, no persistido, dado que no hay dato clínico | Change (modelo) | Tech |
| Media | Reserva pública: ¿el paciente elige sillón o lo auto-asigna el sistema? Propuesta: lo elige la recepcionista; el endpoint público acepta `sillon_id` opcional y si falta auto-asigna el primero libre | Change (contrato `POST /reservas`) | Tech |
| Baja | Nombre definitivo (Qz): ¿`TurnosAR` queda o se cambia? La cátedra no exige uno propio | Video / README | Tech |
| Baja | Auth del personal: ¿API key fija por rol o usuario+password mínimo? Propuesta: API key por env var para no quemar horas en auth | Change | Tech |
| Baja | Rate-limit público: ¿ventana en memoria (`10/min`) o sin límite en MVP? Propuesta: en memoria, documentado como deuda | Change | Tech |

**Resueltas por esta KB (ya no bloquean)**:
- Qx (persistencia para RN02): resuelta → PostgreSQL 16 + `EXCLUDE USING gist` (DD-04).
- Stack/scale/sys: resueltos por las 4 respuestas cerradas (api / team / FastAPI+Postgres / mantenibilidad).
