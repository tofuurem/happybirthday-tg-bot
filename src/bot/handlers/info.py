from datetime import date

from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes

from src.container import Container
from src.dao.storage.cache import Cache


@inject
async def birthdays(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    """
    Returns info about user and their birthdays

    like:
        user1 22.10.1987
        user2 10.12.1934
    """

    user, chat = await cache.get_user_and_chat(update.effective_chat, update.effective_user, lazy=True)
    text = "Users with birthdays ({0}/{1}):\n{2}".format(
        chat.users,
        await update.effective_chat.get_member_count(),
        "\n".join(["{0:15s} {1}".format(u.name, user.birthday.strftime('%d.%m')) for u in chat.users])
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode='HTML'
    )
