"""001: tablas + btree_gist (sin EXCLUDE; van en 002)."""
from alembic import op

revision = "001_create_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
    op.execute(
        """
        CREATE TABLE profesional (
            id UUID PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            matricula TEXT UNIQUE,
            activo BOOLEAN NOT NULL DEFAULT TRUE
        )
        """
    )
    op.execute(
        """
        CREATE TABLE sillon (
            id UUID PRIMARY KEY,
            nombre TEXT NOT NULL UNIQUE,
            activo BOOLEAN NOT NULL DEFAULT TRUE
        )
        """
    )
    op.execute(
        """
        CREATE TABLE prestacion (
            id UUID PRIMARY KEY,
            nombre TEXT NOT NULL,
            duracion_min INTEGER NOT NULL,
            activa BOOLEAN NOT NULL DEFAULT TRUE,
            CONSTRAINT ck_prestacion_duracion CHECK (duracion_min > 0)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE paciente_guest (
            id UUID PRIMARY KEY,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX idx_paciente_telefono ON paciente_guest (telefono)")
    op.execute("CREATE INDEX idx_paciente_email ON paciente_guest (email)")
    op.execute(
        """
        CREATE TABLE turno (
            id UUID PRIMARY KEY,
            profesional_id UUID NOT NULL REFERENCES profesional (id),
            sillon_id UUID NOT NULL REFERENCES sillon (id),
            prestacion_id UUID NOT NULL REFERENCES prestacion (id),
            paciente_id UUID NOT NULL REFERENCES paciente_guest (id),
            inicio TIMESTAMPTZ NOT NULL,
            fin TIMESTAMPTZ NOT NULL,
            estado TEXT NOT NULL DEFAULT 'activo',
            token_cancelacion TEXT UNIQUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            cancelled_at TIMESTAMPTZ,
            CONSTRAINT ck_turno_fin_mayor_inicio CHECK (fin > inicio),
            CONSTRAINT ck_turno_estado CHECK (estado IN ('activo','cancelado'))
        )
        """
    )
    op.execute(
        "CREATE INDEX idx_turno_profesional_inicio ON turno (profesional_id, inicio)"
    )
    op.execute("CREATE INDEX idx_turno_sillon_inicio ON turno (sillon_id, inicio)")
    op.execute("CREATE INDEX idx_turno_estado ON turno (estado)")
    op.execute(
        """
        CREATE TABLE horario_atencion (
            id UUID PRIMARY KEY,
            profesional_id UUID REFERENCES profesional (id),
            dia_semana INTEGER NOT NULL,
            hora_desde TIME NOT NULL,
            hora_hasta TIME NOT NULL,
            CONSTRAINT ck_horario_dia CHECK (dia_semana >= 0 AND dia_semana <= 6),
            CONSTRAINT ck_horario_rango CHECK (hora_hasta > hora_desde)
        )
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE horario_atencion")
    op.execute("DROP TABLE turno")
    op.execute("DROP TABLE paciente_guest")
    op.execute("DROP TABLE prestacion")
    op.execute("DROP TABLE sillon")
    op.execute("DROP TABLE profesional")
