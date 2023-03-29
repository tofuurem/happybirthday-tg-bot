from loguru import logger

from telegram.ext import ContextTypes
from dependency_injector.wiring import Provide

from src.container import Container
from src.bot.functions.birthday_utils import check_birthday
from src.dao.storage.cache import Cache


async def birthday_notify(
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    """
    Notify about birthday of users
    """
    all_users = await cache.get_all_users()
    pretty_data = check_birthday(list(all_users))
    if not pretty_data:
        logger.info('No birthdays today')
        return

    data = await cache.get_chats_for_users(pretty_data)

    for user, chats in data.items():
        for chat in chats:
            await context.bot.send_message(
                chat_id=chat.tg_id,
                text="""
                        У нас тут день варенья у кое кого....
                        @{0} - {1} <i>фото_члена.jpg</i>
                    """.format(user.user_name, user.first_name),
                parse_mode='HTML'
            )
