# TurnosAR — Sistema de Gestión de Turnos Odontológicos

> **Trabajo Práctico Integrador — Metodología en Sistemas I (TUP — UTN)**  
> **Grupo:** Dinosaurios Feroces  
> **Integrantes:**  
> - Isaías Morinigo  
> - Juan Martínez  

---

## 📖 Acerca del Proyecto

**TurnosAR** es un sistema integral de gestión de turnos para consultorios odontológicos en Argentina, diseñado e implementado siguiendo la metodología **Spec-Driven Development (SDD)** con **OpenSpec** y **Active Stack**.

El sistema resuelve la problemática de asignación de turnos concurrentes y reglas de negocio complejas mediante una arquitectura robusta donde las invariantes críticas están garantizadas directamente a nivel de base de datos (PostgreSQL 16) y reforzadas en el dominio:

### Reglas de Negocio Implementadas (RN01 – RN05)
- **RN01 (Cálculo de fin en servidor):** La hora de finalización del turno no la envía el cliente; la calcula el servidor (`fin = inicio + duracion_min`) según la prestación solicitada.
- **RN02 (Invariante de solapamiento en persistencia):** Doble constraint de exclusión `EXCLUDE USING gist` sobre intervalos semiabiertos `[inicio, fin)` con predicado parcial `WHERE (estado = 'activo')`. Impide solapamientos tanto por **profesional** como por **sillón/box**, resolviendo carreras concurrentes a nivel motor de base de datos sin riesgo de condiciones de carrera en memoria.
- **RN03 (Temporalidad y horarios):** Validación estricta que impide turnos en el pasado o fuera de los horarios de atención configurados para el consultorio.
- **RN04 (Cancelación y liberación de slot):** Cancelación idempotente con registro de auditoría (`cancelled_at`). Al pasar a `cancelado`, el slot se libera de inmediato para nuevas reservas.
- **RN05 (Límite de turnos por paciente):** Restricción de máximo 1 turno activo por paciente por día calendario mediante un índice parcial único en PostgreSQL, previniendo acaparamientos de turnos.

### Módulos y Casos de Uso Soportados
1. **Catálogos Públicos:** Consulta abierta de profesionales activos, sillones y prestaciones con sus duraciones.
2. **Disponibilidad en Tiempo Real:** Cálculo funcional y determinista de slots libres respetando horarios, turnos ocupados y descartando el pasado.
3. **Agenda para Profesionales:** Visualización ordenada cronológicamente de la agenda diaria por profesional, con control de acceso RBAC (`API_KEY_ODONTOLOGO`), prevención de acceso a agendas ajenas (HTTP 403) y filtros opcionales de cancelados.
4. **Alta de Turnos por Recepcionista:** Asignación transaccional con diferenciación reactiva de errores (`409` por conflicto de sillón/profesional vs `422` por validación).
5. **Reprogramación Atómica:** Cambio de horario en una única transacción de base de datos (`POST /turnos/{id}/reprogramacion`). Si el nuevo slot presenta conflicto, se ejecuta un **rollback total**, garantizando que el turno original permanezca activo sin pérdida de datos.
6. **Portal Público de Reservas Guest:** Autoservicio para pacientes sin login con autoasignación inteligente de sillón disponible, emisión de token seguro de cancelación y cancelación idempotente por token.
7. **Interfaz Web Frontend Vanilla:** Aplicación web moderna y modular (HTML5 semántico, CSS moderno y JavaScript ES nativo) servida directamente por FastAPI a través de `StaticFiles`, sin requerir Node.js, Vite ni herramientas de build externas.

---

## 🛠️ Requisitos Previos

Antes de comenzar, asegurate de tener instaladas las siguientes herramientas en tu computadora:

- **Python 3.12 o superior** (verificado y compatible con Python 3.12, 3.13 y 3.14).
- **Docker y Docker Compose** (para ejecutar el contenedor de base de datos PostgreSQL 16 con la extensión `btree_gist`).
- **Git** (para clonar el repositorio).

---

## 🚀 Guía de Instalación y Puesta en Marcha (Paso a Paso)

Seguí estos pasos en orden para levantar el proyecto desde cero en tu máquina local sin errores:

### Paso 1: Clonar el repositorio y situarse en la carpeta
Abrí una terminal (PowerShell en Windows o Bash en Linux/macOS):
```bash
git clone <URL_DEL_REPOSITORIO>
cd turnos-odontologia
```

### Paso 2: Crear y activar el entorno virtual de Python
Desde la raíz del proyecto (`turnos-odontologia`):

**En Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**En Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

*(Verificá que la terminal muestre el prefijo `(.venv)` indicando que el entorno virtual está activo).*

### Paso 3: Instalar las dependencias del proyecto
Con el entorno virtual activado, instalá el paquete del backend en modo editable junto con `uvicorn`:
```bash
cd backend
pip install -e .
pip install uvicorn
```

### Paso 4: Configurar las variables de entorno (`.env`)
Dentro de la carpeta `backend/`, copiá la plantilla de variables de entorno:

**En Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**En Linux / macOS:**
```bash
cp .env.example .env
```

> [!NOTE]
> El archivo `.env.example` ya viene configurado con los valores óptimos para desarrollo local:
> - `DATABASE_URL=postgresql+psycopg://turnos:turnos-dev@127.0.0.1:5433/turnos`  
>   *(Se utiliza el puerto **5433** en el host para evitar cualquier conflicto si tenés otra instancia de PostgreSQL corriendo localmente en el puerto default 5432).*
> - `API_KEY_RECEPCION=dev-recepcion-123`
> - `API_KEY_ODONTOLOGO=dev-odonto-123`
> - `NOTIF_BACKEND=mock`

### Paso 5: Levantar la base de datos con Docker
Desde la raíz del proyecto (`turnos-odontologia`):
```bash
docker compose up -d db
```
Podés verificar que el contenedor esté corriendo y saludable con:
```bash
docker compose ps
```
*(Debe figurar el servicio `turnos-odontologia-db-1` en estado `healthy` o `running` escuchando en `127.0.0.1:5433`).*

### Paso 6: Aplicar las migraciones de base de datos
Con el entorno virtual activo, ejecutá las migraciones de Alembic desde la carpeta `backend/` para crear el esquema, los índices GiST y las reglas de integridad:
```bash
cd backend
python -m alembic upgrade head
```
*(Esto aplicará las versiones `001` de tablas base, `002` de doble constraint EXCLUDE, `003` de ajustes de alcance, `004` de columna e índice para cancelación, y `005` de token único y constraint RN05).*

### Paso 7: Sembrar los datos de prueba (Seed)
Para cargar datos sintéticos iniciales (profesionales, sillones, prestaciones de 30/45/90 min, horarios de atención semanales y turnos de ejemplo):
```bash
python -m app.seed
```
*Salida esperada:* `{'seed': 'ok', 'profesionales': 2, 'sillones': 2, 'prestaciones': 3}` *(o `{'seed': 'ya existente'}` si ya se había ejecutado).*

### Paso 8: Iniciar el servidor de desarrollo
Iniciá FastAPI con Uvicorn:
```bash
python -m uvicorn app.main:app --reload
```
El servidor quedará escuchando en `http://127.0.0.1:8000`.

---

## 🖥️ Acceso a la Aplicación y Uso del Frontend

Una vez iniciado el servidor:

1. **Frontend Web Integrado:** Accedé desde tu navegador a:  
   👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**  
   *(Servido como estático Vanilla en el mismo origen por FastAPI, sin necesidad de compilar nada).*

2. **Documentación Swagger / OpenAPI:**  
   👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**  
   👉 **[http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)**

### Credenciales de Prueba para el Frontend
En la esquina superior del frontend podés ingresar la clave correspondiente según el rol que quieras probar (se guarda en memoria de sesión):

| Rol | Clave de Acceso (API Key) | Pantallas Disponibles |
|---|---|---|
| **Público (Guest)** | *(No requiere clave)* | • **Reserva Pública:** Seleccionar profesional, prestación, ver slots y reservar con autoasignación de sillón y token.<br>• **Cancelar Reserva:** Cancelar un turno guest ingresando su token. |
| **Recepcionista** | `dev-recepcion-123` | • **Dar Turno:** Alta de turno con validación inmediata de conflictos de sillón o profesional (RN02) y límite diario (RN05).<br>• **Reprogramar / Cancelar:** Reprogramación atómica con rollback o cancelación directa liberando el slot. |
| **Odontólogo** | `dev-odonto-123` | • **Agenda Diaria:** Ver turnos asignados por fecha con desglose de paciente, prestación y sillón, con filtro para incluir o excluir turnos cancelados. |

---

## 🧪 Ejecución de Tests Automatizados

La suite de pruebas automatizadas contiene **84 tests** que verifican el 100% de los requerimientos, las reglas de negocio puras, los contratos de API y las condiciones de concurrencia reales.

> [!IMPORTANT]
> Los tests corren contra la instancia real de **PostgreSQL 16 en Docker** (no usan SQLite ni mocks de base de datos) para garantizar que las extensiones `btree_gist` y las exclusiones de concurrencia funcionen exactamente como en producción.

Con la base de datos levantada (`docker compose up -d db`) y el entorno virtual activo:
```bash
cd backend
python -m pytest -v
```

### Cobertura de la Suite de Tests:
- `test_rules.py`: Reglas RN01 y RN03 como funciones puras y deterministas en Python.
- `test_rn02_solapamiento.py` y `test_rn02_concurrencia.py`: Doble eje profesional/sillón, intervalos semiabiertos `[)`, slots liberados tras cancelación y 2 solicitudes concurrentes al mismo slot con un solo ganador (201 vs 409).
- `test_rn05_indice_parcial.py` y `test_rn05_limite_paciente.py`: Invariante de 1 turno activo por paciente por día y códigos de error `RN05`.
- `test_cancelacion_api.py`: Cancelación transaccional por recepcionista, idempotencia y liberación de cupo.
- `test_reprogramacion_api.py`: Atomicidad de reprogramación, rollback total si el horario destino está tomado y persistencia del turno original.
- `test_reservas_guest_api.py`: Flujo completo de paciente invitado, emisión y validación de tokens de cancelación, protección contra campos clínicos (Ley 25.326) y concurrencia.
- `test_agenda_odontologo.py`: Control de acceso RBAC, 403 al consultar agendas ajenas y orden cronológico.
- `test_catalogos_api.py` y `test_disponibilidad.py`: Endpoints públicos y cálculo de disponibilidad horaria.
- `test_migracion_004.py` y `test_migracion_005.py`: Migraciones reversibles con preservación de datos e invariantes.
- `test_notificaciones_mock.py`: Notificaciones desacopladas y patrón best-effort post-commit.

---

## 📂 Estructura del Repositorio

```
turnos-odontologia/
├── backend/                   # Backend API con FastAPI y SQLAlchemy Async
│   ├── alembic/versions/      # Migraciones de base de datos (001 a 005)
│   ├── app/
│   │   ├── api/v1/            # Routers (catalogos, disponibilidad, agenda, turnos, reservas)
│   │   ├── application/       # Lógica transaccional (bookings.py, availability.py, reservas.py)
│   │   ├── core/              # Configuración (.env), seguridad y manejo de errores
│   │   ├── domain/            # Modelos SQLAlchemy y reglas puras (models.py, rules.py)
│   │   ├── notifications/     # Servicio de notificaciones desacoplado (mock)
│   │   ├── schemas/           # Schemas Pydantic con extra="forbid"
│   │   ├── main.py            # Fábrica FastAPI y montaje del frontend estático
│   │   └── seed.py            # Script de inicialización de datos de prueba
│   ├── tests/                 # Suite completa de 84 tests con pytest
│   ├── pyproject.toml         # Dependencias y configuración de packaging
│   └── alembic.ini            # Configuración de Alembic
├── frontend/                  # Interfaz de usuario Vanilla (HTML5/CSS3/JS modular)
│   ├── css/app.css            # Estilos modernos y responsivos
│   ├── js/
│   │   ├── screens/           # Vistas (agenda, dar-turno, reprogramar, reserva)
│   │   ├── api.js             # Cliente fetch centralizado para contrato {code, message}
│   │   ├── auth.js            # Manejo de roles y credenciales en memoria
│   │   └── router.js          # Navegación SPA sin recarga
│   └── index.html             # Punto de entrada de la aplicación web
├── knowledge-base/            # Base de conocimiento SDD (10 documentos canónicos de especificación)
├── openspec/                  # Especificaciones activas y changes archivados (C-01 a C-35)
├── docs/                      # Documentación del trabajo (discovery, reflexión, entregables)
├── mcp-skill/                 # Integración de Skill propia (auditor) y Servidor MCP Context7
├── docker-compose.yml         # Orquestación de PostgreSQL 16 con puerto 5433
├── CHANGES.md                 # Roadmap canónico de implementación SDD (100% archivado)
└── README.md                  # Este archivo de documentación
```

---

## 🔧 Resolución de Problemas Frecuentes

- **Error de conexión a la base de datos (`ConnectionRefusedError` o `could not connect to server`):**  
  Asegurate de haber ejecutado `docker compose up -d db` y de que `DATABASE_URL` en tu `backend/.env` utilice el puerto `5433`:
  ```
  DATABASE_URL=postgresql+psycopg://turnos:turnos-dev@127.0.0.1:5433/turnos
  ```
- **Error `ports are not available: exposing port TCP 127.0.0.1:5433`:**  
  Tenés otra aplicación utilizando el puerto 5433. Podés cambiar el puerto del host en `docker-compose.yml` (por ejemplo a `"127.0.0.1:5434:5432"`) y actualizar el puerto en tu `backend/.env`.
- **Lentitud en respuestas (`~10 segundos por conexión`) en Windows:**  
  En algunos sistemas Windows, `localhost` resuelve primero a IPv6. Para evitarlo, asegurate de utilizar siempre `127.0.0.1` en `DATABASE_URL`.
- **Ejecutables `.exe` de `.venv` fallan en Windows:**  
  Si al correr `pytest` o `alembic` la terminal no responde o sale con código de error, utilizá siempre la sintaxis de módulo de Python: `python -m pytest` y `python -m alembic`.
- **Protección de Datos Personales (Ley 25.326):**  
  Todos los datos presentes en el script de seed y en las pruebas son puramente sintéticos y ficticios. Nunca se deben ingresar datos clínicos ni de pacientes reales en este entorno.

---

## 🤖 Integración de MCP y Skill Propia

El proyecto incluye la investigación, desarrollo y configuración de herramientas avanzadas para agentes de IA:

### 1. Skill Propia: `auditor-changes-22-23-29`
- **Ubicación:** `.agents/skills/auditor-changes-22-23-29/SKILL.md` (y espejo en `mcp-skill/auditor-changes-22-23-29/SKILL.md`).
- **Función:** Skill diseñada específicamente para auditar los cambios de la Fase 3 (`C-22`, `C-23`, `C-29`), verificando el cumplimiento estricto de las reglas `RN01` a `RN05`, escenarios con pruebas pytest y protección según Ley 25.326.

### 2. Servidor MCP: `Context7` (`@upstash/context7-mcp`)
- **Configuración:** Disponible en `mcp-skill/config-mcp-ejemplo.json`.
- **Uso:** Servidor MCP que permite consultar documentación canónica en tiempo de diseño (por ejemplo, resolución de consultas sobre el modelo transaccional asíncrono de `SQLAlchemy 2.0`). Las evidencias de su invocación y trazabilidad se documentan en `mcp-skill/evidencias/ejecucion-mcp-context7.md`.
