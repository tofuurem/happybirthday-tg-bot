import random
import re
from datetime import datetime

from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes

from src.bot.functions.time import to_datetime
from src.container import Container
from src.dao.dto.database import Chat, User, Association
from src.dao.storage.cache import Cache


def _now():
    n = datetime.now()
    return to_datetime(n.strftime('%d.%m'))


@inject
async def nearest_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    await cache.update_if_not_exists(tg_chat=update.effective_chat, tg_user=update.effective_user)

    now = _now()
    users = [
        u
        for u in sorted(await cache.users_by_room(update.effective_chat.id), key=lambda x: getattr(x, 'birthday'))
        if u.birthday > now
    ]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Nearest users birthdays:\n{0}".format(
            "\n".join(["{0:15s} {1}".format(u.name, u.birthday.strftime('%d.%m')) for u in users])
        ),
        parse_mode='HTML'
    )
