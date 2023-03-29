from typing import Type, Sequence

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import lazyload, joinedload

from src.config import Configuration
from src.dao.dto.database import Base, User, Chat, Association


# 1) бот добавляется в чат -> заполняется чат и пользователи и после саб таблица
# 2) берет пользователь и обновляется данные пользователя
# 3) берется информация по пользователям в комнате
# 4) todo: берется информация по комнатам пользователя (in future)
# 5)

class SQLTransport:

    def __init__(self, cfg: Configuration) -> None:
        self.cfg = cfg.pg

    async def async_session(self) -> async_sessionmaker:
        engine = create_async_engine(
            self.cfg.connection_string,
        )
        return async_sessionmaker(engine, expire_on_commit=False)

    async def init_db(self) -> None:
        engine = create_async_engine(
            self.cfg.connection_string,
        )
        async with engine.begin() as conn:
            Base.metadata.schema = self.cfg.schema_db
            await conn.run_sync(Base.metadata.create_all)

    async def users_by_room(self, tg_id: int) -> Sequence[User]:
        async_session = await self.async_session()
        async with async_session() as session:
            stmp = (
                select(User)
                .join(Association)
                .join(Chat)
                .where(User.id == Association.user_id)
                .where(Chat.id == Association.chat_id)
                .where(Chat.tg_id == tg_id)
            )
            result = await session.execute(stmp)
            return result.scalars().all()

    async def get_model(self, tg_id: int, model: Type[Chat | User], *, lazy: bool = False) -> Chat | User | None:
        # fixme: sometimes it's kill me
        attrb = 'chats' if issubclass(model, User) else 'users'
        async_session = await self.async_session()
        async with async_session() as session:
            stmp = select(model).where(model.tg_id == tg_id)
            if lazy:
                stmp = select(model).where(model.tg_id == tg_id).options(joinedload(getattr(model, attrb)))
            result = await session.execute(stmp)
            return result.scalars().first()

    async def add_model(self, model: Chat | User | Association) -> None:
        async_session = await self.async_session()
        async with async_session() as session:
            session.add(model)
            await session.commit()

    async def is_user_in_room(self, tg_user: int, tg_chat: int) -> bool:
        async_session = await self.async_session()
        async with async_session() as session:
            stmp = (
                select(Association)
                .join(User)
                .join(Chat)
                .where(User.tg_id == tg_user)
                .where(Chat.tg_id == tg_chat)
            )
            result = await session.execute(stmp)
            return bool(result.scalars().first())
