from typing import Type, Sequence

from telegram import User as TgUser
from telegram import Chat as TgChat

from src.dao.storage.resources.sql_transport import SQLTransport
from src.dao.dto.database import User, Chat, Association


class Cache:
    def __init__(self, transport: SQLTransport) -> None:
        self._tr = transport

    async def users_by_room(
        self,
        tg_id: int
    ) -> Sequence[User]:
        return await self._tr.users_by_room(tg_id)

    async def update_if_not_exists(
        self,
        tg_user: TgUser | None,
        tg_chat: TgChat | None,
        *,
        lazy: bool = False
    ) -> tuple[User, Chat]:
        chat = await self.get_model(tg_chat.id, Chat, lazy=lazy)
        if not chat:
            chat = Chat(tg_id=tg_chat.id, title=tg_chat.title)
            await self.add_model(chat)

        user = await self.get_model(tg_user.id, User)
        if not user:
            user = User(
                tg_id=tg_user.id,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                user_name=tg_user.username,
            )
            await self.add_model(user)

        if not await self.is_user_in_room(tg_user.id, tg_chat.id):
            chat_user = Association(user_id=user.id, chat_id=chat.id)
            await self.add_model(chat_user)
        return user, chat

    async def add_model(self, model: Chat | User | Association) -> None:
        await self._tr.add_model(model)

    async def get_model(self, tg_id: int, model: Type[Chat | User], *, lazy: bool = False) -> Chat | User | None:
        return await self._tr.get_model(tg_id, model, lazy=lazy)

    async def is_user_in_room(self, tg_id_user: int, tg_id_chat: int) -> bool:
        return await self._tr.is_user_in_room(tg_id_user, tg_id_chat)
