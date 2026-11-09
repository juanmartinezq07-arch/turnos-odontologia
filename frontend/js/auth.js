// Credenciales de rol y utilidades de sesión en memoria (variables de módulo).
// Al recargar la página las credenciales se pierden; nunca se persisten en localStorage.
let recepcionKey = null;
let odontologoKey = null;
let profesionalId = null;
let activeRole = "guest"; // "guest" | "recepcion" | "odontologo"
let pendingTurnoId = null;
const listeners = new Set();
const recentTurnos = [];

function notify() {
  const state = getAuthState();
  for (const fn of listeners) {
    try {
      fn(state);
    } catch {
      // ignore listener errors
    }
  }
}

export function setRecepcionKey(key) {
  recepcionKey = key ? String(key).trim() : null;
  if (recepcionKey) {
    odontologoKey = null;
    activeRole = "recepcion";
  }
  notify();
}

export function setOdontologo(key, profId) {
  odontologoKey = key ? String(key).trim() : null;
  if (profId !== undefined) {
    profesionalId = profId ? String(profId).trim() : null;
  }
  if (odontologoKey) {
    recepcionKey = null;
    activeRole = "odontologo";
  }
  notify();
}

export function setProfesionalId(profId) {
  profesionalId = profId ? String(profId).trim() : null;
  notify();
}

export function setActiveRole(role) {
  if (role === "guest" || role === "recepcion" || role === "odontologo") {
    activeRole = role;
    if (role === "guest") {
      recepcionKey = null;
      odontologoKey = null;
    }
    notify();
  }
}

export function clearAuth() {
  recepcionKey = null;
  odontologoKey = null;
  profesionalId = null;
  activeRole = "guest";
  notify();
}

export function authHeaders() {
  const h = {};
  if (activeRole === "recepcion" && recepcionKey) {
    h["X-API-Key"] = recepcionKey;
  } else if (activeRole === "odontologo" && odontologoKey) {
    h["X-API-Key"] = odontologoKey;
    if (profesionalId) h["X-Profesional-Id"] = profesionalId;
  } else if (recepcionKey) {
    h["X-API-Key"] = recepcionKey;
  } else if (odontologoKey) {
    h["X-API-Key"] = odontologoKey;
    if (profesionalId) h["X-Profesional-Id"] = profesionalId;
  }
  return h;
}

export function hasAuth() {
  return !!(recepcionKey || odontologoKey);
}

export function getAuthState() {
  return {
    role: activeRole,
    recepcionKey: recepcionKey || "",
    odontologoKey: odontologoKey || "",
    profesionalId: profesionalId || "",
    hasRecepcion: !!recepcionKey,
    hasOdontologo: !!odontologoKey,
    isAuthenticated:
      (activeRole === "recepcion" && !!recepcionKey) ||
      (activeRole === "odontologo" && !!odontologoKey),
  };
}

export function onAuthChange(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

export function rememberTurno(turno, label = "") {
  if (!turno || !turno.id) return;
  const idx = recentTurnos.findIndex((x) => x.id === turno.id);
  const entry = {
    id: turno.id,
    profesional_id: turno.profesional_id || null,
    prestacion_id: turno.prestacion_id || null,
    sillon_id: turno.sillon_id || null,
    inicio: turno.inicio || null,
    fin: turno.fin || null,
    estado: turno.estado || "activo",
    label: label || "",
  };
  if (idx >= 0) recentTurnos[idx] = { ...recentTurnos[idx], ...entry };
  else recentTurnos.unshift(entry);
  if (recentTurnos.length > 8) recentTurnos.pop();
}

export function getRecentTurnos() {
  return [...recentTurnos];
}

export function setPendingTurnoId(id) {
  pendingTurnoId = id || null;
}

export function consumePendingTurnoId() {
  const val = pendingTurnoId;
  pendingTurnoId = null;
  return val;
}

/* ==================== UI HELPERS ==================== */
export function showToast(message, type = "info") {
  const root = document.getElementById("toast-root");
  if (!root) return;
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.innerHTML = `<span>${message}</span>`;
  root.appendChild(el);
  setTimeout(() => {
    el.style.opacity = "0";
    el.style.transform = "translateY(8px)";
    el.style.transition = "opacity 180ms ease, transform 180ms ease";
    setTimeout(() => el.remove(), 200);
  }, 3400);
}

export async function copyToClipboard(text, label = "Copiado al portapapeles") {
  try {
    await navigator.clipboard.writeText(text);
    showToast(`${label}: ${text.slice(0, 18)}${text.length > 18 ? "…" : ""}`, "success");
  } catch {
    showToast("No se pudo copiar automáticamente", "warning");
  }
}

export function dateOffsetISO(daysOffset = 0) {
  const d = new Date();
  d.setDate(d.getDate() + daysOffset);
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

export function nextMondayISO() {
  const d = new Date();
  const day = d.getDay();
  const diff = day === 0 ? 1 : 8 - day;
  return dateOffsetISO(diff);
}

export function formatHour(isoStr) {
  if (!isoStr) return "";
  const d = new Date(isoStr);
  if (Number.isNaN(d.getTime())) {
    const m = String(isoStr).match(/T(\d{2}:\d{2})/);
    return m ? m[1] : String(isoStr);
  }
  return d.toLocaleTimeString("es-AR", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
}

export function formatDateTimeShort(isoStr) {
  if (!isoStr) return "—";
  const d = new Date(isoStr);
  if (Number.isNaN(d.getTime())) return String(isoStr);
  return d.toLocaleString("es-AR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
}

const DEMO_PATIENTS = [
  { nombre: "Lucía Fernández Demo", telefono: "11-4501-1122", email: "lucia.demo@example.com" },
  { nombre: "Martín Pereyra Demo", telefono: "11-5802-3344", email: "martin.demo@example.com" },
  { nombre: "Valentina Gómez Demo", telefono: "11-6203-5566", email: "valentina.demo@example.com" },
  { nombre: "Santiago Ruiz Demo", telefono: "11-3904-7788", email: "santiago.demo@example.com" },
];
let demoIdx = 0;

export function nextDemoPatient() {
  const p = DEMO_PATIENTS[demoIdx % DEMO_PATIENTS.length];
  demoIdx += 1;
  return p;
}
