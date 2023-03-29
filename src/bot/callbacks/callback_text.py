from telegram import Update
from telegram.ext import ContextTypes

from dependency_injector.wiring import inject, Provide
from loguru import logger

from src.container import Container
from src.dao.storage.cache import Cache


@inject
async def _callback_reg_query(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    q = update.callback_query
    await q.answer()
    choice = q.data
    key = (update.effective_user.id, update.effective_chat.id)

    # maybe pattern matching?:D
    if choice == '0':
        await context.bot.edit_message_text(
            chat_id=q.message.chat_id,
            message_id=q.message.message_id,
            text='Ваши данные остались теми же.',
            parse_mode='HTML'
        )
    elif choice == '1':
        dt = context.user_data[key]
        u = await cache.get(key)
        u.birthday = dt
        await cache.set(u)
        await context.bot.edit_message_text(
            chat_id=q.message.chat_id,
            message_id=q.message.message_id,
            text=u.__str__(),
            parse_mode='HTML'
        )
    else:
        logger.error("Bad callback")
