const routes = {};
let current = "/";
const routeListeners = new Set();

export function register(path, render) {
  routes[path] = render;
}

export function navigate(path) {
  if (location.hash !== "#" + path) {
    location.hash = path;
  } else {
    render();
  }
}

export function getCurrentRoute() {
  return current;
}

export function onRouteChange(fn) {
  routeListeners.add(fn);
  return () => routeListeners.delete(fn);
}

function render() {
  const path = location.hash.replace(/^#/, "") || "/";
  const fn = routes[path] || routes["/"];
  const app = document.getElementById("app");
  current = routes[path] ? path : "/";

  if (app && fn) {
    app.classList.remove("screen-enter");
    void app.offsetWidth; // trigger reflow for smooth entrance animation
    app.classList.add("screen-enter");
    fn(app);
  }

  for (const listener of routeListeners) {
    try {
      listener(current);
    } catch {
      // ignore
    }
  }
}

export function startRouter() {
  window.addEventListener("hashchange", render);
  render();
}
