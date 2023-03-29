from dependency_injector import containers, providers

from src.config import Configuration
from src.dao.storage.cache import Cache
from src.dao.storage.resources.sql_transport import SQLTransport


class Container(containers.DeclarativeContainer):
    config: providers.Singleton[Configuration] = providers.Singleton(Configuration)

    _sql: providers.Factory[SQLTransport] = providers.Factory(
        SQLTransport,
        cfg=config.provided
    )

    cache: providers.Factory[Cache] = providers.Factory(
        Cache,
        transport=_sql
    )
