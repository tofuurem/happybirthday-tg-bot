from telegram import Update
from telegram.ext import ContextTypes
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.bot.birthday_utils import create_birthday_message
from src.storage.cache import Cache


@inject
async def _test_try(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    key = (update.effective_user.id, update.effective_chat.id)
    user = await cache.get(key)

    text = create_birthday_message([user])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode='HTML'
    )
