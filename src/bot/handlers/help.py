from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes


async def _help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " The following commands are available:\n"
    commands = [
        ["/reg", "Registration user with Optional argument for birthday,\n{0:15s}like: /reg 01.01.2001".format(' ')],
        ["/sex", "Choose sex for user"],
        ["/info", "Returns info about user and their birthdays"],
        ["/fullness", "Check that count users in chat equals users in cache"],
        ["/help", "Get this message"]
    ]
    for command in commands:
        text += f"{command[0]:10s} - {command[1]}\n"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
