from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from app.core.enums import PlanAvailability, PlanType

from .base import TrackableModel


class PlanDto(TrackableModel):
    id: int
    name: str
    plan_type: PlanType
    is_active: bool

    traffic_limit: Optional[int]
    device_limit: Optional[int]

    duration_days: int
    price: Decimal
    description: Optional[str]

    available_for: PlanAvailability
    allowed_user_ids: Optional[list[int]]

    created_at: datetime
    updated_at: datetime

    @property
    def is_unlimited_traffic(self) -> bool:
        return self.traffic_limit is None or self.traffic_limit == 0

    @property
    def is_unlimited_devices(self) -> bool:
        return self.device_limit is None or self.device_limit == 0

    @property
    def total_duration(self) -> timedelta:
        return timedelta(days=self.duration_days)

    @property
    def price_per_day(self) -> float:
        return float(self.price) / self.duration_days if self.duration_days > 0 else 0.0
