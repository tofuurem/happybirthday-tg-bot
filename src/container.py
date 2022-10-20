from dependency_injector import containers, providers

from src.config import Configuration
from src.storage.cache import Cache
from src.storage.redis_transport import RedisTransport


class Container(containers.DeclarativeContainer):
    config: providers.Singleton[Configuration] = providers.Singleton(Configuration)

    _redis: providers.Factory[RedisTransport] = providers.Factory(
        RedisTransport,
        url=config().redis_url
    )

    cache: providers.Factory[Cache] = providers.Factory(
        Cache,
        transport=_redis
    )
