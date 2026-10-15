"""003: recorte de alcance C-01 (CU02/CU03 fuera del change).

Retira el indice parcial RN05 y las columnas de cancelacion guest
(token_cancelacion, cancelled_at). No edita 001 ni 002: todo cambio
nuevo va en una migracion nueva.
"""
from alembic import op

revision = "003_recorte_alcance_c01"
down_revision = "002_add_exclude_constraints"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DROP INDEX IF EXISTS rn05_un_activo_por_dia")
    op.execute("ALTER TABLE turno DROP COLUMN IF EXISTS token_cancelacion")
    op.execute("ALTER TABLE turno DROP COLUMN IF EXISTS cancelled_at")


def downgrade() -> None:
    op.execute("ALTER TABLE turno ADD COLUMN cancelled_at TIMESTAMPTZ")
    op.execute("ALTER TABLE turno ADD COLUMN token_cancelacion TEXT UNIQUE")
    op.execute(
        """
        CREATE UNIQUE INDEX rn05_un_activo_por_dia ON turno (
            paciente_id,
            ((inicio AT TIME ZONE 'America/Argentina/Buenos_Aires')::date)
        ) WHERE estado = 'activo'
        """
    )
