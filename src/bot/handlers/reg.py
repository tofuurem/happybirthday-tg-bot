import random
import re

from dependency_injector.wiring import inject, Provide
from telegram import Update
from telegram.ext import ContextTypes

from src.bot.functions.time import to_datetime
from src.container import Container
from src.dao.dto.database import Chat, User, Association
from src.dao.storage.cache import Cache

answers = [
    "Знакомые лица:3",
    "Ооо, кто это тут у нас:3",
    "Хох, новых друзей решил найти человечешка?",
    "Знакомые лица:3 Ну вас то я помню",
    "Ой куда не зайду тебя вижу, хватит так много общаться -_-"
]


@inject
async def reg_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    """
        Registration user with Optional argument for birthday
    """
    chat = await cache.get_model(update.effective_chat.id, Chat)
    if not chat:
        chat = Chat(tg_id=update.effective_chat.id, title=update.effective_chat.title)
        await cache.add_model(chat)

    user = await cache.get_model(update.effective_user.id, User)
    if not user:
        user = User(
            tg_id=update.effective_user.id,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name,
            user_name=update.effective_user.username,
        )
        await cache.add_model(user)

    if not await cache.is_user_in_room(update.effective_user.id, update.effective_chat.id):
        chat_user = Association(user_id=user.id, chat_id=chat.id)
        await cache.add_model(chat_user)

    if user.birthday:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=random.choice(answers),
            parse_mode='HTML'
        )

        return

    dt = re.search(r'\d{2}[./-]\d{2}([./-]\d{4})?', context.args[0]) if context.args else None
    if dt:
        dt = to_datetime(dt.group())

    if not dt:
        # message about sosi hui i delay normalno
        text = 'Уважаемый <i>{}</i> вводите валидный формат данных'.format(update.effective_user.name),
    else:
        text = 'Запомнил и записал!'
        user.birthday = dt
        await cache.add_model(user)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='HTML')
