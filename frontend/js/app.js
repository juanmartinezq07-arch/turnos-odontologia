import { register, startRouter, navigate, getCurrentRoute, onRouteChange } from "./router.js";
import { apiFetch } from "./api.js";
import {
  getAuthState,
  setActiveRole,
  setRecepcionKey,
  setOdontologo,
  setProfesionalId,
  clearAuth,
  onAuthChange,
  showToast,
} from "./auth.js";
import { renderAgenda } from "./screens/agenda.js";
import { renderDarTurno } from "./screens/dar-turno.js";
import { renderReprogramar } from "./screens/reprogramar.js";
import { renderReserva } from "./screens/reserva.js";

let cachedProfesionales = [];

const NAV_ITEMS = [
  { path: "/", label: "Inicio", roles: ["guest", "recepcion", "odontologo"] },
  { path: "/reserva", label: "Reserva Pública", roles: ["guest"] },
  { path: "/dar-turno", label: "Dar Turno", roles: ["recepcion"] },
  { path: "/reprogramar", label: "Reprogramar / Cancelar", roles: ["recepcion"] },
  { path: "/agenda", label: "Agenda Diaria", roles: ["odontologo", "recepcion"] },
  { path: "/catalogos", label: "Catálogos", roles: ["guest", "recepcion", "odontologo"] },
];

async function ensureProfesionales() {
  if (cachedProfesionales.length) return cachedProfesionales;
  try {
    cachedProfesionales = await apiFetch("/profesionales");
    const st = getAuthState();
    if (!st.profesionalId && cachedProfesionales[0]) {
      setProfesionalId(cachedProfesionales[0].id);
    }
  } catch {
    cachedProfesionales = [];
  }
  return cachedProfesionales;
}

function renderHeaderControls() {
  const roleBar = document.getElementById("role-bar");
  const navEl = document.getElementById("nav");
  const drawerEl = document.getElementById("auth-drawer");
  const st = getAuthState();
  const route = getCurrentRoute();

  if (roleBar) {
    roleBar.innerHTML = `
      <div class="role-switcher" role="group" aria-label="Seleccionar rol de usuario">
        <span class="role-label">Modo</span>
        <button type="button" class="role-btn ${st.role === "guest" ? "active" : ""}" data-role="guest">
          <span class="role-dot"></span>Paciente Guest
        </button>
        <button type="button" class="role-btn ${st.role === "recepcion" ? "active" : ""}" data-role="recepcion">
          <span class="role-dot"></span>Recepcionista
        </button>
        <button type="button" class="role-btn ${st.role === "odontologo" ? "active" : ""}" data-role="odontologo">
          <span class="role-dot"></span>Odontólogo
        </button>
      </div>
    `;

    roleBar.querySelectorAll("[data-role]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const targetRole = btn.getAttribute("data-role");
        setActiveRole(targetRole);
        if (targetRole === "guest") {
          showToast("Modo Paciente (Guest) activo — sin necesidad de clave", "info");
        } else if (targetRole === "recepcion") {
          showToast("Modo Recepcionista seleccionado", "info");
        } else if (targetRole === "odontologo") {
          showToast("Modo Odontólogo seleccionado", "info");
        }
      });
    });
  }

  if (navEl) {
    navEl.innerHTML = NAV_ITEMS.map((item) => {
      const isActive = route === item.path;
      const isRec = item.roles.includes(st.role) && item.path !== "/" && item.path !== "/catalogos";
      return `<a href="#${item.path}" class="nav-link ${isActive ? "active" : ""} ${isRec ? "recommended" : ""}">${item.label}</a>`;
    }).join("");
  }

  if (drawerEl) {
    if (st.role === "guest") {
      drawerEl.innerHTML = `
        <div class="auth-bar-form">
          <span class="auth-status-pill guest">Portal Público · Sin autenticación</span>
          <button type="button" class="btn-chip-header" id="hdr-quick-recep">Probar Recepción Demo</button>
          <button type="button" class="btn-chip-header" id="hdr-quick-odonto">Probar Odontólogo Demo</button>
        </div>
      `;
      document.getElementById("hdr-quick-recep")?.addEventListener("click", () => {
        setRecepcionKey("dev-recepcion-123");
        showToast("Credencial demo de Recepción cargada en memoria", "success");
        navigate("/dar-turno");
      });
      document.getElementById("hdr-quick-odonto")?.addEventListener("click", async () => {
        const profs = await ensureProfesionales();
        const firstId = profs[0]?.id || st.profesionalId || "";
        setOdontologo("dev-odonto-123", firstId);
        showToast("Credencial demo de Odontólogo cargada en memoria", "success");
        navigate("/agenda");
      });
    } else if (st.role === "recepcion") {
      drawerEl.innerHTML = `
        <div class="auth-bar-form">
          <span class="auth-status-pill ${st.hasRecepcion ? "ok" : "pending"}">
            ${st.hasRecepcion ? "✓ Recepción Autenticada" : "⚠ Clave requerida"}
          </span>
          <input
            type="password"
            id="hdr-recep-key"
            class="auth-input-compact"
            placeholder="API Key Recepción..."
            value="${st.recepcionKey}"
            aria-label="API Key de Recepcionista"
          />
          <button type="button" class="btn-chip-header" id="hdr-save-recep">Aplicar</button>
          <button type="button" class="btn-chip-header" id="hdr-demo-recep">Cargar Demo (dev-recepcion-123)</button>
          ${st.hasRecepcion ? `<button type="button" class="btn-chip-header ghost" id="hdr-clear-auth">Salir</button>` : ""}
        </div>
      `;
      document.getElementById("hdr-save-recep")?.addEventListener("click", () => {
        const val = document.getElementById("hdr-recep-key")?.value || "";
        setRecepcionKey(val);
        showToast(val ? "Credencial de Recepción actualizada en memoria" : "Credencial limpiada", "success");
      });
      document.getElementById("hdr-demo-recep")?.addEventListener("click", () => {
        setRecepcionKey("dev-recepcion-123");
        showToast("Clave demo dev-recepcion-123 activa en memoria", "success");
      });
      document.getElementById("hdr-clear-auth")?.addEventListener("click", () => {
        clearAuth();
        showToast("Sesión en memoria cerrada", "info");
      });
    } else if (st.role === "odontologo") {
      const optionsHtml = cachedProfesionales.length
        ? cachedProfesionales
            .map(
              (p) =>
                `<option value="${p.id}" ${p.id === st.profesionalId ? "selected" : ""}>${p.nombre} ${p.apellido || ""}</option>`
            )
            .join("")
        : `<option value="${st.profesionalId}">Cargando profesionales...</option>`;

      drawerEl.innerHTML = `
        <div class="auth-bar-form">
          <span class="auth-status-pill ${st.hasOdontologo ? "ok" : "pending"}">
            ${st.hasOdontologo ? "✓ Odontólogo Autenticado" : "⚠ Clave requerida"}
          </span>
          <select id="hdr-odonto-prof" class="auth-select-compact" aria-label="Profesional Odontólogo">
            ${optionsHtml}
          </select>
          <input
            type="password"
            id="hdr-odonto-key"
            class="auth-input-compact"
            placeholder="API Key Odontólogo..."
            value="${st.odontologoKey}"
            aria-label="API Key de Odontólogo"
          />
          <button type="button" class="btn-chip-header" id="hdr-save-odonto">Aplicar</button>
          <button type="button" class="btn-chip-header" id="hdr-demo-odonto">Cargar Demo (dev-odonto-123)</button>
          ${st.hasOdontologo ? `<button type="button" class="btn-chip-header ghost" id="hdr-clear-auth">Salir</button>` : ""}
        </div>
      `;
      document.getElementById("hdr-odonto-prof")?.addEventListener("change", (e) => {
        setProfesionalId(e.target.value);
        showToast("Profesional activo actualizado en cabecera", "info");
      });
      document.getElementById("hdr-save-odonto")?.addEventListener("click", () => {
        const keyVal = document.getElementById("hdr-odonto-key")?.value || "";
        const profVal = document.getElementById("hdr-odonto-prof")?.value || "";
        setOdontologo(keyVal, profVal);
        showToast("Credencial de Odontólogo actualizada en memoria", "success");
      });
      document.getElementById("hdr-demo-odonto")?.addEventListener("click", async () => {
        const profs = await ensureProfesionales();
        const profSelect = document.getElementById("hdr-odonto-prof");
        const chosenProf = profSelect?.value || profs[0]?.id || "";
        setOdontologo("dev-odonto-123", chosenProf);
        showToast("Clave demo dev-odonto-123 activa en memoria", "success");
      });
      document.getElementById("hdr-clear-auth")?.addEventListener("click", () => {
        clearAuth();
        showToast("Sesión en memoria cerrada", "info");
      });
    }
  }
}

function homeView(app) {
  app.innerHTML = `
    <div class="card-navy">
      <div class="hero-banner">
        <div>
          <span class="hero-kicker">Clínica Odontológica · Sistema Integral de Turnos</span>
          <h2>Gestión Clínica</h2>
          <p>
            Organizá la atención del consultorio de forma ágil y ordenada. Consultá agendas profesionales,
            administrá la disponibilidad de cada especialidad y facilitá la reserva de turnos online para tus pacientes.
          </p>
        </div>
        <div style="display:flex; gap:0.65rem; flex-wrap:wrap;">
          <button type="button" class="primary" id="hero-btn-reserva" style="background:#38bdf8; color:#06101e; font-weight:700;">
            Reservar Turno Online
          </button>
          <button type="button" id="hero-btn-catalogos" style="background:rgba(255,255,255,0.1); color:#fff; border-color:rgba(186,230,253,0.3);">
            Ver Equipo y Prestaciones
          </button>
        </div>
      </div>
    </div>

    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <div>
          <div class="stat-value" id="stat-profs">—</div>
          <div class="stat-label">Odontólogos Activos</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        </div>
        <div>
          <div class="stat-value" id="stat-sillones">—</div>
          <div class="stat-label">Sillones / Boxes Equipados</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        </div>
        <div>
          <div class="stat-value" id="stat-prestaciones">—</div>
          <div class="stat-label">Prestaciones (30 a 90 min)</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        </div>
        <div>
          <div class="stat-value">Lun – Sáb</div>
          <div class="stat-label">Atención y Reserva Online</div>
        </div>
      </div>
    </div>

    <div class="grid-3" style="margin-bottom: 1.5rem;">
      <div class="portal-card">
        <div>
          <span class="badge badge-ice">Acceso Público · Guest</span>
          <h3>Portal de Pacientes</h3>
          <p>
            Consultá horarios disponibles en tiempo real por odontólogo y prestación, reservá sin crear cuenta
            y gestioná cancelaciones con tu código de reserva.
          </p>
        </div>
        <div class="portal-actions">
          <button type="button" class="primary" id="card-go-reserva">Reservar Turno</button>
          <a href="#/reserva" class="nav-link" style="color:var(--ice-600);">Ir a Reserva Pública →</a>
        </div>
      </div>

      <div class="portal-card">
        <div>
          <span class="badge badge-navy">Rol Recepcionista</span>
          <h3>Recepción y Admisión</h3>
          <p>
            Otorgá turnos asignando sillón/box y profesional con verificación inmediata de disponibilidad,
            o gestioná reprogramaciones y cancelaciones de forma simple y segura.
          </p>
        </div>
        <div class="portal-actions">
          <button type="button" class="primary" id="card-go-darturno">Dar Turno (Demo)</button>
          <button type="button" id="card-go-reprog">Reprogramar / Cancelar</button>
        </div>
      </div>

      <div class="portal-card">
        <div>
          <span class="badge badge-activo">Rol Odontólogo</span>
          <h3>Agenda Clínica Diaria</h3>
          <p>
            Visualizá tu cronograma diario ordenado por horario con detalle de prestación, duración,
            box asignado y paciente, con control de acceso por profesional.
          </p>
        </div>
        <div class="portal-actions">
          <button type="button" class="primary" id="card-go-agenda">Abrir Mi Agenda (Demo)</button>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="page-header" style="margin-bottom:0.75rem;">
        <div class="page-title-group">
          <h2>Información de Atención del Consultorio</h2>
          <p class="page-subtitle">Navegación directa: <a href="#/agenda">Agenda</a> · <a href="#/dar-turno">Dar turno</a> · <a href="#/reprogramar">Reprogramar/Cancelar</a> · <a href="#/reserva">Reserva pública</a> · <a href="#/catalogos">Catálogos</a></p>
        </div>
      </div>
      <div class="grid-2">
        <div class="card-subtle">
          <strong>Especialidades y Duración de Turnos</strong>
          <p style="margin:0.35rem 0 0; font-size:0.85rem; color:var(--muted);">
            Cada consulta se agenda contemplando el tiempo estimado según el tratamiento seleccionado (30, 45 o 90 minutos) y la disponibilidad del profesional y su consultorio.
          </p>
        </div>
        <div class="card-subtle">
          <strong>Horarios de Atención y Cancelaciones</strong>
          <p style="margin:0.35rem 0 0; font-size:0.85rem; color:var(--muted);">
            Atención de lunes a viernes de 09:00 a 18:00 hs y sábados de 09:00 a 12:00 hs. Las cancelaciones o cambios de horario liberan el lugar de inmediato para otros pacientes.
          </p>
        </div>
      </div>
    </div>
  `;

  document.getElementById("hero-btn-reserva")?.addEventListener("click", () => {
    setActiveRole("guest");
    navigate("/reserva");
  });
  document.getElementById("hero-btn-catalogos")?.addEventListener("click", () => {
    navigate("/catalogos");
  });
  document.getElementById("card-go-reserva")?.addEventListener("click", () => {
    setActiveRole("guest");
    navigate("/reserva");
  });
  document.getElementById("card-go-darturno")?.addEventListener("click", () => {
    setRecepcionKey("dev-recepcion-123");
    showToast("Modo Recepción activado con clave demo", "success");
    navigate("/dar-turno");
  });
  document.getElementById("card-go-reprog")?.addEventListener("click", () => {
    setRecepcionKey("dev-recepcion-123");
    showToast("Modo Recepción activado con clave demo", "success");
    navigate("/reprogramar");
  });
  document.getElementById("card-go-agenda")?.addEventListener("click", async () => {
    const profs = await ensureProfesionales();
    setOdontologo("dev-odonto-123", profs[0]?.id || "");
    showToast("Modo Odontólogo activado con clave demo", "success");
    navigate("/agenda");
  });

  Promise.all([
    apiFetch("/profesionales"),
    apiFetch("/sillones"),
    apiFetch("/prestaciones"),
  ])
    .then(([profs, sils, pres]) => {
      cachedProfesionales = profs;
      const elP = document.getElementById("stat-profs");
      const elS = document.getElementById("stat-sillones");
      const elPr = document.getElementById("stat-prestaciones");
      if (elP) elP.textContent = String(profs.length);
      if (elS) elS.textContent = String(sils.length);
      if (elPr) elPr.textContent = String(pres.length);
      renderHeaderControls();
    })
    .catch(() => {});
}

function catalogosView(app) {
  app.innerHTML = `
    <div class="card">
      <div class="page-header">
        <div class="page-title-group">
          <h2>Catálogos Clínicos Activos</h2>
          <p class="page-subtitle">Profesionales matriculados, prestaciones odontológicas y boxes de atención.</p>
        </div>
        <span id="out" class="badge badge-ice">Cargando...</span>
      </div>

      <div class="grid-3" id="catalogos-grid">
        <div class="card-subtle">Cargando profesionales...</div>
        <div class="card-subtle">Cargando prestaciones...</div>
        <div class="card-subtle">Cargando sillones...</div>
      </div>
    </div>
  `;

  Promise.all([
    apiFetch("/profesionales"),
    apiFetch("/prestaciones"),
    apiFetch("/sillones"),
  ])
    .then(([profs, pres, sils]) => {
      cachedProfesionales = profs;
      const outEl = document.getElementById("out");
      if (outEl) outEl.textContent = `Profesionales activos: ${profs.length}`;

      const grid = document.getElementById("catalogos-grid");
      if (!grid) return;

      const profsHtml = profs
        .map(
          (p) => `
          <div style="padding:0.75rem; background:#fff; border:1px solid var(--border); border-radius:8px; margin-bottom:0.6rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem;">
              <strong>${p.nombre} ${p.apellido || ""}</strong>
              <span class="badge badge-activo">Activo</span>
            </div>
            <div style="font-size:0.8rem; color:var(--muted); margin-top:0.2rem;">
              Matrícula: <strong>${p.matricula || "M.N. Verificada"}</strong>
            </div>
            <div style="font-size:0.72rem; color:var(--muted); margin-top:0.25rem;" class="code-pill">${p.id}</div>
          </div>`
        )
        .join("");

      const presHtml = pres
        .map(
          (pr) => `
          <div style="padding:0.75rem; background:#fff; border:1px solid var(--border); border-radius:8px; margin-bottom:0.6rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem;">
              <strong>${pr.nombre}</strong>
              <span class="badge badge-ice">${pr.duracion_min} min</span>
            </div>
            <div style="font-size:0.72rem; color:var(--muted); margin-top:0.35rem;" class="code-pill">${pr.id}</div>
          </div>`
        )
        .join("");

      const silsHtml = sils
        .map(
          (s) => `
          <div style="padding:0.75rem; background:#fff; border:1px solid var(--border); border-radius:8px; margin-bottom:0.6rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem;">
              <strong>${s.nombre}</strong>
              <span class="badge badge-navy">Box Equipado</span>
            </div>
            <div style="font-size:0.72rem; color:var(--muted); margin-top:0.35rem;" class="code-pill">${s.id}</div>
          </div>`
        )
        .join("");

      grid.innerHTML = `
        <div class="card-subtle">
          <h3 style="margin-top:0; color:var(--navy-900); font-size:1rem;">Odontólogos (${profs.length})</h3>
          ${profsHtml || '<p class="empty-state">Sin profesionales</p>'}
        </div>
        <div class="card-subtle">
          <h3 style="margin-top:0; color:var(--navy-900); font-size:1rem;">Prestaciones (${pres.length})</h3>
          ${presHtml || '<p class="empty-state">Sin prestaciones</p>'}
        </div>
        <div class="card-subtle">
          <h3 style="margin-top:0; color:var(--navy-900); font-size:1rem;">Sillones / Boxes (${sils.length})</h3>
          ${silsHtml || '<p class="empty-state">Sin sillones</p>'}
        </div>
      `;
    })
    .catch((e) => {
      const el = document.getElementById("out");
      if (el) el.textContent = `Error: ${e.code} — ${e.message}`;
    });
}

register("/", homeView);
register("/catalogos", catalogosView);
register("/agenda", renderAgenda);
register("/dar-turno", renderDarTurno);
register("/reprogramar", renderReprogramar);
register("/reserva", renderReserva);

onAuthChange(() => renderHeaderControls());
onRouteChange(() => renderHeaderControls());

ensureProfesionales().then(() => {
  renderHeaderControls();
});

startRouter();
renderHeaderControls();
