from typing import Any, Awaitable, Callable

from aiogram.types import TelegramObject
from dishka import AsyncContainer

from src.core.constants import CONTAINER_KEY, USER_KEY
from src.core.enums import MiddlewareEventType
from src.infrastructure.database.models.dto import UserDto
from src.services import MaintenanceService, NotificationService

from .base import EventTypedMiddleware


class MaintenanceMiddleware(EventTypedMiddleware):
    __event_types__ = [MiddlewareEventType.MESSAGE, MiddlewareEventType.CALLBACK_QUERY]

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        container: AsyncContainer = data[CONTAINER_KEY]
        user: UserDto = data[USER_KEY]

        maintenance_service: MaintenanceService = await container.get(MaintenanceService)
        notification_service: NotificationService = await container.get(NotificationService)

        access_allowed = await maintenance_service.check_access(user=user, event=event)

        if not access_allowed:
            await notification_service.notify_user(
                user=user,
                text_key="ntf-maintenance-denied-global",
            )
            return

        return await handler(event, data)
