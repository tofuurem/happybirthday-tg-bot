from src.abstract.transport import AbstractTransport
from src.dto.user import User


class Cache:
    def __init__(self, transport: AbstractTransport) -> None:
        self._tr = transport

    async def dall_users(self) -> list[User]:
        keys = await self._tr.keys()
        if not keys:
            return []
        return [await self._tr.load(k) for k in keys]

    async def all_chat_str(self, current_chat_id: int) -> str:
        data = await self.dall_users()
        return '\n'.join([i.__str__() for i in data if i.group_id == current_chat_id])

    async def get(self, key: tuple[int, int] | str) -> User | None:
        return await self._tr.load(key)

    async def set(self, user: User) -> None:
        await self._tr.save(user)

