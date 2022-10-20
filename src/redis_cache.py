import json

from loguru import logger

import aioredis

from src.entities import User


class Cache:
    def __init__(self, url: str | None = None) -> None:
        self.redis = aioredis.from_url(url or "redis://localhost:6379/1")

    async def dall_users(self) -> list[User]:
        keys = await self.keys()
        if not keys:
            return []
        data = [await self.get(k) for k in keys]
        return data

    async def all_chat_str(self, current_chat_id: int) -> str:
        keys = await self.keys()
        if not keys:
            return ''
        data = [await self.get(k) for k in keys]
        return '\n'.join([i.__str__() for i in data if i.group_id == current_chat_id])

    async def get(self, key: tuple[int, int]) -> User | None:
        """
        :param key: (user_id, chat_id)
        :return:
        """
        key = '{0}_{1}'.format(*key)
        try:
            u = await self.redis.get(key)
            if u:
                decoded_u = User(**json.loads(u.decode('utf-8')))
                return decoded_u
        except Exception as ex:
            logger.exception(ex)

    async def set(self, user: User) -> None:
        await self.redis.set(user.rkey(), user.json())

    async def keys(self) -> list[tuple[int, int]]:
        keys = await self.redis.keys()
        return [tuple(k.decode('utf-8').split('_')) for k in keys]
