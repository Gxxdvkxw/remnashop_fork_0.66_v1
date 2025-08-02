from typing import Any, Optional, cast

from sqlalchemy import func, or_, select
from sqlalchemy.sql.functions import count

from src.core.enums import UserRole
from src.infrastructure.database.models.sql import User

from .base import BaseRepository


class UserRepository(BaseRepository):
    async def get(self, telegram_id: int) -> Optional[User]:
        return await self._get_one(User, User.telegram_id == telegram_id)

    async def get_by_partial_name(self, query: str) -> list[User]:
        search_pattern = f"%{query.lower()}%"
        conditions = [func.lower(User.name).like(search_pattern)]
        return await self._get_many(User, or_(*conditions))

    async def update(self, telegram_id: int, **data: Any) -> Optional[User]:
        return await self._update(User, [User.telegram_id == telegram_id], **data)

    async def delete(self, telegram_id: int) -> int:
        return await self._delete(User, User.telegram_id == telegram_id)

    async def count(self) -> int:
        return cast(int, await self.session.scalar(select(count(User.id))))

    async def filter_by_role(self, role: UserRole) -> list[User]:
        return await self._get_many(User, User.role == role)

    async def filter_by_blocked(self, blocked: bool = True) -> list[User]:
        return await self._get_many(User, User.is_blocked == blocked)
