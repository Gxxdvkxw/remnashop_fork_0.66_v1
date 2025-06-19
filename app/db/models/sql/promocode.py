from datetime import datetime
from typing import Optional

from sqlalchemy import TIMESTAMP, Boolean, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import PromocodeType
from app.db.models.dto import PromocodeDto

from .base import Base


class Promocode(Base):
    __tablename__ = "promocodes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    type: Mapped[PromocodeType] = mapped_column(Enum(PromocodeType), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_multi_use: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    lifetime: Mapped[Optional[int]] = mapped_column(Integer, default=None, nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    traffic: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    # subscription: Mapped[Optional[str]] = mapped_column(String, nullable=True) # TODO: plan config
    discount_percent: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    activated_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.telegram_id"),
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

    def dto(self) -> PromocodeDto:
        return PromocodeDto.model_validate(self)
