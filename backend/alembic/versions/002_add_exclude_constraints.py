"""002: doble EXCLUDE parcial RN02 + indice parcial RN05 (D-01, D-02)."""
from alembic import op

revision = "002_add_exclude_constraints"
down_revision = "001_create_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
    op.execute(
        """
        ALTER TABLE turno ADD CONSTRAINT rn02_profesional
        EXCLUDE USING gist (
            profesional_id WITH =,
            tstzrange(inicio, fin) WITH &&
        ) WHERE (estado = 'activo')
        """
    )
    op.execute(
        """
        ALTER TABLE turno ADD CONSTRAINT rn02_sillon
        EXCLUDE USING gist (
            sillon_id WITH =,
            tstzrange(inicio, fin) WITH &&
        ) WHERE (estado = 'activo')
        """
    )
    op.execute(
        """
        CREATE UNIQUE INDEX rn05_un_activo_por_dia ON turno (
            paciente_id,
            ((inicio AT TIME ZONE 'America/Argentina/Buenos_Aires')::date)
        ) WHERE estado = 'activo'
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX rn05_un_activo_por_dia")
    op.execute("ALTER TABLE turno DROP CONSTRAINT rn02_sillon")
    op.execute("ALTER TABLE turno DROP CONSTRAINT rn02_profesional")
