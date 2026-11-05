import { apiFetch } from "../api.js";
import { authHeaders } from "../auth.js";

export function renderReprogramar(app) {
  app.innerHTML = `
    <div class="card">
      <h2>Cancelar / Reprogramar turno</h2>
      <section>
        <h3>Cancelar</h3>
        <form id="fc">
          <label>ID turno <input name="id" required /></label>
          <button type="submit">Cancelar turno</button>
        </form>
        <p id="mc"></p>
      </section>
      <section>
        <h3>Reprogramar</h3>
        <form id="fr">
          <label>ID turno original <input name="id" required /></label>
          <label>Nuevo inicio <input name="inicio" type="datetime-local" required /></label>
          <label>Sillón nuevo (opcional) <input name="sillon_id" /></label>
          <button type="submit" class="primary">Reprogramar</button>
        </form>
        <p id="mr"></p>
      </section>
    </div>`;
  const mc = document.getElementById("mc");
  const mr = document.getElementById("mr");

  document.getElementById("fc").addEventListener("submit", async (e) => {
    e.preventDefault();
    const id = new FormData(e.target).get("id");
    mc.textContent = "Cancelando...";
    try {
      const t = await apiFetch(`/turnos/${id}/cancelacion`, { method: "POST", headers: authHeaders() });
      mc.textContent = `Cancelado: ${t.id} (${t.estado}, cancelled_at=${t.cancelled_at})`;
    } catch (err) {
      if (err.code === "TURNO_NO_ACTIVO") mc.textContent = "El turno ya estaba cancelado.";
      else if (err.status === 404) mc.textContent = "Turno no encontrado.";
      else if (err.status === 401) mc.textContent = "Ingresá credencial de recepción.";
      else mc.textContent = `Error: ${err.code} — ${err.message}`;
    }
  });

  document.getElementById("fr").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const id = fd.get("id");
    const inicio = fd.get("inicio");
    const sillon = fd.get("sillon_id");
    const body = { inicio: new Date(inicio).toISOString() };
    if (sillon) body.sillon_id = sillon;
    mr.textContent = "Reprogramando...";
    try {
      const r = await apiFetch(`/turnos/${id}/reprogramacion`, { method: "POST", headers: authHeaders(), body: JSON.stringify(body) });
      mr.textContent = `OK: original ${r.original.id} (${r.original.estado}), nuevo ${r.nuevo.id} (${r.nuevo.estado})`;
    } catch (err) {
      const code = err.code || "";
      if (code === "TURNO_NO_ACTIVO") mr.textContent = "El turno original ya estaba cancelado.";
      else if (code.startsWith("RN02")) mr.textContent = `Conflicto de agenda (${code}). El turno original sigue activo.`;
      else if (code === "RN05") mr.textContent = `Paciente ya tiene turno ese día (${code}). El turno original sigue activo.`;
      else if (code.startsWith("RN03")) mr.textContent = `Validación (${code}). El turno original sigue activo.`;
      else if (err.status === 404) mr.textContent = "Turno no encontrado.";
      else if (err.status === 401) mr.textContent = "Ingresá credencial de recepción.";
      else mr.textContent = `Error: ${code} — ${err.message}`;
    }
  });
}