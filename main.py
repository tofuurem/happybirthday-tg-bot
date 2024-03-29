import sys

import pytz
from loguru import logger
from telegram.ext import ApplicationBuilder, Application, Defaults

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
                sys.modules["src.bot.handlers.birthdays"],
                sys.modules["src.bot.handlers.reg"],
                sys.modules["src.bot.handlers.join_chat"],
                sys.modules["src.bot.handlers.nearest"],
                sys.modules["src.bot.handlers.help"],
            ]
        )
        self._container.init_resources()

    def _init_app(self) -> Application:
        defaults = Defaults(tzinfo=pytz.timezone('Europe/Moscow'))
        _app = ApplicationBuilder().token(self._container.config().tg_token).defaults(defaults).build()
        _app.add_handlers(get_handlers())

        jq = _app.job_queue
        first = seconds_first_start()
        _ = jq.run_repeating(birthday_notify, interval=86400, first=first)
        return _app

    def run(self) -> None:
        logger.info('start bot')
        self._app.run_polling()


if __name__ == '__main__':
    app = App()
    app.run()
