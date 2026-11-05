import { apiFetch } from "../api.js";

const TOKEN_KEY = "turnos_guest_token";

export function renderReserva(app) {
  app.innerHTML = `
    <div class="card">
      <h2>Reserva pública</h2>
      <form id="f">
        <label>Profesional <select name="profesional_id" id="prof" required></select></label>
        <label>Prestación <select name="prestacion_id" id="pres" required></select></label>
        <label>Fecha <input name="fecha" type="date" required /></label>
        <button type="button" id="btnSlots">Ver disponibilidad</button>
        <div id="slots"></div>
        <fieldset><legend>Contacto</legend>
          <label>Nombre <input name="nombre" required /></label>
          <label>Teléfono <input name="telefono" /></label>
          <label>Email <input name="email" type="email" /></label>
        </fieldset>
        <input type="hidden" name="inicio" id="inicio" />
        <button type="submit" class="primary">Reservar</button>
      </form>
      <p id="msg"></p>
      <section>
        <h3>Cancelar reserva</h3>
        <form id="fc">
          <label>Token <input name="token" required /></label>
          <button type="submit">Cancelar</button>
        </form>
        <p id="mc"></p>
      </section>
    </div>`;
  const msg = document.getElementById("msg");
  const slots = document.getElementById("slots");
  const inicioInput = document.getElementById("inicio");
  const profSel = document.getElementById("prof");
  const presSel = document.getElementById("pres");

  Promise.all([apiFetch("/profesionales"), apiFetch("/prestaciones")]).then(([profs, pres]) => {
    for (const p of profs) profSel.add(new Option(`${p.nombre} ${p.apellido || ""}`, p.id));
    for (const p of pres) presSel.add(new Option(`${p.nombre} (${p.duracion_min}min)`, p.id));
  }).catch((e) => { msg.textContent = `Error catálogos: ${e.code}`; });

  document.getElementById("btnSlots").addEventListener("click", async () => {
    slots.innerHTML = "Cargando...";
    const pid = profSel.value;
    const presId = presSel.value;
    const fecha = document.querySelector('[name="fecha"]').value;
    try {
      const data = await apiFetch(`/disponibilidad?profesional_id=${encodeURIComponent(pid)}&fecha=${encodeURIComponent(fecha)}&prestacion_id=${encodeURIComponent(presId)}`);
      slots.innerHTML = "";
      for (const s of data) {
        const b = document.createElement("button");
        b.type = "button";
        b.textContent = s.inicio;
        b.addEventListener("click", () => { inicioInput.value = s.inicio; slots.querySelectorAll("button").forEach(x=>x.classList.remove("primary")); b.classList.add("primary"); });
        slots.appendChild(b);
      }
      if (!data.length) slots.textContent = "Sin slots disponibles.";
    } catch (e) { slots.textContent = `Error: ${e.code}`; }
  });

  document.getElementById("f").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
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
    msg.textContent = "Reservando...";
    try {
      const t = await apiFetch("/reservas", { method: "POST", body: JSON.stringify(payload) });
      const token = t.token_cancelacion;
      if (token) localStorage.setItem(TOKEN_KEY, token);
      msg.textContent = `Reserva creada: ${t.id}. Token: ${token}`;
    } catch (err) {
      if (err.status === 429) msg.textContent = "Demasiados intentos, intentá más tarde.";
      else if (err.code && err.code.startsWith("RN02")) msg.textContent = `Conflicto de agenda (${err.code}).`;
      else if (err.code === "RN05") msg.textContent = "Ya tenés un turno ese día.";
      else msg.textContent = `Error: ${err.code || err.status} — ${err.message}`;
    }
  });

  document.getElementById("fc").addEventListener("submit", async (e) => {
    e.preventDefault();
    const token = new FormData(e.target).get("token") || localStorage.getItem(TOKEN_KEY);
    const mc = document.getElementById("mc");
    mc.textContent = "Cancelando...";
    try {
      const t = await apiFetch(`/reservas/${encodeURIComponent(token)}/cancelacion`, { method: "POST" });
      mc.textContent = `Cancelado: ${t.id} (${t.estado})`;
      localStorage.removeItem(TOKEN_KEY);
    } catch (err) {
      mc.textContent = `Error: ${err.code || err.status} — ${err.message}`;
    }
  });
}