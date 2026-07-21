from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.databases import Base


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    patient_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("patients.id"),
        nullable=False,
    )

    chart_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    symptoms: Mapped[str] = mapped_column(
        Text,
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

    patient: Mapped["Patient"] = relationship(
        back_populates="medical_records",
    )

    xray_images: Mapped[list["XrayImage"]] = relationship(
        back_populates="medical_record",
    )

    ai_analysis_results: Mapped[list["AIAnalysisResult"]] = relationship(
        back_populates="medical_record",
    )