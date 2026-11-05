// Cliente HTTP nativo para TurnosAR. Consume el contrato {code, message}.
export class ApiError extends Error {
  constructor(code, message, status) {
    super(message);
    this.code = code;
    this.message = message;
    this.status = status;
    this.name = "ApiError";
  }
}

export async function apiFetch(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const res = await fetch(path, { ...options, headers });
  const text = await res.text();
  let data = null;
  if (text) {
    try { data = JSON.parse(text); } catch { data = text; }
  }
  if (!res.ok) {
    const code = (data && data.code) || `HTTP_${res.status}`;
    const message = (data && data.message) || res.statusText || "Error";
    throw new ApiError(code, message, res.status);
  }
  return data;
}