from typing import Any, Optional

from app.core.enums import PlanAvailability, PlanType
from app.db import SQLSessionContext
from app.db.models.dto import PlanDto
from app.db.models.sql import Plan

from .base import CrudService


class PlanService(CrudService):
    async def create(
        self,
        name: str,
        plan_type: PlanType,
        duration_days: int,
        price: float,
        *,
        traffic_limit: Optional[int] = None,
        device_limit: Optional[int] = None,
        description: Optional[str] = None,
        available_for: PlanAvailability = PlanAvailability.ALL,
        allowed_user_ids: Optional[list[int]] = None,
        is_active: bool = True,
    ) -> PlanDto:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            db_plan = Plan(
                name=name,
                plan_type=plan_type,
                duration_days=duration_days,
                price=price,
                traffic_limit=traffic_limit,
                device_limit=device_limit,
                description=description,
                available_for=available_for,
                allowed_user_ids=allowed_user_ids,
                is_active=is_active,
            )
            await uow.commit(db_plan)
            return db_plan.dto()

    async def get(self, plan_id: int) -> Optional[PlanDto]:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            db_plan = await repository.plans.get(plan_id=plan_id)
            return db_plan.dto() if db_plan else None

    async def get_by_name(self, name: str) -> Optional[PlanDto]:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            db_plan = await repository.plans.get_by_name(name=name)
            return db_plan.dto() if db_plan else None

    async def update(self, plan: PlanDto, **data: Any) -> Optional[PlanDto]:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            for key, value in data.items():
                setattr(plan, key, value)
            db_plan = await repository.plans.update(plan_id=plan.id, **plan.model_state)
            return db_plan.dto() if db_plan else None

    async def delete(self, plan_id: int) -> bool:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            return await repository.plans.delete(plan_id=plan_id)

    async def count(self) -> int:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            return await repository.plans.count()

    async def filter_by_type(self, plan_type: PlanType) -> list[PlanDto]:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            plans = await repository.plans.filter_by_type(plan_type)
            return [plan.dto() for plan in plans]

    async def filter_by_availability(self, available_for: PlanAvailability) -> list[PlanDto]:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            plans = await repository.plans.filter_by_availability(available_for)
            return [plan.dto() for plan in plans]

    async def filter_active(self, is_active: bool = True) -> list[PlanDto]:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            plans = await repository.plans.filter_active(is_active)
            return [plan.dto() for plan in plans]
