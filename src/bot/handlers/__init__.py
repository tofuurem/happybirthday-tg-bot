from typing import Any

from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler

from src.bot.handlers.callbacks import _callback_reg_query
from src.bot.handlers.fullness import _fullness_check
from src.bot.handlers.help import _help
from src.bot.handlers.info import _users_info
from src.bot.handlers.reg import _reg
from src.bot.handlers.sex import _choose_sex
from src.bot.handlers.test_try import _test_try


def get_handlers() -> list[CommandHandler[CallbackContext | Any]]:
    # ToDo: add handler to set timezone
    return [
        CommandHandler('reg', _reg),
        CommandHandler('info', _users_info),
        CommandHandler('fullness', _fullness_check),
        CommandHandler('test', _test_try),
        CommandHandler('sex', _choose_sex),
        CommandHandler('help', _help),
        CallbackQueryHandler(_callback_reg_query)
    ]
