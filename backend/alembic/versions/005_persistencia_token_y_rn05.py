"""005: token_cancelacion UNIQUE + indice parcial RN05 (C-21).

Agrega la columna token_cancelacion (para reserva guest, CU02) y el indice
unico parcial rn05_un_activo_por_dia para la invariante RN05 (maximo 1
turno activo por paciente y día). No edita 001-004.
"""
from alembic import op

revision = "005_persistencia_token_y_rn05"
down_revision = "004_cancelled_at_paciente_fecha"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE turno ADD COLUMN token_cancelacion TEXT UNIQUE")
    op.execute(
        """
        CREATE UNIQUE INDEX rn05_un_activo_por_dia ON turno (
            paciente_id,
            ((inicio AT TIME ZONE 'America/Argentina/Buenos_Aires')::date)
        ) WHERE estado = 'activo'
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS rn05_un_activo_por_dia")
    op.execute("ALTER TABLE turno DROP COLUMN IF EXISTS token_cancelacion")
