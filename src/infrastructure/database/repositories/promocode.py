from typing import Any, Optional, cast

from sqlalchemy import select
from sqlalchemy.sql.functions import count

from src.core.enums import PromocodeType
from src.infrastructure.database.models.sql import Promocode

from .base import BaseRepository


class PromocodeRepository(BaseRepository):
    async def get(self, promocode_id: int) -> Optional[Promocode]:
        return await self._get_one(Promocode, Promocode.id == promocode_id)

    async def get_by_code(self, code: str) -> Optional[Promocode]:
        return await self._get_one(Promocode, Promocode.code == code)

    async def update(self, promocode_id: int, **data: Any) -> Optional[Promocode]:
        return await self._update(Promocode, Promocode.id == promocode_id, **data)

    async def delete(self, promocode_id: int) -> bool:
        return await self._delete(Promocode, Promocode.id == promocode_id)

    async def count(self) -> int:
        return cast(int, await self.session.scalar(select(count(Promocode.id))))

    async def filter_by_type(self, promocode_type: PromocodeType) -> list[Promocode]:
        return await self._get_many(Promocode, Promocode.type == promocode_type)

    async def filter_active(self, is_active: bool = True) -> list[Promocode]:
        return await self._get_many(Promocode, Promocode.is_active == is_active)

    async def filter_multi_use(self, is_multi_use: bool = True) -> list[Promocode]:
        return await self._get_many(Promocode, Promocode.is_multi_use == is_multi_use)
