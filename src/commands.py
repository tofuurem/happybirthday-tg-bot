import re
from datetime import datetime, date
from typing import Any

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, CallbackContext, CallbackQueryHandler

from dependency_injector.wiring import inject, Provide
from loguru import logger

from container import Container
from src.birthday_utils import create_birthday_message
from src.entities import User
from src.redis_cache import Cache


def _to_datetime(dt: str | None) -> date | None:
    if dt is None:
        return None
    splitter = re.search(r'[./-]', dt).group()
    fmt = '%d{0}%m{0}%Y'.format(splitter)
    return datetime.strptime(dt, fmt).date()


@inject
async def _callback_reg_query(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == '0':
        await context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text='Ваши данные остались теми же.',
            parse_mode='HTML'
        )
    elif choice == '1':
        key = (update.effective_user.id, update.effective_chat.id)
        dt = context.user_data[key]
        u = await cache.get(key)
        u.birthday = dt
        await cache.set(u)
        await context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=u.__str__(),
            parse_mode='HTML'
        )
    else:
        logger.error("Bad callback")


@inject
async def _reg(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    """
    Registration user with Optional argument for birthday

    using:
        /reg            - save without birthday

        /reg {date_arg: str | optional}

        ### format mm{./-}dd{./-}YYYY
        /reg 01.01.2001 - save with birthday
        /reg 01/01/2001 - save with birthday
        /reg 01-01-2001 - save with birthday

    :param update:
    :param context:
    :return:
    """
    key = (update.effective_user.id, update.effective_chat.id)
    user = await cache.get(key)
    dt = re.findall(r'\d{2}[./-]\d{2}[./-]\d{4}', context.args[0]) if context.args else None

    if (context.args and len(context.args) > 1) or (context.args and not dt):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Уважаемый <i>{}</i> вводите валидный формат данных'.format(
                update.effective_user.name),
            parse_mode='HTML'
        )
        return
    if user and dt and dt != user.birthday:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Вы {0} уверены, что хотите заменить {1} на {2} дату?'.format(
                user.name,
                user.birthday.strftime('%d.%m.%Y'),
                dt[0]
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton("Да", callback_data='1'),
                        InlineKeyboardButton("Нет", callback_data='0')
                    ]
                ],
                one_time_keyboard=True
            )
        )
        context.user_data[key] = _to_datetime(dt[0])
        return
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
        await cache.set(user)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=user.__str__(), parse_mode='HTML')


@inject
async def _users_info(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    """
    Returns info about user and their birthdays

    like:
        user1: 22.10.1987
        user2: 10.12.1934

    :param update:
    :param context:
    :return:
    """
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


@inject
async def _fullness_check(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    """
    Check that count users in chat equals users in cache
    :param update:
    :param context:
    :return:
    """
    # ToDo: get only users without bots
    member_count = await update.effective_chat.get_member_count()
    users = [u for u in await cache.dall_users() if u.group_id == update.effective_chat.id]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Statistic {}/{} (reg member with birthday/members in chat)".format(len(users), member_count)
    )


async def _help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " The following commands are available:\n"
    commands = [
        ["/reg", "Registration user with Optional argument for birthday,\n{like:15s}: /reg 01.01.2001"],
        ["/info", "Returns info about user and their birthdays"],
        ["/fullness", "Check that count users in chat equals users in cache"],
        ["/help", "Get this message"]
    ]
    for command in commands:
        text += f"{command[0]:10s} - {command[1]}\n"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


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


def get_handlers() -> list[CommandHandler[CallbackContext | Any]]:
    # ToDo: add handler to set timezone
    return [
        CommandHandler('reg', _reg),
        CommandHandler('info', _users_info),
        CommandHandler('fullness', _fullness_check),
        CommandHandler('test', _test_try),
        CommandHandler('help', _help),
        CallbackQueryHandler(_callback_reg_query)
    ]
