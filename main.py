import sys

from telegram.ext import ApplicationBuilder, Application, JobQueue

from src.bot.handlers import get_handlers
from src.container import Container

from src.bot.tasks import birthday_notify
from src.bot.time import seconds_first_start


class App:

    def __init__(self):
        self._container = Container()
        self.__init_container()
        self._app = self._init_app()

    def __init_container(self) -> None:
        self._container.wire(
            modules=[
                sys.modules[__name__],
                sys.modules["src.bot.tasks"],
                sys.modules["src.bot.handlers.fullness"],
                sys.modules["src.bot.handlers.help"],
                sys.modules["src.bot.handlers.info"],
                sys.modules["src.bot.handlers.reg"],
                sys.modules["src.bot.handlers.sex"],
                sys.modules["src.bot.handlers.test_try"],
                sys.modules["src.bot.handlers.callbacks"],
            ]
        )
        self._container.init_resources()

    def _init_app(self) -> Application:
        # ToDo: add https://github.com/python-telegram-bot/python-telegram-bot/wiki/Adding-defaults-to-your-bot
        _app = ApplicationBuilder().token(self._container.config().tg_token).build()
        _app.add_handlers(get_handlers())
        jq: JobQueue = _app.job_queue

        _ = jq.run_once(birthday_notify, 1)

        first = seconds_first_start()
        _ = jq.run_repeating(birthday_notify, interval=first + 86400, first=first)

        return _app

    def run(self) -> None:
        self._app.run_polling()


if __name__ == '__main__':
    app = App()
    app.run()
