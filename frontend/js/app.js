import { register, startRouter } from "./router.js";
import { apiFetch } from "./api.js";
import { renderAgenda } from "./screens/agenda.js";
import { renderDarTurno } from "./screens/dar-turno.js";
import { renderReprogramar } from "./screens/reprogramar.js";
import { renderReserva } from "./screens/reserva.js";

function homeView(app) {
  app.innerHTML = `<div class="card"><h2>Inicio</h2><p>TurnosAR — interfaz base (vanilla).</p><p><a href="#/agenda">Agenda</a> · <a href="#/dar-turno">Dar turno</a> · <a href="#/reprogramar">Reprogramar/Cancelar</a> · <a href="#/reserva">Reserva pública</a> · <a href="#/catalogos">Catálogos</a></p></div>`;
}

function catalogosView(app) {
  app.innerHTML = `<div class="card"><h2>Catálogos</h2><p id="out">Cargando...</p></div>`;
  apiFetch("/profesionales").then((data) => {
    const el = document.getElementById("out");
    if (el) el.textContent = `Profesionales activos: ${data.length}`;
  }).catch((e) => {
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

startRouter();