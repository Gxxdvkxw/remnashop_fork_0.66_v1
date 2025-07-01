from redis.asyncio import Redis

from app.core.constants import MAINTENANCE_KEY, MAINTENANCE_WAITLIST_KEY
from app.core.enums import MaintenanceMode

from .base import BaseService


class MaintenanceService(BaseService):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        super().__init__()

    async def get_mode(self) -> MaintenanceMode:
        value = await self.redis.get(MAINTENANCE_KEY)

        if value is None:
            self.logger.debug(
                f"Maintenance mode not set in Redis, defaulting to '{MaintenanceMode.OFF.value}'"
            )
            return MaintenanceMode.OFF

        if isinstance(value, bytes):
            value = value.decode()

        try:
            mode = MaintenanceMode(value)
            self.logger.debug(f"Current maintenance mode: '{mode.value}'")
            return mode
        except ValueError:
            self.logger.error(
                f"Invalid maintenance mode value '{value}' found in Redis. "
                f"Falling back to '{MaintenanceMode.OFF.value}'"
            )
            return MaintenanceMode.OFF

    async def get_available_modes(self) -> list[MaintenanceMode]:
        current = await self.get_mode()
        available_modes = [mode for mode in MaintenanceMode if mode != current]
        self.logger.debug(
            f"Available maintenance modes (excluding current '{current.value}'): "
            f"{[m.value for m in available_modes]}"
        )
        return available_modes

    async def set_mode(self, mode: MaintenanceMode) -> None:
        await self.redis.set(MAINTENANCE_KEY, mode.value)
        self.logger.info(f"Maintenance mode set to '{mode.value}'")

    async def is_active(self) -> bool:
        return await self.get_mode() != MaintenanceMode.OFF

    async def is_purchase_mode(self) -> bool:
        return await self.get_mode() == MaintenanceMode.PURCHASE

    async def is_global_mode(self) -> bool:
        return await self.get_mode() == MaintenanceMode.GLOBAL

    async def register_waiting_user(self, telegram_id: int) -> None:
        await self.redis.sadd(MAINTENANCE_WAITLIST_KEY, telegram_id)
        self.logger.info(f"User '{telegram_id}' registered in waiting list")

    async def should_notify_user(self, telegram_id: int) -> bool:
        should_notify = not await self.redis.sismember(MAINTENANCE_WAITLIST_KEY, telegram_id)
        self.logger.debug(f"Should notify user '{telegram_id}': {should_notify}")
        return should_notify

    async def get_waiting_users(self) -> list[int]:
        members: set[bytes] = await self.redis.smembers(MAINTENANCE_WAITLIST_KEY)
        waiting_users = [int(m.decode()) for m in members]
        self.logger.debug(f"Retrieved {len(waiting_users)} users from waiting list")
        return waiting_users

    async def clear_waiting_users(self) -> None:
        await self.redis.delete(MAINTENANCE_WAITLIST_KEY)
        self.logger.info("Cleared all users from waiting list")
