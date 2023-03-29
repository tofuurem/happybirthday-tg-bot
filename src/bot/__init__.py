from typing import Any

from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters

from src.bot.handlers.help import help_handler
from src.bot.handlers.reg import reg_handler


def get_handlers() -> list[CommandHandler[CallbackContext | Any]]:
    # ToDo: add handler to set timezone
    return [
        CommandHandler('reg', reg_handler),
        # CommandHandler('nearest', ),
        # CommandHandler('birthdays', ),
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, ),

        CommandHandler('help', help_handler),
    ]
