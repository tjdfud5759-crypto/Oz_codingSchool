from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    DECIMAL,
    ForeignKey,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.databases import Base


class AIAnalysisResult(Base):
    __tablename__ = "ai_analysis_results"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    record_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("medical_records.id"),
        nullable=False,
    )

    is_pneumonia: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    confidence: Mapped[Decimal] = mapped_column(
        DECIMAL(5, 2),
        nullable=False,
    )

    heatmap_url: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    ai_model: Mapped[str] = mapped_column(
        String(50),
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

    medical_record: Mapped["MedicalRecord"] = relationship(
        back_populates="ai_analysis_results",
    )