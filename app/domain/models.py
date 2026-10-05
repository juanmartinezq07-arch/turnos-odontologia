"""Entidades del dominio (SQLAlchemy 2.0, mapped_column).

RN02 vive aca (doble EXCLUDE parcial) y se refleja en Alembic 002.
Solo datos ficticios de contacto en PacienteGuest (Ley 25.326).
"""
import uuid
from datetime import date, datetime, time

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Text,
    Time,
    Uuid,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Profesional(Base):
    __tablename__ = "profesional"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(Text, nullable=False)
    apellido: Mapped[str] = mapped_column(Text, nullable=False)
    matricula: Mapped[str | None] = mapped_column(Text, unique=True, nullable=True)
    activo: Mapped[bool] = mapped_column(default=True, nullable=False)


class Sillon(Base):
    __tablename__ = "sillon"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    activo: Mapped[bool] = mapped_column(default=True, nullable=False)


class Prestacion(Base):
    __tablename__ = "prestacion"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(Text, nullable=False)
    duracion_min: Mapped[int] = mapped_column(nullable=False)
    activa: Mapped[bool] = mapped_column(default=True, nullable=False)

    __table_args__ = (
        CheckConstraint("duracion_min > 0", name="ck_prestacion_duracion"),
    )


class PacienteGuest(Base):
    """Solo contacto minimo (nombre + telefono/email ficticios). Sin DNI ni clinica."""

    __tablename__ = "paciente_guest"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(Text, nullable=False)
    telefono: Mapped[str | None] = mapped_column(Text, nullable=True)
    email: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("idx_paciente_telefono", "telefono"),
        Index("idx_paciente_email", "email"),
    )


class Turno(Base):
    __tablename__ = "turno"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    profesional_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profesional.id"), nullable=False
    )
    sillon_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sillon.id"), nullable=False)
    prestacion_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("prestacion.id"), nullable=False
    )
    paciente_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("paciente_guest.id"), nullable=False
    )
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fin: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    estado: Mapped[str] = mapped_column(Text, nullable=False, default="activo")
    token_cancelacion: Mapped[str | None] = mapped_column(
        Text, unique=True, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        CheckConstraint("fin > inicio", name="ck_turno_fin_mayor_inicio"),
        CheckConstraint(
            "estado IN ('activo','cancelado')", name="ck_turno_estado"
        ),
        ExcludeConstraint(
            ("profesional_id", "="),
            (func.tstzrange(text("inicio"), text("fin")), "&&"),
            where=text("estado = 'activo'"),
            name="rn02_profesional",
            using="gist",
        ),
        ExcludeConstraint(
            ("sillon_id", "="),
            (func.tstzrange(text("inicio"), text("fin")), "&&"),
            where=text("estado = 'activo'"),
            name="rn02_sillon",
            using="gist",
        ),
        Index(
            "rn05_un_activo_por_dia",
            "paciente_id",
            text("(inicio AT TIME ZONE 'America/Argentina/Buenos_Aires')::date"),
            unique=True,
            postgresql_where=text("estado = 'activo'"),
        ),
        Index("idx_turno_profesional_inicio", "profesional_id", "inicio"),
        Index("idx_turno_sillon_inicio", "sillon_id", "inicio"),
        Index("idx_turno_estado", "estado"),
    )


class HorarioAtencion(Base):
    __tablename__ = "horario_atencion"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    profesional_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("profesional.id"), nullable=True
    )
    dia_semana: Mapped[int] = mapped_column(nullable=False)  # 0=lunes .. 6=domingo
    hora_desde: Mapped[time] = mapped_column(Time, nullable=False)
    hora_hasta: Mapped[time] = mapped_column(Time, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "dia_semana >= 0 AND dia_semana <= 6", name="ck_horario_dia"
        ),
        CheckConstraint("hora_hasta > hora_desde", name="ck_horario_rango"),
    )


__all__ = [
    "Base",
    "Profesional",
    "Sillon",
    "Prestacion",
    "PacienteGuest",
    "Turno",
    "HorarioAtencion",
]
