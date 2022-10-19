import re
from datetime import datetime, date
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, CallbackContext

from src import cache
from src.entities import User


def _to_datetime(dt: str | None) -> date | None:
    if dt is None:
        return None

    splitter = re.search(r'[./-]', dt).group()
    fmt = '%d{0}%m{0}%Y'.format(splitter)
    return datetime.strptime(dt, fmt).date()


async def _reg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Registration user with Optional argument for birthday

    using:
        /reg            - save without birthday

        ### format mm{./-}dd{./-}YYYY
        /reg 01.01.2001 - save with birthday
        /reg 01/01/2001 - save with birthday
        /reg 01-01-2001 - save with birthday

    :param update:
    :param context:
    :return:
    """
    # ToDo: заполнять недостающую информацию о пользователе
    key = (update.effective_user.id, update.effective_chat.id)
    user = await cache.get(key)

    dt = re.findall(r'\d{2}[./-]\d{2}[./-]\d{4}', context.args[0])[0] if context.args else None
    if user and not user.birthday and dt:
        user.birthday = _to_datetime(dt)
    elif user and not dt and user.birthday:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Вы уже зарегистрировались',
            parse_mode='HTML'
        )
        return
    else:
        user = User(
            tg_id=update.effective_user.id,
            group_id=update.effective_chat.id,
            name=update.effective_user.name,
            birthday=_to_datetime(dt)
        )
    await cache.set(key, user)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=user.__str__(), parse_mode='HTML')


async def _users_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Returns info about user and their birthdays

    like:
        user1: 22.10.1987
        user2: 10.12.1934

    :param update:
    :param context:
    :return:
    """
    # ToDo: select with group chat id
    data = await cache.all_chat_str(update.effective_chat.id)
    if not data:
        text = 'No data about users in this chat'
    else:
        text = f" All users with birthdays:\n{data}"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode='HTML'
    )


async def _fullness_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Check that count users in chat equals users in cache
    :param update:
    :param context:
    :return:
    """
    pass


async def _help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " The following commands are available:\n"
    commands = [
        ["/reg", "Registration user with Optional argument for birthday,\n     like: /reg 01.01.2001"],
        ["/info", "Returns info about user and their birthdays"],
        ["/fullness", "Check that count users in chat equals users in cache"],
        ["/help", "Get this message"]
    ]
    for command in commands:
        text += f"{command[0]:10s} - {command[1]}\n"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def get_handlers() -> list[CommandHandler[CallbackContext | Any]]:
    # ToDo: add handler to set timezone
    return [
        CommandHandler('reg', _reg),
        CommandHandler('info', _users_info),
        CommandHandler('fullness', _fullness_check),
        CommandHandler('help', _help)
    ]
