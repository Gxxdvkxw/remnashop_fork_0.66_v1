from typing import Type

from pydantic import SecretStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from yarl import URL

from .base import BaseConfig
from .validators import validate_not_change_me


class RedisConfig(BaseConfig, env_prefix="REDIS_"):
    host: str
    port: int
    name: str
    password: SecretStr

    @field_validator("password")
    @classmethod
    def validate_redis_password(
        cls: Type["RedisConfig"],
        field: SecretStr,
        info: FieldValidationInfo,
    ) -> SecretStr:
        validate_not_change_me(field, info)
        return field

    @property
    def dsn(self) -> str:
        return str(
            URL.build(
                scheme="redis",
                password=self.password.get_secret_value(),
                host=self.host,
                port=self.port,
                path=f"/{self.name}",
            )
        )
