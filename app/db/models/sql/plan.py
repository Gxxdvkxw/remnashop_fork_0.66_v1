from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    BigInteger,
    Boolean,
    Enum,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import PlanAvailability, PlanType
from app.db.models.dto import PlanDto

from .base import Base


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    plan_type: Mapped[PlanType] = mapped_column(Enum(PlanType), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    traffic_limit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    device_limit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    available_for: Mapped[PlanAvailability] = mapped_column(
        Enum(PlanAvailability),
        default=PlanAvailability.ALL,
        nullable=False,
    )
    allowed_user_ids: Mapped[Optional[list[int]]] = mapped_column(
        ARRAY(BigInteger),
        default=None,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        nullable=False,
        onupdate=func.now(),
    )

    def dto(self) -> PlanDto:
        return PlanDto.model_validate(self)
