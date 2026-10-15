"""Permite `python -m alembic` corrido desde `backend/`.

El paquete local `alembic/` (migraciones) hace sombra a la librería Alembic
instalada cuando el cwd está en `sys.path`. Este shim saca `backend/` del
path, reimporta la librería real y delega en su `main()`. Después, el
`prepend_sys_path = .` de `alembic.ini` vuelve a agregar `backend/` para que
`env.py` pueda importar `app.*` (y `from alembic import context` reutiliza la
librería ya importada vía `sys.modules`).
"""
import os
import sys


def _purge_local_package() -> None:
    backend = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path = [
        p for p in sys.path if os.path.abspath(p or os.getcwd()) != backend
    ]
    for mod in [m for m in sys.modules if m == "alembic" or m.startswith("alembic.")]:
        del sys.modules[mod]


_purge_local_package()

from alembic.config import main  # noqa: E402  (import tras purgar el shadowing)

if __name__ == "__main__":
    raise SystemExit(main())
