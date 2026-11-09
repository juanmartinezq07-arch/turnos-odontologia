import { apiFetch } from "../api.js";
import {
  authHeaders,
  getAuthState,
  setOdontologo,
  setRecepcionKey,
  showToast,
  copyToClipboard,
  dateOffsetISO,
  formatHour,
  rememberTurno,
  setPendingTurnoId,
} from "../auth.js";
import { navigate } from "../router.js";

export function renderAgenda(app) {
  const st = getAuthState();
  const initialDate = dateOffsetISO(1);

  app.innerHTML = `
    <div class="card">
      <div class="page-header">
        <div class="page-title-group">
          <h2>Agenda Clínica Diaria</h2>
          <p class="page-subtitle">
            Cronograma ordenado por horario de inicio con control de acceso por rol (Odontólogo titular o Recepción global).
          </p>
        </div>
        <span class="badge badge-ice">GET /agenda · RBAC Activo</span>
      </div>

      <div id="agenda-auth-banner"></div>

      <form id="f" class="card-subtle" style="margin-bottom: 1.25rem;">
        <div class="form-row">
          <label>
            Profesional Odontólogo
            <select name="profesional_id" id="agenda-prof" required>
              <option value="">Cargando profesionales...</option>
            </select>
          </label>

          <label>
            Fecha de Atención
            <input name="fecha" id="agenda-fecha" type="date" value="${initialDate}" required />
            <div class="quick-chips">
              <button type="button" class="chip-btn" data-day-step="-1">◀ Día ant.</button>
              <button type="button" class="chip-btn" data-day-exact="${dateOffsetISO(0)}">Hoy</button>
              <button type="button" class="chip-btn" data-day-exact="${dateOffsetISO(1)}">Mañana</button>
              <button type="button" class="chip-btn" data-day-step="1">Día sig. ▶</button>
            </div>
          </label>
        </div>

        <div style="display:flex; align-items:center; justify-content:space-between; gap:1rem; flex-wrap:wrap; margin-top:0.25rem;">
          <label class="checkbox-label">
            <input name="incluir_cancelados" type="checkbox" />
            Incluir turnos cancelados en el listado
          </label>

          <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
            <button type="submit" class="primary">Consultar Agenda</button>
          </div>
        </div>
      </form>

      <div id="agenda-stats" class="stats-row" style="display:none;"></div>

      <p id="msg" class="feedback-box info"></p>

      <div class="table-wrap">
        <table id="tbl">
          <thead>
            <tr>
              <th>Horario</th>
              <th>Prestación</th>
              <th>Sillón / Box</th>
              <th>Paciente</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td colspan="6" class="empty-state">Seleccioná profesional y fecha para consultar los turnos del día.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `;

  const form = document.getElementById("f");
  const profSel = document.getElementById("agenda-prof");
  const fechaInput = document.getElementById("agenda-fecha");
  const msg = document.getElementById("msg");
  const statsBox = document.getElementById("agenda-stats");
  const authBanner = document.getElementById("agenda-auth-banner");
  const tbody = document.querySelector("#tbl tbody");

  function updateAuthBanner() {
    const cur = getAuthState();
    if (!authBanner) return;
    if (!cur.hasOdontologo && !cur.hasRecepcion) {
      authBanner.innerHTML = `
        <div class="cred-banner">
          <div class="cred-banner-text">
            <strong>Autenticación requerida para consultar agenda:</strong>
            Podés activar en 1 clic la credencial demo de Odontólogo (acceso a su propia agenda) o de Recepción (acceso global).
          </div>
          <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
            <button type="button" class="sm primary" id="btn-auth-odonto">Activar Odontólogo Demo</button>
            <button type="button" class="sm" id="btn-auth-recep">Activar Recepción Demo</button>
          </div>
        </div>
      `;
      document.getElementById("btn-auth-odonto")?.addEventListener("click", () => {
        const pid = profSel.value || "";
        setOdontologo("dev-odonto-123", pid);
        showToast("Credencial Odontólogo activa para el profesional seleccionado", "success");
        updateAuthBanner();
      });
      document.getElementById("btn-auth-recep")?.addEventListener("click", () => {
        setRecepcionKey("dev-recepcion-123");
        showToast("Credencial Recepción activa (lectura global de agendas)", "success");
        updateAuthBanner();
      });
    } else if (cur.role === "odontologo") {
      authBanner.innerHTML = `
        <div class="cred-banner">
          <div class="cred-banner-text">
            Sesión activa como <strong>Odontólogo</strong> (Titular ID: <span class="code-pill">${cur.profesionalId || "no asignado"}</span>).
            Si consultás otro profesional, el backend responderá <span class="code-pill">403 AGENDA_AJENA</span>.
          </div>
          <button type="button" class="sm" id="btn-sync-prof">Sincronizar credencial con el profesional elegido</button>
        </div>
      `;
      document.getElementById("btn-sync-prof")?.addEventListener("click", () => {
        setOdontologo(cur.odontologoKey || "dev-odonto-123", profSel.value);
        showToast("X-Profesional-Id sincronizado con el selector actual", "success");
        updateAuthBanner();
      });
    } else {
      authBanner.innerHTML = "";
    }
  }

  apiFetch("/profesionales")
    .then((profs) => {
      profSel.innerHTML = "";
      for (const p of profs) {
        const label = `${p.nombre} ${p.apellido || ""}${p.matricula ? ` — Mat. ${p.matricula}` : ""}`;
        profSel.add(new Option(label, p.id));
      }
      if (st.profesionalId && profs.some((p) => p.id === st.profesionalId)) {
        profSel.value = st.profesionalId;
      }
      updateAuthBanner();
      if (getAuthState().hasOdontologo || getAuthState().hasRecepcion) {
        form.requestSubmit();
      }
    })
    .catch((e) => {
      msg.className = "feedback-box error";
      msg.textContent = `Error cargando profesionales: ${e.code}`;
    });

  // Quick date chips
  form.querySelectorAll("[data-day-exact]").forEach((btn) => {
    btn.addEventListener("click", () => {
      fechaInput.value = btn.getAttribute("data-day-exact");
      if (getAuthState().hasOdontologo || getAuthState().hasRecepcion) form.requestSubmit();
    });
  });

  form.querySelectorAll("[data-day-step]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const step = Number(btn.getAttribute("data-day-step") || 0);
      const base = fechaInput.value ? new Date(`${fechaInput.value}T12:00:00`) : new Date();
      base.setDate(base.getDate() + step);
      const yyyy = base.getFullYear();
      const mm = String(base.getMonth() + 1).padStart(2, "0");
      const dd = String(base.getDate()).padStart(2, "0");
      fechaInput.value = `${yyyy}-${mm}-${dd}`;
      if (getAuthState().hasOdontologo || getAuthState().hasRecepcion) form.requestSubmit();
    });
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    updateAuthBanner();
    const fd = new FormData(form);
    const pid = fd.get("profesional_id");
    const fecha = fd.get("fecha");
    const inc = fd.get("incluir_cancelados") ? "true" : "false";

    msg.className = "feedback-box info";
    msg.textContent = "Cargando...";
    tbody.innerHTML = "";

    try {
      const data = await apiFetch(
        `/agenda?profesional_id=${encodeURIComponent(pid)}&fecha=${encodeURIComponent(fecha)}&incluir_cancelados=${inc}`,
        { headers: authHeaders() }
      );
      msg.className = "feedback-box success";
      msg.textContent = `${data.length} turno(s) encontrados para la fecha ${fecha}`;

      const activosCount = data.filter((t) => t.estado === "activo").length;
      const canceladosCount = data.filter((t) => t.estado === "cancelado").length;
      const minutosCount = data
        .filter((t) => t.estado === "activo")
        .reduce((acc, t) => acc + (t.prestacion?.duracion_min || 0), 0);

      if (statsBox) {
        statsBox.style.display = "grid";
        statsBox.innerHTML = `
          <div class="stat-card">
            <div>
              <div class="stat-value">${data.length}</div>
              <div class="stat-label">Turnos Listados</div>
            </div>
          </div>
          <div class="stat-card">
            <div>
              <div class="stat-value" style="color:var(--success-fg);">${activosCount}</div>
              <div class="stat-label">Turnos Activos</div>
            </div>
          </div>
          <div class="stat-card">
            <div>
              <div class="stat-value" style="color:var(--danger-fg);">${canceladosCount}</div>
              <div class="stat-label">Turnos Cancelados</div>
            </div>
          </div>
          <div class="stat-card">
            <div>
              <div class="stat-value">${minutosCount} min</div>
              <div class="stat-label">Carga Clínica Activa</div>
            </div>
          </div>
        `;
      }

      if (!data.length) {
        tbody.innerHTML = `
          <tr>
            <td colspan="6" class="empty-state">No hay turnos registrados para este profesional en la fecha seleccionada.</td>
          </tr>
        `;
        return;
      }

      for (const t of data) {
        rememberTurno(t, `${t.paciente?.nombre || "Paciente"} (${formatHour(t.inicio)})`);
        const tr = document.createElement("tr");
        if (t.estado === "cancelado") {
          tr.style.opacity = "0.5";
          tr.className = "row-cancelado";
        }
        const pres = t.prestacion || {};
        const sil = t.sillon || {};
        const pac = t.paciente || {};
        const horaIni = formatHour(t.inicio);
        const horaFin = formatHour(t.fin);

        tr.innerHTML = `
          <td>
            <strong>${horaIni}${horaFin ? ` – ${horaFin}` : ""}</strong>
            <div style="font-size:0.72rem; color:var(--muted);">${t.inicio}</div>
          </td>
          <td>
            <strong>${pres.nombre || ""}</strong>
            <span class="badge badge-ice">${pres.duracion_min ?? ""}min</span>
          </td>
          <td><span class="badge badge-navy">${sil.nombre || sil.id || ""}</span></td>
          <td>
            <strong>${pac.nombre || pac.id || ""}</strong>
            <div style="font-size:0.76rem; color:var(--muted);">
              ${pac.telefono || ""}${pac.telefono && pac.email ? " · " : ""}${pac.email || ""}
            </div>
          </td>
          <td>
            <span class="badge ${t.estado === "activo" ? "badge-activo" : "badge-cancelado"}">${t.estado}</span>
          </td>
          <td>
            <div style="display:flex; gap:0.35rem; flex-wrap:wrap;">
              <button type="button" class="sm btn-copy-id" data-id="${t.id}">Copiar ID</button>
              <button type="button" class="sm btn-manage-id" data-id="${t.id}">Gestionar</button>
            </div>
          </td>
        `;
        tbody.appendChild(tr);
      }

      tbody.querySelectorAll(".btn-copy-id").forEach((b) => {
        b.addEventListener("click", () => {
          copyToClipboard(b.getAttribute("data-id"), "ID de turno copiado");
        });
      });

      tbody.querySelectorAll(".btn-manage-id").forEach((b) => {
        b.addEventListener("click", () => {
          const id = b.getAttribute("data-id");
          setPendingTurnoId(id);
          setRecepcionKey("dev-recepcion-123");
          showToast("Turno enviado a Reprogramar / Cancelar", "info");
          navigate("/reprogramar");
        });
      });
    } catch (err) {
      if (statsBox) statsBox.style.display = "none";
      msg.className = "feedback-box error";
      if (err.code === "AGENDA_AJENA") {
        msg.textContent = "Solo podés ver tu propia agenda.";
        showToast("Acceso denegado (403 AGENDA_AJENA): intentaste ver otro profesional", "error");
      } else if (err.status === 401) {
        msg.textContent = "Ingresá una credencial válida.";
        showToast("Credencial requerida (401)", "warning");
      } else {
        msg.textContent = `Error: ${err.code} — ${err.message}`;
      }
      tbody.innerHTML = `
        <tr>
          <td colspan="6" class="empty-state">${msg.textContent}</td>
        </tr>
      `;
    }
  });
}
