from dependency_injector.wiring import Provide, inject
from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

from src.container import Container
from src.dao.dto.database import Chat
from src.dao.storage.cache import Cache


@inject
async def new_member(update: Update, _: ContextTypes.DEFAULT_TYPE, cache: Cache = Provide[Container.cache]) -> None:
    for member in update.message.new_chat_members:
        if member.id == 5396830407:
            # save room to db
            chat = await cache.get_model(update.effective_chat.id, Chat)
            if not chat:
                chat = Chat(tg_id=update.effective_chat.id, title=update.effective_chat.title)
                await cache.add_model(chat)
            await update.message.reply_text('Теперь я с вами, мне нужны ваши данные:3')
