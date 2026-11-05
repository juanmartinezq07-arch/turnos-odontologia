import { apiFetch } from "../api.js";
import { authHeaders } from "../auth.js";

export function renderAgenda(app) {
  app.innerHTML = `
    <div class="card">
      <h2>Agenda diaria</h2>
      <form id="f">
        <label>Profesional ID <input name="profesional_id" required /></label>
        <label>Fecha <input name="fecha" type="date" required /></label>
        <label><input name="incluir_cancelados" type="checkbox" /> Incluir cancelados</label>
        <button type="submit" class="primary">Consultar</button>
      </form>
      <p id="msg"></p>
      <table id="tbl"><thead><tr><th>Inicio</th><th>Prestación</th><th>Sillón</th><th>Paciente</th><th>Estado</th></tr></thead><tbody></tbody></table>
    </div>`;
  const form = document.getElementById("f");
  const msg = document.getElementById("msg");
  const tbody = document.querySelector("#tbl tbody");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const pid = fd.get("profesional_id");
    const fecha = fd.get("fecha");
    const inc = fd.get("incluir_cancelados") ? "true" : "false";
    msg.textContent = "Cargando...";
    tbody.innerHTML = "";
    try {
      const data = await apiFetch(`/agenda?profesional_id=${encodeURIComponent(pid)}&fecha=${encodeURIComponent(fecha)}&incluir_cancelados=${inc}`, { headers: authHeaders() });
      msg.textContent = `${data.length} turno(s)`;
      for (const t of data) {
        const tr = document.createElement("tr");
        if (t.estado === "cancelado") tr.style.opacity = "0.5";
        const pres = t.prestacion || {};
        const sil = t.sillon || {};
        const pac = t.paciente || {};
        tr.innerHTML = `<td>${t.inicio}</td><td>${pres.nombre || ""} (${pres.duracion_min ?? ""}min)</td><td>${sil.nombre || sil.id || ""}</td><td>${pac.nombre || pac.id || ""}</td><td>${t.estado}</td>`;
        tbody.appendChild(tr);
      }
    } catch (err) {
      if (err.code === "AGENDA_AJENA") msg.textContent = "Solo podés ver tu propia agenda.";
      else if (err.status === 401) msg.textContent = "Ingresá una credencial válida.";
      else msg.textContent = `Error: ${err.code} — ${err.message}`;
    }
  });
}