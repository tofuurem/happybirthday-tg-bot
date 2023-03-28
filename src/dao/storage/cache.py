from typing import Type

from src.dao.storage.resources.sql_transport import SQLTransport
from src.dao.dto.database import User, Chat


class Cache:
    def __init__(self, transport: SQLTransport) -> None:
        self._tr = transport

    async def add_model(self, model: Chat | User) -> None:
        await self._tr.add_model(model)

    async def get_model(self, tg_id: int, model: Type[Chat | User]) -> Chat | User | None:
        return await self._tr.get_model(tg_id, model)
