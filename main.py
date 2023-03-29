import sys

from telegram.ext import ApplicationBuilder, Application

from src.bot import get_handlers
from src.container import Container

from src.bot.functions.tasks import birthday_notify
from src.bot.functions.time import seconds_first_start


class App:

    def __init__(self):
        self._container = Container()
        self.__init_container()
        self._app = self._init_app()

    def __init_container(self) -> None:
        self._container.wire(
            modules=[
                sys.modules[__name__],
                sys.modules["src.bot.handlers.info"],
                sys.modules["src.bot.handlers.reg"],
                sys.modules["src.bot.handlers.join_chat"],
                sys.modules["src.bot.handlers.nearest"],
                sys.modules["src.bot.handlers.help"],
            ]
        )
        self._container.init_resources()

    def _init_app(self) -> Application:
        # ToDo: add https://github.com/python-telegram-bot/python-telegram-bot/wiki/Adding-defaults-to-your-bot
        _app = ApplicationBuilder().token(self._container.config().tg_token).build()
        _app.add_handlers(get_handlers())
        # jq = _app.job_queue

        # first = seconds_first_start()
        # job_daily = jq.run_repeating(birthday_notify, interval=first + 86400, first=first)
        return _app

    def run(self) -> None:
        self._app.run_polling()


if __name__ == '__main__':
    app = App()
    app.run()
