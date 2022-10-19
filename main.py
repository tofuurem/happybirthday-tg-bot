from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from config import Configuration
from src.commands import get_handlers


from src.tasks import birthday_notify


if __name__ == '__main__':
    cfg = Configuration()

    app = ApplicationBuilder().token(cfg.tg_token).build()
    app.add_handlers(get_handlers())
    jq = app.job_queue

    job_daily = jq.run_repeating(birthday_notify, interval=86400, first=1)  # every day

    app.run_polling()
