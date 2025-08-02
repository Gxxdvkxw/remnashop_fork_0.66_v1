from typing import Type

from pydantic import SecretStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from yarl import URL

from .base import BaseConfig
from .validators import validate_not_change_me


class DatabaseConfig(BaseConfig, env_prefix="DATABASE_"):
    host: str
    port: int
    name: str
    user: str
    password: SecretStr

    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int
    pool_timeout: int
    pool_recycle: int

    @field_validator("password")
    @classmethod
    def validate_database_password(
        cls: Type["DatabaseConfig"],
        field: SecretStr,
        info: FieldValidationInfo,
    ) -> SecretStr:
        validate_not_change_me(field, info)
        return field

    @property
    def dsn(self) -> str:
        return str(
            URL.build(
                scheme="postgresql+asyncpg",
                user=self.user,
                password=self.password.get_secret_value(),
                host=self.host,
                port=self.port,
                path=f"/{self.name}",
            )
        )
