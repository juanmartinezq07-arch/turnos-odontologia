import { apiFetch } from "../api.js";
import {
  authHeaders,
  getAuthState,
  setRecepcionKey,
  showToast,
  copyToClipboard,
  dateOffsetISO,
  nextMondayISO,
  formatHour,
  getRecentTurnos,
  rememberTurno,
  consumePendingTurnoId,
} from "../auth.js";

function toDatetimeLocalValue(isoStr) {
  if (!isoStr) return "";
  const d = new Date(isoStr);
  if (Number.isNaN(d.getTime())) {
    return String(isoStr).slice(0, 16);
  }
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  const hh = String(d.getHours()).padStart(2, "0");
  const min = String(d.getMinutes()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}T${hh}:${min}`;
}

export function renderReprogramar(app) {
  const preselectedId = consumePendingTurnoId() || "";
  const defaultSearchDate = nextMondayISO();

  app.innerHTML = `
    <div class="card">
      <div class="page-header">
        <div class="page-title-group">
          <h2>Reprogramación y Cancelación de Turnos</h2>
          <p class="page-subtitle">
            Gestión de cambios de horario y cancelaciones con actualización inmediata de la disponibilidad en agenda.
          </p>
        </div>
        <span class="badge badge-navy">Gestión de Turnos · Recepción</span>
      </div>

      <div id="rep-auth-banner"></div>

      <div class="card-subtle" style="margin-bottom: 1.5rem;">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:1rem; flex-wrap:wrap; margin-bottom:0.75rem;">
          <div>
            <strong style="color:var(--navy-900); font-size:0.95rem;">Selector Rápido de Turnos desde Agenda</strong>
            <div style="font-size:0.8rem; color:var(--muted);">
              Buscá turnos por odontólogo y fecha para seleccionarlos en 1 clic sin copiar UUIDs manualmente.
            </div>
          </div>
          <div style="display:flex; gap:0.5rem; align-items:center; flex-wrap:wrap;">
            <select id="finder-prof" style="width:auto; min-width:200px;"></select>
            <input type="date" id="finder-fecha" value="${defaultSearchDate}" style="width:auto;" />
            <button type="button" class="sm primary" id="btn-finder-load">Buscar Turnos</button>
          </div>
        </div>

        <div id="recent-turnos-bar" style="margin-bottom:0.6rem;"></div>
        <div id="finder-results"></div>
      </div>

      <div class="grid-2">
        <section class="card-subtle">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
            <h3 style="margin:0; color:var(--navy-900); font-size:1.05rem;">Cancelar Turno</h3>
            <span class="badge badge-cancelado">Liberación inmediata</span>
          </div>

          <form id="fc">
            <label>
              ID del Turno a Cancelar
              <input name="id" id="fc-id" value="${preselectedId}" placeholder="UUID del turno..." required />
            </label>
            <button type="submit" class="danger">Cancelar Turno y Liberar Slot</button>
          </form>
          <p id="mc" class="feedback-box"></p>
        </section>

        <section class="card-subtle">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
            <h3 style="margin:0; color:var(--navy-900); font-size:1.05rem;">Reprogramar Turno</h3>
            <span class="badge badge-ice">Cambio de horario</span>
          </div>

          <form id="fr">
            <label>
              ID del Turno Original
              <input name="id" id="fr-id" value="${preselectedId}" placeholder="UUID del turno activo..." required />
            </label>

            <label>
              Sillón / Box Destino (opcional)
              <select name="sillon_id" id="fr-sillon">
                <option value="">(Mantener sillón original del turno)</option>
              </select>
            </label>

            <div class="slots-panel" style="background:#fff;">
              <div class="slots-header">
                <span class="slots-title">Asistente de horarios disponibles</span>
                <button type="button" class="sm chip-btn" id="btn-fr-slots">Ver slots libres</button>
              </div>
              <div class="form-row" style="margin-bottom:0.65rem;">
                <select id="fr-slot-prof" aria-label="Profesional para consultar slots"></select>
                <select id="fr-slot-pres" aria-label="Prestación para consultar slots"></select>
                <input type="date" id="fr-slot-fecha" value="${defaultSearchDate}" aria-label="Fecha para consultar slots" />
              </div>
              <div id="fr-slots-grid" class="slots-grid"></div>
            </div>

            <label>
              Nuevo Inicio (Fecha y Hora)
              <input name="inicio" id="fr-inicio" type="datetime-local" value="${defaultSearchDate}T10:30" required />
            </label>

            <button type="submit" class="primary">Confirmar Reprogramación</button>
          </form>
          <p id="mr" class="feedback-box"></p>
        </section>
      </div>
    </div>
  `;

  const mc = document.getElementById("mc");
  const mr = document.getElementById("mr");
  const fcId = document.getElementById("fc-id");
  const frId = document.getElementById("fr-id");
  const frSillon = document.getElementById("fr-sillon");
  const frInicio = document.getElementById("fr-inicio");
  const finderProf = document.getElementById("finder-prof");
  const finderFecha = document.getElementById("finder-fecha");
  const finderResults = document.getElementById("finder-results");
  const recentBar = document.getElementById("recent-turnos-bar");
  const authBanner = document.getElementById("rep-auth-banner");
  const frSlotProf = document.getElementById("fr-slot-prof");
  const frSlotPres = document.getElementById("fr-slot-pres");
  const frSlotFecha = document.getElementById("fr-slot-fecha");
  const frSlotsGrid = document.getElementById("fr-slots-grid");

  function renderAuthBanner() {
    const st = getAuthState();
    if (!authBanner) return;
    if (!st.hasRecepcion) {
      authBanner.innerHTML = `
        <div class="cred-banner">
          <div class="cred-banner-text">
            <strong>Requiere credencial de Recepcionista:</strong>
            Activá la clave demo en memoria para cancelar, reprogramar o buscar en todas las agendas.
          </div>
          <button type="button" class="sm primary" id="btn-rep-auth">Activar Recepción Demo (dev-recepcion-123)</button>
        </div>
      `;
      document.getElementById("btn-rep-auth")?.addEventListener("click", () => {
        setRecepcionKey("dev-recepcion-123");
        showToast("Credencial de Recepcionista activa en memoria", "success");
        renderAuthBanner();
        loadFinderTurnos();
      });
    } else {
      authBanner.innerHTML = "";
    }
  }

  function renderRecentTurnos() {
    const recents = getRecentTurnos();
    if (!recentBar) return;
    if (!recents.length) {
      recentBar.innerHTML = "";
      return;
    }
    recentBar.innerHTML = `
      <div class="quick-chips">
        <span style="font-size:0.75rem; color:var(--muted); font-weight:600;">Recientes en sesión:</span>
        ${recents
          .map(
            (r) => `
            <button type="button" class="chip-btn btn-pick-recent" data-id="${r.id}">
              ${r.label || r.id.slice(0, 8)} (${r.estado})
            </button>`
          )
          .join("")}
      </div>
    `;
    recentBar.querySelectorAll(".btn-pick-recent").forEach((b) => {
      b.addEventListener("click", () => {
        const id = b.getAttribute("data-id");
        fcId.value = id;
        frId.value = id;
        showToast(`Turno ${id.slice(0, 8)}… cargado en ambos formularios`, "info");
      });
    });
  }

  async function loadFinderTurnos() {
    const pid = finderProf.value;
    const fecha = finderFecha.value;
    if (!pid || !fecha) return;
    if (!getAuthState().hasRecepcion && !getAuthState().hasOdontologo) {
      finderResults.innerHTML = `<div style="font-size:0.82rem; color:var(--muted);">Activá la credencial de Recepción arriba para listar turnos de la agenda.</div>`;
      return;
    }
    finderResults.innerHTML = `<div style="font-size:0.82rem; color:var(--muted);">Buscando turnos del día...</div>`;
    try {
      const data = await apiFetch(
        `/agenda?profesional_id=${encodeURIComponent(pid)}&fecha=${encodeURIComponent(fecha)}&incluir_cancelados=true`,
        { headers: authHeaders() }
      );
      if (!data.length) {
        finderResults.innerHTML = `<div style="font-size:0.82rem; color:var(--muted);">No hay turnos registrados para este profesional el ${fecha}.</div>`;
        return;
      }
      finderResults.innerHTML = `
        <div class="table-wrap" style="margin-top:0.5rem;">
          <table>
            <thead>
              <tr>
                <th>Horario</th>
                <th>Paciente</th>
                <th>Prestación / Box</th>
                <th>Estado</th>
                <th>Seleccionar</th>
              </tr>
            </thead>
            <tbody>
              ${data
                .map(
                  (t) => `
                  <tr class="${t.estado === "cancelado" ? "row-cancelado" : ""}">
                    <td><strong>${formatHour(t.inicio)} – ${formatHour(t.fin)}</strong></td>
                    <td>${t.paciente?.nombre || "—"}</td>
                    <td>${t.prestacion?.nombre || ""} · <span class="badge badge-navy">${t.sillon?.nombre || ""}</span></td>
                    <td><span class="badge ${t.estado === "activo" ? "badge-activo" : "badge-cancelado"}">${t.estado}</span></td>
                    <td>
                      <div style="display:flex; gap:0.35rem; flex-wrap:wrap;">
                        <button type="button" class="sm btn-use-both" data-id="${t.id}" data-prof="${t.profesional_id}" data-pres="${t.prestacion?.id || ""}">
                          Seleccionar Turno
                        </button>
                      </div>
                    </td>
                  </tr>`
                )
                .join("")}
            </tbody>
          </table>
        </div>
      `;
      finderResults.querySelectorAll(".btn-use-both").forEach((btn) => {
        btn.addEventListener("click", () => {
          const id = btn.getAttribute("data-id");
          const prof = btn.getAttribute("data-prof");
          const pres = btn.getAttribute("data-pres");
          fcId.value = id;
          frId.value = id;
          if (prof && frSlotProf) frSlotProf.value = prof;
          if (pres && frSlotPres) frSlotPres.value = pres;
          loadReprogSlots();
          showToast(`Turno ${id.slice(0, 8)}… cargado para cancelar o reprogramar`, "success");
        });
      });
    } catch (e) {
      finderResults.innerHTML = `<div style="font-size:0.82rem; color:var(--danger);">No se pudo listar la agenda (${e.code}).</div>`;
    }
  }

  async function loadReprogSlots() {
    const pid = frSlotProf.value;
    const presId = frSlotPres.value;
    const fecha = frSlotFecha.value;
    if (!pid || !presId || !fecha) return;
    frSlotsGrid.innerHTML = `<span style="font-size:0.8rem; color:var(--muted);">Cargando horarios...</span>`;
    try {
      const data = await apiFetch(
        `/disponibilidad?profesional_id=${encodeURIComponent(pid)}&fecha=${encodeURIComponent(fecha)}&prestacion_id=${encodeURIComponent(presId)}`
      );
      frSlotsGrid.innerHTML = "";
      if (!data.length) {
        frSlotsGrid.innerHTML = `<span style="font-size:0.8rem; color:var(--muted); grid-column: 1 / -1;">Sin horarios libres en esta fecha.</span>`;
        return;
      }
      for (const s of data) {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "slot-btn";
        const hhmm = formatHour(s.inicio);
        b.innerHTML = `<span>${hhmm}</span><span class="slot-sub">a ${formatHour(s.fin)}</span>`;
        b.addEventListener("click", () => {
          frInicio.value = toDatetimeLocalValue(s.inicio);
          frSlotsGrid.querySelectorAll("button").forEach((x) => x.classList.remove("primary"));
          b.classList.add("primary");
          showToast(`Nuevo horario cargado: ${hhmm}`, "info");
        });
        frSlotsGrid.appendChild(b);
      }
    } catch {
      frSlotsGrid.innerHTML = `<span style="font-size:0.8rem; color:var(--danger);">Error al consultar slots.</span>`;
    }
  }

  renderAuthBanner();
  renderRecentTurnos();

  Promise.all([
    apiFetch("/profesionales"),
    apiFetch("/prestaciones"),
    apiFetch("/sillones"),
  ])
    .then(([profs, pres, sils]) => {
      for (const p of profs) {
        const label = `${p.nombre} ${p.apellido || ""}`;
        finderProf.add(new Option(label, p.id));
        frSlotProf.add(new Option(label, p.id));
      }
      for (const pr of pres) {
        frSlotPres.add(new Option(`${pr.nombre} (${pr.duracion_min}min)`, pr.id));
      }
      for (const s of sils) {
        frSillon.add(new Option(s.nombre, s.id));
      }
      loadReprogSlots();
      if (getAuthState().hasRecepcion || getAuthState().hasOdontologo) {
        loadFinderTurnos();
      }
    })
    .catch(() => {});

  document.getElementById("btn-finder-load")?.addEventListener("click", loadFinderTurnos);
  finderProf.addEventListener("change", loadFinderTurnos);
  finderFecha.addEventListener("change", loadFinderTurnos);

  document.getElementById("btn-fr-slots")?.addEventListener("click", loadReprogSlots);
  frSlotProf.addEventListener("change", loadReprogSlots);
  frSlotPres.addEventListener("change", loadReprogSlots);
  frSlotFecha.addEventListener("change", loadReprogSlots);

  document.getElementById("fc").addEventListener("submit", async (e) => {
    e.preventDefault();
    renderAuthBanner();
    const id = new FormData(e.target).get("id");
    mc.className = "feedback-box info";
    mc.textContent = "Cancelando...";
    try {
      const t = await apiFetch(`/turnos/${id}/cancelacion`, {
        method: "POST",
        headers: authHeaders(),
      });
      rememberTurno(t);
      renderRecentTurnos();
      loadFinderTurnos();
      mc.className = "feedback-box success";
      mc.textContent = `Cancelado: ${t.id} (${t.estado}, cancelled_at=${t.cancelled_at})`;
      showToast("Turno cancelado y slot liberado", "success");
    } catch (err) {
      mc.className = "feedback-box error";
      if (err.code === "TURNO_NO_ACTIVO") mc.textContent = "El turno ya estaba cancelado.";
      else if (err.status === 404) mc.textContent = "Turno no encontrado.";
      else if (err.status === 401) mc.textContent = "Ingresá credencial de recepción.";
      else mc.textContent = `Error: ${err.code} — ${err.message}`;
      showToast(mc.textContent, "error");
    }
  });

  document.getElementById("fr").addEventListener("submit", async (e) => {
    e.preventDefault();
    renderAuthBanner();
    const fd = new FormData(e.target);
    const id = fd.get("id");
    const inicio = fd.get("inicio");
    const sillon = fd.get("sillon_id");
    const body = { inicio: new Date(inicio).toISOString() };
    if (sillon) body.sillon_id = sillon;

    mr.className = "feedback-box info";
    mr.textContent = "Reprogramando...";
    try {
      const r = await apiFetch(`/turnos/${id}/reprogramacion`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify(body),
      });
      rememberTurno(r.original);
      rememberTurno(r.nuevo, `Reprogramado (${formatHour(r.nuevo.inicio)})`);
      renderRecentTurnos();
      loadFinderTurnos();
      loadReprogSlots();

      mr.className = "feedback-box success";
      mr.innerHTML = `
        <div><strong>OK: original ${r.original.id} (${r.original.estado}), nuevo ${r.nuevo.id} (${r.nuevo.estado})</strong></div>
        <div style="margin-top:0.5rem; display:flex; gap:0.45rem; flex-wrap:wrap;">
          <button type="button" class="sm" id="btn-copy-new-id">Copiar Nuevo ID</button>
          <button type="button" class="sm" id="btn-use-new-id">Cargar Nuevo ID en Formularios</button>
        </div>
      `;
      showToast("Reprogramación atómica exitosa", "success");

      document.getElementById("btn-copy-new-id")?.addEventListener("click", () => {
        copyToClipboard(r.nuevo.id, "Nuevo ID copiado");
      });
      document.getElementById("btn-use-new-id")?.addEventListener("click", () => {
        fcId.value = r.nuevo.id;
        frId.value = r.nuevo.id;
        showToast("Nuevo turno cargado en los formularios", "info");
      });
    } catch (err) {
      mr.className = "feedback-box error";
      const code = err.code || "";
      if (code === "TURNO_NO_ACTIVO") mr.textContent = "El turno original ya estaba cancelado.";
      else if (code.startsWith("RN02")) mr.textContent = "Conflicto de horario en la agenda. El turno original sigue activo.";
      else if (code === "RN05") mr.textContent = "El paciente ya tiene un turno ese día. El turno original sigue activo.";
      else if (code.startsWith("RN03")) mr.textContent = "El horario elegido no es válido. El turno original sigue activo.";
      else if (err.status === 404) mr.textContent = "Turno no encontrado.";
      else if (err.status === 401) mr.textContent = "Ingresá credencial de recepción.";
      else mr.textContent = `Error: ${code} — ${err.message}`;
      showToast(mr.textContent, "error");
    }
  });
}
