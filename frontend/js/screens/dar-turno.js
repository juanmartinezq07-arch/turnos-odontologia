import { apiFetch, ApiError } from "../api.js";
import { authHeaders } from "../auth.js";

export function renderDarTurno(app) {
  app.innerHTML = `
    <div class="card">
      <h2>Dar turno</h2>
      <form id="f">
        <label>Profesional <select name="profesional_id" id="prof" required></select></label>
        <label>Prestación <select name="prestacion_id" id="pres" required></select></label>
        <label>Sillón <select name="sillon_id" id="sil"></select></label>
        <label>Fecha <input name="fecha" type="date" required /></label>
        <label>Hora <input name="hora" type="time" required /></label>
        <fieldset><legend>Paciente</legend>
          <label>Nombre <input name="nombre" required /></label>
          <label>Teléfono <input name="telefono" /></label>
          <label>Email <input name="email" type="email" /></label>
        </fieldset>
        <button type="submit" class="primary">Crear turno</button>
      </form>
      <p id="msg"></p>
      <div id="slots"></div>
    </div>`;
  const msg = document.getElementById("msg");
  const profSel = document.getElementById("prof");
  const presSel = document.getElementById("pres");
  const silSel = document.getElementById("sil");

  // Cargar catálogos
  Promise.all([
    apiFetch("/profesionales"),
    apiFetch("/prestaciones"),
    apiFetch("/sillones"),
  ]).then(([profs, pres, sils]) => {
    for (const p of profs) profSel.add(new Option(`${p.nombre} ${p.apellido || ""}`, p.id));
    for (const p of pres) presSel.add(new Option(`${p.nombre} (${p.duracion_min}min)`, p.id));
    silSel.add(new Option("(auto)", ""));
    for (const s of sils) silSel.add(new Option(s.nombre, s.id));
  }).catch((e) => { msg.textContent = `Error cargando catálogos: ${e.code}`; });

  document.getElementById("f").addEventListener("submit", async (e) => {
    e.preventDefault();
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
    msg.textContent = "Creando...";
    try {
      const t = await apiFetch("/turnos", { method: "POST", headers: authHeaders(), body: JSON.stringify(payload) });
      msg.textContent = `Turno creado: ${t.id} (fin ${t.fin})`;
    } catch (err) {
      if (err instanceof ApiError) {
        const m = {
          RN02_PROFESIONAL: "El profesional ya tiene un turno en ese horario.",
          RN02_SILLON: "El sillón ya está ocupado en ese horario.",
          RN05: "El paciente ya tiene un turno ese día.",
        }[err.code];
        msg.textContent = m || `Error: ${err.code} — ${err.message}`;
        if (err.status === 401) msg.textContent = "Ingresá una credencial de recepción válida.";
        if (err.status === 422) msg.textContent = `Validación: ${err.message}`;
      } else {
        msg.textContent = `Error: ${err.message}`;
      }
    }
  });
}