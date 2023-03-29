from typing import Any

from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters

from src.bot.handlers.help import help_handler
from src.bot.handlers.info import birthdays
from src.bot.handlers.join_chat import new_member
from src.bot.handlers.nearest import nearest_handler
from src.bot.handlers.reg import reg_handler


def get_handlers() -> list[CommandHandler[CallbackContext | Any]]:
    # ToDo: add handler to set timezone
    return [
        CommandHandler('reg', reg_handler),
        CommandHandler('nearest', nearest_handler),
        CommandHandler('birthdays', birthdays),
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member),

        CommandHandler('help', help_handler),
    ]
