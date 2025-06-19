from typing import Any, Optional, cast

from sqlalchemy import select
from sqlalchemy.sql.functions import count

from app.core.enums import PlanAvailability, PlanType
from app.db.models.sql import Plan

from .base import BaseRepository


class PlansRepository(BaseRepository):
    async def get(self, plan_id: int) -> Optional[Plan]:
        return await self._get(Plan, Plan.id == plan_id)

    async def get_by_name(self, name: str) -> Optional[Plan]:
        return await self._get(Plan, Plan.name == name)

    async def update(self, plan_id: int, **data: Any) -> Optional[Plan]:
        return await self._update(
            model=Plan,
            conditions=[Plan.id == plan_id],
            load_result=True,
            **data,
        )

    async def delete(self, plan_id: int) -> bool:
        return await self._delete(Plan, Plan.id == plan_id)

    async def count(self) -> int:
        return cast(int, await self.session.scalar(select(count(Plan.id))))

    async def filter_by_type(self, plan_type: PlanType) -> list[Plan]:
        return await self._get_many(Plan, Plan.plan_type == plan_type)

    async def filter_by_availability(self, available_for: PlanAvailability) -> list[Plan]:
        return await self._get_many(Plan, Plan.available_for == available_for)

    async def filter_active(self, is_active: bool = True) -> list[Plan]:
        return await self._get_many(Plan, Plan.is_active == is_active)
