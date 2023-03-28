import re

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from dependency_injector.wiring import inject, Provide

from src.bot.time import to_datetime
from src.container import Container


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
                user.birthday.strftime('%d.%m.%Y') if user.birthday else 'None',
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
        context.user_data[key] = to_datetime(dt[0])
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
            birthday=to_datetime(dt)
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
    data = await cache.all_chat_str('*_{}'.format(update.effective_chat.id))
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
async def _choose_sex(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    """
    Choose sex for user
    :param update:
    :param context:
    :return:
    """
    key = (update.effective_user.id, update.effective_chat.id)
    user = await cache.get(key)

    if not user:
        await context.bot.send_message(update.effective_chat.id, text="Для начала зарегистрируйтесь: /reg dd.mm.yyyy")
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Выберете пол:',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton("М", callback_data='М'),
                    InlineKeyboardButton("Ж", callback_data='Ж')
                ]
            ],
            one_time_keyboard=True
        )
    )


async def _help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " The following commands are available:\n"
    commands = [
        ["/reg", "Update user info about birthday in formats %d.%m.%y or %d.%m"],
        ["/nearest", "Get nearest 3 birthdays"],
        ["/birthdays", "Returns info about chat and all users birthdays"],
        ["/help", "Get this message"]
    ]
    for command in commands:
        text += f"{command[0]:10s} - {command[1]}\n"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
