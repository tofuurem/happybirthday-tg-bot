from typing import Type

from src.dao.storage.resources.sql_transport import SQLTransport
from src.dao.dto.database import User, Chat, Association


class Cache:
    def __init__(self, transport: SQLTransport) -> None:
        self._tr = transport

    async def add_model(self, model: Chat | User | Association) -> None:
        await self._tr.add_model(model)

    async def get_model(self, tg_id: int, model: Type[Chat | User]) -> Chat | User | None:
        return await self._tr.get_model(tg_id, model)

    async def is_user_in_room(self, tg_id_user: int, tg_id_chat: int) -> bool:
        return await self._tr.is_user_in_room(tg_id_user, tg_id_chat)
