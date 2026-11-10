import { apiFetch } from "../api.js";
import {
  showToast,
  copyToClipboard,
  dateOffsetISO,
  nextMondayISO,
  formatHour,
  nextDemoPatient,
  rememberTurno,
} from "../auth.js";

const TOKEN_KEY = "turnos_guest_token";

export function renderReserva(app) {
  const savedToken = localStorage.getItem(TOKEN_KEY) || "";
  const defaultDate = nextMondayISO();

  app.innerHTML = `
    <div class="card">
      <div class="page-header">
        <div class="page-title-group">
          <h2>Portal Público de Reservas (Pacientes)</h2>
          <p class="page-subtitle">
            Reservá tu turno online las 24 hs sin crear cuenta. El sistema asigna automáticamente un sillón disponible y emite un token único de cancelación.
          </p>
        </div>
        <span class="badge badge-ice">Acceso Público · Sin Login</span>
      </div>

      <div class="grid-sidebar">
        <div>
          <form id="f" class="card-subtle">
            <h3 style="margin-top:0; font-size:1.02rem; color:var(--navy-900);">1. Elegí Especialista, Prestación y Fecha</h3>

            <div class="form-row">
              <label>
                Profesional Odontólogo
                <select name="profesional_id" id="prof" required></select>
              </label>

              <label>
                Prestación Solicitada
                <select name="prestacion_id" id="pres" required></select>
              </label>
            </div>

            <div class="form-row" style="align-items:end;">
              <label>
                Fecha Preferida
                <input name="fecha" id="res-fecha" type="date" value="${defaultDate}" required />
                <div class="quick-chips">
                  <button type="button" class="chip-btn" data-res-date="${dateOffsetISO(0)}">Hoy</button>
                  <button type="button" class="chip-btn" data-res-date="${dateOffsetISO(1)}">Mañana</button>
                  <button type="button" class="chip-btn" data-res-date="${nextMondayISO()}">Próx. Lunes</button>
                </div>
              </label>

              <div>
                <button type="button" id="btnSlots" style="width:100%;">
                  Ver disponibilidad
                </button>
              </div>
            </div>

            <div class="slots-panel" style="background:#fff;">
              <div class="slots-header">
                <span class="slots-title">2. Seleccioná un Horario Disponible</span>
                <span id="res-selected-badge" class="badge badge-ice">Ninguno elegido</span>
              </div>
              <div id="slots" class="slots-grid"></div>
            </div>

            <fieldset>
              <legend>3. Tus Datos de Contacto</legend>
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; flex-wrap:wrap; gap:0.5rem;">
                <span style="font-size:0.78rem; color:var(--muted);">Ingresá tus datos de contacto para recibir la confirmación</span>
                <button type="button" class="sm chip-btn" id="btn-res-demo">Autocompletar Paciente Demo</button>
              </div>

              <div class="form-row">
                <label>
                  Nombre y Apellido
                  <input name="nombre" id="res-nombre" placeholder="Ej: Martín Pereyra Demo" required />
                </label>
                <label>
                  Teléfono
                  <input name="telefono" id="res-tel" placeholder="Ej: 11-5802-3344" />
                </label>
                <label>
                  Email
                  <input name="email" id="res-email" type="email" placeholder="Ej: martin.demo@example.com" />
                </label>
              </div>
            </fieldset>

            <input type="hidden" name="inicio" id="inicio" />
            <button type="submit" class="primary" style="padding:0.8rem 1.2rem; font-size:0.95rem;">
              Confirmar Reserva Online
            </button>
          </form>

          <div id="msg" class="feedback-box"></div>
        </div>

        <div>
          <section class="card-subtle">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.65rem;">
              <h3 style="margin:0; font-size:1.02rem; color:var(--navy-900);">Cancelar Reserva con Token</h3>
              <span class="badge badge-cancelado">Autogestión</span>
            </div>
            <p style="margin:0 0 1rem; font-size:0.84rem; color:var(--muted);">
              Si necesitás cancelar tu turno, ingresá el token que recibiste al confirmar tu reserva. El horario se liberará de inmediato.
            </p>

            <form id="fc">
              <label>
                Token de Cancelación
                <input name="token" id="fc-token" value="${savedToken}" placeholder="Pegá aquí tu token único..." required />
              </label>
              <button type="submit" class="danger">Cancelar Mi Reserva</button>
            </form>
            <p id="mc" class="feedback-box"></p>
          </section>
        </div>
      </div>
    </div>
  `;

  const msg = document.getElementById("msg");
  const slots = document.getElementById("slots");
  const inicioInput = document.getElementById("inicio");
  const profSel = document.getElementById("prof");
  const presSel = document.getElementById("pres");
  const fechaInput = document.getElementById("res-fecha");
  const selectedBadge = document.getElementById("res-selected-badge");
  const fcTokenInput = document.getElementById("fc-token");

  async function fetchSlots() {
    const pid = profSel.value;
    const presId = presSel.value;
    const fecha = fechaInput.value;
    if (!pid || !presId || !fecha) return;

    slots.innerHTML = `<span style="font-size:0.84rem; color:var(--muted);">Cargando...</span>`;
    try {
      const data = await apiFetch(
        `/disponibilidad?profesional_id=${encodeURIComponent(pid)}&fecha=${encodeURIComponent(fecha)}&prestacion_id=${encodeURIComponent(presId)}`
      );
      slots.innerHTML = "";
      for (const s of data) {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "slot-btn";
        const hhmm = formatHour(s.inicio);
        const finHhmm = formatHour(s.fin);
        b.innerHTML = `
          <span>${hhmm}</span>
          <span class="slot-sub">a ${finHhmm}</span>
        `;
        b.addEventListener("click", () => {
          inicioInput.value = s.inicio;
          slots.querySelectorAll("button").forEach((x) => x.classList.remove("primary"));
          b.classList.add("primary");
          if (selectedBadge) {
            selectedBadge.className = "badge badge-activo";
            selectedBadge.textContent = `Elegido: ${hhmm}`;
          }
          showToast(`Horario elegido: ${hhmm}`, "info");
        });
        slots.appendChild(b);
      }
      if (!data.length) {
        slots.textContent = "Sin slots disponibles.";
      } else if (!inicioInput.value && data[0]) {
        // Pre-seleccionar el primer slot libre para agilizar la reserva
        const firstBtn = slots.querySelector("button");
        if (firstBtn) firstBtn.click();
      }
    } catch (e) {
      slots.textContent = `Error: ${e.code}`;
    }
  }

  Promise.all([apiFetch("/profesionales"), apiFetch("/prestaciones")])
    .then(([profs, pres]) => {
      for (const p of profs) profSel.add(new Option(`${p.nombre} ${p.apellido || ""}`, p.id));
      for (const p of pres) presSel.add(new Option(`${p.nombre} (${p.duracion_min}min)`, p.id));
      fetchSlots();
    })
    .catch((e) => {
      msg.className = "feedback-box error";
      msg.textContent = `Error catálogos: ${e.code}`;
    });

  document.getElementById("btnSlots").addEventListener("click", fetchSlots);
  profSel.addEventListener("change", () => {
    inicioInput.value = "";
    fetchSlots();
  });
  presSel.addEventListener("change", () => {
    inicioInput.value = "";
    fetchSlots();
  });
  fechaInput.addEventListener("change", () => {
    inicioInput.value = "";
    fetchSlots();
  });

  app.querySelectorAll("[data-res-date]").forEach((btn) => {
    btn.addEventListener("click", () => {
      fechaInput.value = btn.getAttribute("data-res-date");
      inicioInput.value = "";
      fetchSlots();
    });
  });

  document.getElementById("btn-res-demo")?.addEventListener("click", () => {
    const p = nextDemoPatient();
    document.getElementById("res-nombre").value = p.nombre;
    document.getElementById("res-tel").value = p.telefono;
    document.getElementById("res-email").value = p.email;
    showToast(`Contacto demo completado: ${p.nombre}`, "info");
  });

  document.getElementById("f").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    if (!fd.get("inicio")) {
      msg.className = "feedback-box warning";
      msg.textContent = "Seleccioná primero un horario disponible en la grilla.";
      showToast("Seleccioná un horario disponible antes de reservar", "warning");
      return;
    }
    const payload = {
      profesional_id: fd.get("profesional_id"),
      prestacion_id: fd.get("prestacion_id"),
      inicio: fd.get("inicio"),
      paciente: {
        nombre: fd.get("nombre"),
        telefono: fd.get("telefono") || null,
        email: fd.get("email") || null,
      },
    };
    msg.className = "feedback-box info";
    msg.textContent = "Reservando...";
    try {
      const t = await apiFetch("/reservas", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      const token = t.token_cancelacion;
      if (token) {
        localStorage.setItem(TOKEN_KEY, token);
        if (fcTokenInput) fcTokenInput.value = token;
      }
      rememberTurno(t, `${payload.paciente.nombre} (${formatHour(t.inicio)})`);
      msg.className = "feedback-box success";
      msg.innerHTML = `
        <div><strong>✓ Reserva creada: ${t.id}. Token: ${token}</strong></div>
        <div style="font-size:0.82rem; margin-top:0.35rem;">
          Horario confirmado: <strong>${formatHour(t.inicio)} – ${formatHour(t.fin)}</strong>
        </div>
        <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:0.6rem;">
          <button type="button" class="sm" id="btn-copy-token">Copiar Token de Cancelación</button>
          <button type="button" class="sm" id="btn-copy-res-id">Copiar ID de Reserva</button>
        </div>
      `;
      showToast("Reserva confirmada y token guardado", "success");
      inicioInput.value = "";
      fetchSlots();

      document.getElementById("btn-copy-token")?.addEventListener("click", () => {
        copyToClipboard(token, "Token copiado");
      });
      document.getElementById("btn-copy-res-id")?.addEventListener("click", () => {
        copyToClipboard(t.id, "ID de reserva copiado");
      });
    } catch (err) {
      msg.className = "feedback-box error";
      if (err.status === 429) msg.textContent = "Demasiados intentos, intentá más tarde.";
      else if (err.code && err.code.startsWith("RN02")) msg.textContent = "El horario seleccionado ya no está disponible.";
      else if (err.code === "RN05") msg.textContent = "Ya tenés un turno ese día.";
      else msg.textContent = `Error: ${err.code || err.status} — ${err.message}`;
      showToast(msg.textContent, "error");
    }
  });

  document.getElementById("fc").addEventListener("submit", async (e) => {
    e.preventDefault();
    const token = new FormData(e.target).get("token") || localStorage.getItem(TOKEN_KEY);
    const mc = document.getElementById("mc");
    mc.className = "feedback-box info";
    mc.textContent = "Cancelando...";
    try {
      const t = await apiFetch(`/reservas/${encodeURIComponent(token)}/cancelacion`, {
        method: "POST",
      });
      mc.className = "feedback-box success";
      mc.textContent = `Cancelado: ${t.id} (${t.estado})`;
      localStorage.removeItem(TOKEN_KEY);
      showToast("Reserva cancelada exitosamente y horario liberado", "success");
      fetchSlots();
    } catch (err) {
      mc.className = "feedback-box error";
      mc.textContent = `Error: ${err.code || err.status} — ${err.message}`;
      showToast(mc.textContent, "error");
    }
  });
}
