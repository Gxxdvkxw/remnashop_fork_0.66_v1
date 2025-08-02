from enum import Enum
from typing import Any, Type

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.core.enums import SystemNotificationType, UserNotificationType
from src.services import NotificationService


async def _get_notification_types_data(
    settings: Any,
    notification_enum: Type[Enum],
) -> list[dict[str, Any]]:
    notification_types_data: list[dict[str, Any]] = []
    notification_types = list(notification_enum)

    for notification_type in notification_types:
        if not hasattr(settings, notification_type.value):
            continue

        is_enabled = getattr(settings, notification_type.value)
        notification_types_data.append(
            {
                "type": notification_type.value,
                "enabled": is_enabled,
            }
        )
    return notification_types_data


@inject
async def user_types_getter(
    dialog_manager: DialogManager,
    notification_service: FromDishka[NotificationService],
    **kwargs: Any,
) -> dict[str, Any]:
    settings = await notification_service.get_user_settings()
    notification_types_data = await _get_notification_types_data(settings, UserNotificationType)
    return {"types": notification_types_data}


@inject
async def system_types_getter(
    dialog_manager: DialogManager,
    notification_service: FromDishka[NotificationService],
    **kwargs: Any,
) -> dict[str, Any]:
    settings = await notification_service.get_system_settings()
    notification_types_data = await _get_notification_types_data(settings, SystemNotificationType)
    return {"types": notification_types_data}
