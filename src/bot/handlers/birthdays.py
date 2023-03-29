from datetime import date

from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes

from src.container import Container
from src.dao.storage.cache import Cache


@inject
async def birthdays_handler(
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

    await cache.update_if_not_exists(tg_chat=update.effective_chat, tg_user=update.effective_user, lazy=True)
    users = [u for u in await cache.users_by_room(update.effective_chat.id) if u.birthday]
    text = "Users with birthdays ({0}/{1}):\n{2}".format(
        len(users),
        # -1 because bot not user:/
        await update.effective_chat.get_member_count() - 1,
        "\n".join(["{0:15s} {1}".format(u.name, u.birthday.strftime('%d.%m')) for u in users])
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode='HTML'
    )
