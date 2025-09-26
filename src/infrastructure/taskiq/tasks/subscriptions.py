from dishka import FromDishka
from dishka.integrations.taskiq import inject

from src.infrastructure.database.models.dto import PlanSnapshotDto, SubscriptionDto, UserDto
from src.infrastructure.taskiq.broker import broker
from src.services.remnawave import RemnawaveService
from src.services.subscription import SubscriptionService


@broker.task
@inject
async def create_subscription_task(
    user: UserDto,
    plan: PlanSnapshotDto,
    remnawave_service: FromDishka[RemnawaveService],
    subscription_service: FromDishka[SubscriptionService],
) -> None:
    created_user = await remnawave_service.create_user(user, plan)

    subscription = SubscriptionDto(
        user_remna_id=created_user.uuid,
        status=created_user.status,
        expire_at=created_user.expire_at,
        url=created_user.short_uuid,
        plan=plan,
    )

    await subscription_service.create(user, subscription)
