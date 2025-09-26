from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .plan import PlanSnapshotDto
    from .user import BaseUserDto

from datetime import datetime, timedelta
from uuid import UUID

from pydantic import Field

from src.core.enums import SubscriptionStatus
from src.core.utils.time import datetime_now

from .base import TrackableDto


class BaseSubscriptionDto(TrackableDto):
    id: Optional[int] = Field(default=None, frozen=True)
    user_remna_id: UUID

    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    expire_at: Optional[datetime]
    url: str
    plan: "PlanSnapshotDto"

    @property
    def expiry_time(self) -> Optional[timedelta]:
        if self.expire_at is None:
            return None

        return self.expire_at - datetime_now()

    created_at: Optional[datetime] = Field(default=None, frozen=True)
    updated_at: Optional[datetime] = Field(default=None, frozen=True)


class SubscriptionDto(BaseSubscriptionDto):
    user: "Optional[BaseUserDto]" = None
