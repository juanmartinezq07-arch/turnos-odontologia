// Credenciales de rol: viven solo en memoria (variable de módulo).
// Al recargar la página se pierden; nunca se persisten en archivos estáticos.
let recepcionKey = null;
let odontologoKey = null;
let profesionalId = null;

export function setRecepcionKey(key) { recepcionKey = key || null; }
export function setOdontologo(key, profId) { odontologoKey = key || null; profesionalId = profId || null; }
export function clearAuth() { recepcionKey = null; odontologoKey = null; profesionalId = null; }

export function authHeaders() {
  const h = {};
  if (recepcionKey) h["X-API-Key"] = recepcionKey;
  else if (odontologoKey) {
    h["X-API-Key"] = odontologoKey;
    if (profesionalId) h["X-Profesional-Id"] = profesionalId;
  }
  return h;
}

export function hasAuth() { return !!(recepcionKey || odontologoKey); }