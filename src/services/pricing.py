from decimal import ROUND_DOWN, Decimal, InvalidOperation

from aiogram import Bot
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from src.core.config import AppConfig
from src.core.enums import Currency
from src.infrastructure.database.models.dto import PriceDetailsDto, UserDto
from src.infrastructure.redis import RedisRepository

from .base import BaseService


class PricingService(BaseService):
    def __init__(
        self,
        config: AppConfig,
        bot: Bot,
        redis_client: Redis,
        redis_repository: RedisRepository,
        translator_hub: TranslatorHub,
    ) -> None:
        super().__init__(config, bot, redis_client, redis_repository, translator_hub)

    @staticmethod
    def calculate(user: UserDto, price: Decimal, currency: Currency) -> PriceDetailsDto:
        discount_percent = min(user.purchase_discount or user.personal_discount, 100)
        discounted = price * (Decimal(100) - Decimal(discount_percent)) / Decimal(100)

        final_amount = (
            Decimal(0)
            if discounted <= 0
            else PricingService.apply_currency_rules(discounted, currency)
        )

        return PriceDetailsDto(
            original_amount=price,
            discount_percent=discount_percent,
            final_amount=final_amount,
        )

    @staticmethod
    def parse_price(input_price: str, currency: Currency) -> Decimal:
        try:
            price = Decimal(input_price.strip())
        except InvalidOperation:
            raise ValueError("Invalid numeric format")

        if price < 0:
            raise ValueError("Price cannot be negative")
        if price == 0:
            return Decimal(0)

        return PricingService.apply_currency_rules(price, currency)

    @staticmethod
    def apply_currency_rules(amount: Decimal, currency: Currency) -> Decimal:
        match currency:
            case Currency.XTR | Currency.RUB:
                amount = amount.to_integral_value(rounding=ROUND_DOWN)
                min_amount = Decimal(1)
            case _:
                amount = amount.quantize(Decimal("0.01"))
                min_amount = Decimal("0.01")

        if amount < min_amount:
            amount = min_amount

        return amount
