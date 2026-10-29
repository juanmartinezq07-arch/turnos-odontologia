"""004: cancelled_at (RN04) + idx_turno_paciente_fecha (C-20).

Restituye la columna que la 003 recorto para habilitar la cancelacion
(C-22) y agrega el indice de consulta por paciente/fecha. No edita
001-003.
"""
from alembic import op

revision = "004_cancelled_at_paciente_fecha"
down_revision = "003_recorte_alcance_c01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE turno ADD COLUMN cancelled_at TIMESTAMPTZ")
    op.execute(
        "CREATE INDEX idx_turno_paciente_fecha ON turno (paciente_id, inicio)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_turno_paciente_fecha")
    op.execute("ALTER TABLE turno DROP COLUMN IF EXISTS cancelled_at")
