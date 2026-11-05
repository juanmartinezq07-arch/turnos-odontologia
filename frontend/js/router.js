const routes = {};
let current = null;

export function register(path, render) { routes[path] = render; }

export function navigate(path) {
  if (location.hash !== "#" + path) location.hash = path;
  else render();
}

function render() {
  const path = location.hash.replace(/^#/, "") || "/";
  const fn = routes[path] || routes["/"];
  const app = document.getElementById("app");
  if (app && fn) fn(app);
  current = path;
}

export function startRouter() {
  window.addEventListener("hashchange", render);
  render();
}