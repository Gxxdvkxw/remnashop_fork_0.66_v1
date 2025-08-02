from dishka.integrations.taskiq import setup_dishka as setup_taskiq_dishka
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

from src.core.config import AppConfig
from src.core.logger import setup_logger
from src.infrastructure.di import create_container


def create_broker(config: AppConfig) -> RedisStreamBroker:
    result_backend = RedisAsyncResultBackend(redis_url=config.redis.dsn)
    broker = RedisStreamBroker(url=config.redis.dsn).with_result_backend(result_backend)
    return broker


# TODO: Think of a way to get rid of the global variable
broker = create_broker(config=AppConfig.get())


def worker() -> RedisStreamBroker:
    setup_logger()

    config = AppConfig.get()
    container = create_container(config=config)

    setup_taskiq_dishka(container=container, broker=broker)
    return broker
