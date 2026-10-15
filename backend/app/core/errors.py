"""Errores de dominio con codigo estable {code, message} (task 2.4)."""
from sqlalchemy.exc import IntegrityError


class DomainConflict(Exception):
    """Conflicto de dominio con codigo estable.

    status por defecto 409 (RN02); las violaciones de validacion
    temporal RN03 usan 422 segun spec.
    """

    def __init__(self, code: str, message: str, status: int = 409) -> None:
        self.code = code
        self.message = message
        self.status = status
        super().__init__(message)


class NotFound(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


def conflict_code_from_integrity_error(exc: IntegrityError) -> str:
    """Mapea la violacion al codigo por NOMBRE de constraint, nunca por mensaje."""
    nombre = ""
    orig = getattr(exc, "orig", None)
    diag = getattr(orig, "diag", None)
    if diag is not None and getattr(diag, "constraint_name", None):
        nombre = str(diag.constraint_name).lower()
    texto = f"{nombre} {type(orig).__name__}".lower()
    if "rn02_profesional" in texto:
        return "RN02_PROFESIONAL"
    if "rn02_sillon" in texto:
        return "RN02_SILLON"
    return "CONFLICTO"
