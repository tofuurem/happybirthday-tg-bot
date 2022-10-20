from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.storage.cache import Cache


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
