from telegram import Update
from telegram.ext import ContextTypes


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
