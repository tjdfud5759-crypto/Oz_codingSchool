from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum as SQLAlchemyEnum,
    SmallInteger,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.databases import Base
from app.models.enums import Gender


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    age: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    gender: Mapped[Gender | None] = mapped_column(
        SQLAlchemyEnum(Gender, name="patient_gender"),
        nullable=True,
    )

    phone: Mapped[str] = mapped_column(
        String(11),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        onupdate=func.now(),
    )

    medical_records: Mapped[list["MedicalRecord"]] = relationship(
        back_populates="patient",
    )