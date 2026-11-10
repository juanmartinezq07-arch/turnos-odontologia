import { apiFetch, ApiError } from "../api.js";
import {
  authHeaders,
  getAuthState,
  setRecepcionKey,
  showToast,
  copyToClipboard,
  dateOffsetISO,
  nextMondayISO,
  formatHour,
  nextDemoPatient,
  rememberTurno,
  setPendingTurnoId,
} from "../auth.js";
import { navigate } from "../router.js";

export function renderDarTurno(app) {
  const defaultDate = nextMondayISO();

  app.innerHTML = `
    <div class="card">
      <div class="page-header">
        <div class="page-title-group">
          <h2>Alta de Turno en Recepción</h2>
          <p class="page-subtitle">
            Asignación de profesional, prestación y consultorio con verificación de horarios disponibles en tiempo real.
          </p>
        </div>
        <span class="badge badge-navy">Admisión · Rol Recepcionista</span>
      </div>

      <div id="dt-auth-banner"></div>

      <form id="f">
        <div class="grid-sidebar">
          <div class="card-subtle">
            <h3 style="margin-top:0; font-size:1rem; color:var(--navy-900);">1. Profesional, Box y Horario</h3>

            <div class="form-row" style="margin-bottom:0.85rem;">
              <label>
                Profesional Odontólogo
                <select name="profesional_id" id="prof" required></select>
              </label>

              <label>
                Prestación Clínica
                <select name="prestacion_id" id="pres" required></select>
              </label>
            </div>

            <div class="form-row" style="margin-bottom:0.85rem;">
              <label>
                Sillón / Box Asignado
                <select name="sillon_id" id="sil" required></select>
              </label>

              <label>
                Fecha del Turno
                <input name="fecha" id="dt-fecha" type="date" value="${defaultDate}" required />
                <div class="quick-chips">
                  <button type="button" class="chip-btn" data-dt-date="${dateOffsetISO(0)}">Hoy</button>
                  <button type="button" class="chip-btn" data-dt-date="${dateOffsetISO(1)}">Mañana</button>
                  <button type="button" class="chip-btn" data-dt-date="${nextMondayISO()}">Próx. Lunes</button>
                </div>
              </label>
            </div>

            <div class="form-row" style="align-items:end; margin-bottom:0.85rem;">
              <label>
                Hora de Inicio (HH:MM)
                <input name="hora" id="dt-hora" type="time" value="09:00" required />
              </label>
              <div>
                <button type="button" id="btn-dt-slots" style="width:100%;">
                  Consultar Horarios Libres
                </button>
              </div>
            </div>

            <div class="slots-panel">
              <div class="slots-header">
                <span class="slots-title">Horarios disponibles en tiempo real (clic para elegir)</span>
                <span id="dt-slots-count" class="badge badge-ice">—</span>
              </div>
              <div id="slots" class="slots-grid"></div>
            </div>
          </div>

          <div>
            <fieldset style="margin-bottom:1rem;">
              <legend>2. Datos de Contacto del Paciente</legend>
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; flex-wrap:wrap; gap:0.5rem;">
                <span style="font-size:0.78rem; color:var(--muted);">Datos de contacto para confirmación del turno</span>
                <button type="button" class="sm chip-btn" id="btn-demo-patient">Autocompletar Paciente Demo</button>
              </div>

              <div style="display:flex; flex-direction:column; gap:0.85rem;">
                <label>
                  Nombre y Apellido
                  <input name="nombre" id="dt-nombre" placeholder="Ej: Lucía Fernández Demo" required />
                </label>
                <label>
                  Teléfono de Contacto
                  <input name="telefono" id="dt-tel" placeholder="Ej: 11-4501-1122" />
                </label>
                <label>
                  Correo Electrónico
                  <input name="email" id="dt-email" type="email" placeholder="Ej: paciente.demo@example.com" />
                </label>
              </div>
            </fieldset>

            <button type="submit" class="primary" style="width:100%; padding:0.8rem 1.2rem; font-size:0.95rem;">
              Confirmar y Crear Turno
            </button>

            <div id="msg" class="feedback-box"></div>
          </div>
        </div>
      </form>
    </div>
  `;

  const msg = document.getElementById("msg");
  const profSel = document.getElementById("prof");
  const presSel = document.getElementById("pres");
  const silSel = document.getElementById("sil");
  const fechaInput = document.getElementById("dt-fecha");
  const horaInput = document.getElementById("dt-hora");
  const slotsBox = document.getElementById("slots");
  const slotsCount = document.getElementById("dt-slots-count");
  const authBanner = document.getElementById("dt-auth-banner");

  function renderBanner() {
    const st = getAuthState();
    if (!authBanner) return;
    if (!st.hasRecepcion) {
      authBanner.innerHTML = `
        <div class="cred-banner">
          <div class="cred-banner-text">
            <strong>Requiere credencial de Recepcionista:</strong>
            Activá la clave demo en memoria para habilitar el alta de turnos (<span class="code-pill">POST /turnos</span>).
          </div>
          <button type="button" class="sm primary" id="btn-dt-auth">Activar Recepción Demo (dev-recepcion-123)</button>
        </div>
      `;
      document.getElementById("btn-dt-auth")?.addEventListener("click", () => {
        setRecepcionKey("dev-recepcion-123");
        showToast("Credencial de Recepcionista activa en memoria", "success");
        renderBanner();
      });
    } else {
      authBanner.innerHTML = "";
    }
  }

  async function loadDisponibilidad() {
    const pid = profSel.value;
    const presId = presSel.value;
    const fecha = fechaInput.value;
    if (!pid || !presId || !fecha) return;

    slotsBox.innerHTML = `<span style="font-size:0.84rem; color:var(--muted);">Consultando disponibilidad...</span>`;
    try {
      const data = await apiFetch(
        `/disponibilidad?profesional_id=${encodeURIComponent(pid)}&fecha=${encodeURIComponent(fecha)}&prestacion_id=${encodeURIComponent(presId)}`
      );
      slotsBox.innerHTML = "";
      if (slotsCount) slotsCount.textContent = `${data.length} libres`;

      if (!data.length) {
        slotsBox.innerHTML = `<span style="font-size:0.84rem; color:var(--muted); grid-column: 1 / -1;">Sin slots disponibles en esta fecha (probá un día hábil Lun–Sáb).</span>`;
        return;
      }

      for (const s of data) {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "slot-btn";
        const hhmm = formatHour(s.inicio);
        const finHhmm = formatHour(s.fin);
        if (horaInput.value === hhmm) b.classList.add("primary");

        b.innerHTML = `
          <span>${hhmm}</span>
          <span class="slot-sub">hasta ${finHhmm}</span>
        `;
        b.addEventListener("click", () => {
          horaInput.value = hhmm;
          slotsBox.querySelectorAll("button").forEach((x) => x.classList.remove("primary"));
          b.classList.add("primary");
          showToast(`Horario seleccionado: ${hhmm} a ${finHhmm}`, "info");
        });
        slotsBox.appendChild(b);
      }
    } catch (e) {
      if (slotsCount) slotsCount.textContent = "Error";
      slotsBox.innerHTML = `<span style="font-size:0.82rem; color:var(--danger); grid-column: 1 / -1;">No se pudo consultar disponibilidad (${e.code}).</span>`;
    }
  }

  renderBanner();

  // Cargar catálogos
  Promise.all([
    apiFetch("/profesionales"),
    apiFetch("/prestaciones"),
    apiFetch("/sillones"),
  ])
    .then(([profs, pres, sils]) => {
      for (const p of profs) {
        profSel.add(new Option(`${p.nombre} ${p.apellido || ""}`, p.id));
      }
      for (const p of pres) {
        presSel.add(new Option(`${p.nombre} (${p.duracion_min}min)`, p.id));
      }
      for (const s of sils) {
        silSel.add(new Option(s.nombre, s.id));
      }
      loadDisponibilidad();
    })
    .catch((e) => {
      msg.className = "feedback-box error";
      msg.textContent = `Error cargando catálogos: ${e.code}`;
    });

  profSel.addEventListener("change", loadDisponibilidad);
  presSel.addEventListener("change", loadDisponibilidad);
  fechaInput.addEventListener("change", loadDisponibilidad);
  document.getElementById("btn-dt-slots")?.addEventListener("click", loadDisponibilidad);

  app.querySelectorAll("[data-dt-date]").forEach((btn) => {
    btn.addEventListener("click", () => {
      fechaInput.value = btn.getAttribute("data-dt-date");
      loadDisponibilidad();
    });
  });

  document.getElementById("btn-demo-patient")?.addEventListener("click", () => {
    const p = nextDemoPatient();
    document.getElementById("dt-nombre").value = p.nombre;
    document.getElementById("dt-tel").value = p.telefono;
    document.getElementById("dt-email").value = p.email;
    showToast(`Datos cargados: ${p.nombre}`, "info");
  });

  document.getElementById("f").addEventListener("submit", async (e) => {
    e.preventDefault();
    renderBanner();
    const fd = new FormData(e.target);
    const inicio = `${fd.get("fecha")}T${fd.get("hora")}:00`;
    const payload = {
      profesional_id: fd.get("profesional_id"),
      prestacion_id: fd.get("prestacion_id"),
      inicio,
      paciente: {
        nombre: fd.get("nombre"),
        telefono: fd.get("telefono") || null,
        email: fd.get("email") || null,
      },
    };
    const sillon = fd.get("sillon_id");
    if (sillon) payload.sillon_id = sillon;

    msg.className = "feedback-box info";
    msg.textContent = "Creando...";

    try {
      const t = await apiFetch("/turnos", {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify(payload),
      });
      rememberTurno(t, `${payload.paciente.nombre} (${formatHour(t.inicio)})`);
      msg.className = "feedback-box success";
      msg.innerHTML = `
        <div><strong>✓ Turno creado: ${t.id} (fin ${t.fin})</strong></div>
        <div style="font-size:0.82rem; margin-top:0.35rem;">
          Horario: <strong>${formatHour(t.inicio)} – ${formatHour(t.fin)}</strong> · Estado: <span class="badge badge-activo">${t.estado}</span>
        </div>
        <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:0.65rem;">
          <button type="button" class="sm" id="btn-copy-created">Copiar ID del Turno</button>
          <button type="button" class="sm primary" id="btn-go-reprog-created">Reprogramar / Cancelar este Turno</button>
        </div>
      `;
      showToast("Turno registrado exitosamente", "success");
      loadDisponibilidad();

      document.getElementById("btn-copy-created")?.addEventListener("click", () => {
        copyToClipboard(t.id, "ID de turno copiado");
      });
      document.getElementById("btn-go-reprog-created")?.addEventListener("click", () => {
        setPendingTurnoId(t.id);
        navigate("/reprogramar");
      });
    } catch (err) {
      msg.className = "feedback-box error";
      if (err instanceof ApiError) {
        const m = {
          RN02_PROFESIONAL: "El profesional ya tiene un turno en ese horario.",
          RN02_SILLON: "El sillón ya está ocupado en ese horario.",
          RN05: "El paciente ya tiene un turno ese día.",
          RN03_PASADO: "No se puede agendar un turno en una fecha u hora pasada.",
          RN03_FUERA_DE_HORARIO: "El horario elegido está fuera de la franja de atención del consultorio.",
        }[err.code];
        msg.textContent = m || `Error: ${err.code} — ${err.message}`;
        if (err.status === 401) msg.textContent = "Ingresá una credencial de recepción válida.";
        if (err.status === 422 && !m) msg.textContent = `Validación: ${err.message}`;
        showToast(msg.textContent, "error");
      } else {
        msg.textContent = `Error: ${err.message}`;
      }
    }
  });
}
