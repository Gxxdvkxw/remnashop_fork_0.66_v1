from typing import Optional

from aiogram.types import BufferedInputFile
from dishka import FromDishka
from dishka.integrations.taskiq import inject

from src.core.config.app import AppConfig
from src.core.enums import MaintenanceMode, MediaType, SystemNotificationType
from src.infrastructure.taskiq.broker import broker
from src.services import NotificationService, UserService


@broker.task
@inject
async def send_system_notification_task(
    ntf_type: SystemNotificationType,
    text_key: str,
    mode: MaintenanceMode,
    user_service: FromDishka[UserService],
    notification_service: FromDishka[NotificationService],
) -> None:
    devs = await user_service.get_devs()
    await notification_service.system_notify(
        devs=devs,
        ntf_type=ntf_type,
        text_key=text_key,
        mode=mode,
    )


@broker.task
@inject
async def send_error_notification_task(
    update_id: int,
    user_id: Optional[str],
    user_name: Optional[str],
    error_type_name: str,
    error_message: str,
    traceback_str: str,
    config: FromDishka[AppConfig],
    user_service: FromDishka[UserService],
    notification_service: FromDishka[NotificationService],
) -> None:
    dev_user = await user_service.get(telegram_id=config.bot.dev_id)

    text = f"{error_type_name}: {error_message}"
    file_data = BufferedInputFile(
        file=traceback_str.encode(),
        filename=f"error_{update_id}.txt",
    )

    await notification_service.notify_super_dev(
        dev=dev_user,
        text_key="ntf-event-error",
        media=file_data,
        media_type=MediaType.DOCUMENT,
        user=bool(user_id),
        id=user_id,
        name=user_name,
        error=text,
    )
