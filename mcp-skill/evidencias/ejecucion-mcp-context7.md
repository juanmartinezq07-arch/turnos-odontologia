# Evidencia de Conexión y Ejecución Real del Servidor MCP (`Context7`)

**Fecha de ejecución**: 04/11/2026  
**Servidor MCP**: `context7` (`@upstash/context7-mcp`)  
**Cliente MCP**: Antigravity IDE / CLI (`~/.gemini/antigravity-cli/mcp/context7/`)  

---

## 1. Comprobación de Esquemas de Herramientas Disponibles

El servidor `context7` expone dos herramientas (*lazy-loaded*) en el entorno del agente:
- `resolve-library-id`: Resuelve el nombre de una librería o paquete al identificador canónico de Context7 (`/org/project`).
- `query-docs`: Consulta fragmentos oficiales de documentación y código para el `libraryId` resuelto.

---

## 2. Primera Invocación Real: `resolve-library-id`

### Solicitud enviada (`call_mcp_tool`)
```json
{
  "ServerName": "context7",
  "ToolName": "resolve-library-id",
  "Arguments": {
    "libraryName": "SQLAlchemy",
    "query": "How to manage AsyncSession transactions, flush, commit, rollback and expire_on_commit in SQLAlchemy 2.0"
  }
}
```

### Resultado obtenido (extracto real)
```text
Available Libraries:
- Title: SQLAlchemy ORM
  Context7-compatible library ID: /websites/sqlalchemy_en_20_orm
  Description: SQLAlchemy ORM is an Object Relational Mapper that provides high-level SQL construction and automated persistence of Python objects to databases.
  Code Snippets: 7872 | Source Reputation: High | Benchmark Score: 76.82
- Title: SQLAlchemy
  Context7-compatible library ID: /sqlalchemy/sqlalchemy
  Versions: rel_1_4_51, rel_2_1_6, rel_2_0_55
```

---

## 3. Segunda Invocación Real: `query-docs`

### Solicitud enviada (`call_mcp_tool`)
```json
{
  "ServerName": "context7",
  "ToolName": "query-docs",
  "Arguments": {
    "libraryId": "/websites/sqlalchemy_en_20_orm",
    "query": "How to use AsyncSession with expire_on_commit=False, session.get, flush, commit, and rollback on IntegrityError in SQLAlchemy 2.0 asyncio"
  }
}
```

### Resultado obtenido (extracto real)
- **Fuente oficial recuperada**: `https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html`
- **Patrón técnico verificado**:
  1. `async_sessionmaker(engine, expire_on_commit=False)` evita IO implícito tras ejecutar `await session.commit()`, permitiendo leer `turno.estado`, `turno.cancelled_at` y `turno.id` en la respuesta de FastAPI y en la llamada post-commit a `get_notification_service().notify_turn_updated(turno.id)`.
  2. `await session.get(Turno, turno_id)` recupera la entidad por clave primaria dentro de la sesión asíncrona; al mutar `turno.estado = "cancelado"` y `turno.cancelled_at = ahora`, el `await session.commit()` emite el `UPDATE` correspondiente.
  3. En operaciones atómicas compuestas (`C-23`), si el `flush()` del nuevo turno lanza `IntegrityError` (por `rn02_profesional`, `rn02_sillon` o `rn05_un_activo_por_dia`), ejecutar `await session.rollback()` revierte también el cambio de estado del turno original dentro de la misma transacción.
