from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from .plans import PlansRepository
from .promocodes import PromocodesRepository
from .users import UsersRepository


class Repository(BaseRepository):
    users: UsersRepository
    plans: PlansRepository
    promocodes: PromocodesRepository

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
        self.users = UsersRepository(session=session)
        self.plans = PlansRepository(session=session)
        self.promocodes = PromocodesRepository(session=session)
