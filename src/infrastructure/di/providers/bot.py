from collections.abc import AsyncIterable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka import Provider, Scope, provide

from src.core.config.app import AppConfig


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_bot(self, config: AppConfig) -> AsyncIterable[Bot]:
        async with Bot(
            token=config.bot.token.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        ) as bot:
            yield bot
        await bot.session.close()
