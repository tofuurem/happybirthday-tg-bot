from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.ext import ContextTypes

from src.container import Container
from src.dao.dto.database import Chat
from src.dao.storage.cache import Cache


@inject
def new_member(update: Update, _: ContextTypes.DEFAULT_TYPE, cache: Cache = Provide[Container.cache]) -> None:
    for member in update.message.new_chat_members:
        if member.username == 'happy_bithday_notify_bot':
            # save room to db
            chat = await cache.get_model(update.effective_chat.id, Chat)
            if not chat:
                chat = Chat(tg_id=update.effective_chat.id, title=update.effective_chat.title)
                await cache.add_model(chat)
            update.message.reply_text('Hi hi!')
