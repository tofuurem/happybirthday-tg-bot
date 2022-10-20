from dependency_injector import containers, providers

from config import Configuration
from src.redis_cache import Cache


class Container(containers.DeclarativeContainer):
    config: providers.Singleton[Configuration] = providers.Singleton(Configuration)

    cache: providers.Factory[Cache] = providers.Factory(
        Cache,
        url=config().redis_url,
    )
