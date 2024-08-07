from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.webhook import aiohttp_server as server
from aiohttp import web


if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher

    from bot.config import Config

from .polling import polling_shutdown, polling_startup
from .webhook import webhook_shutdown, webhook_startup


def run_polling(bot: Bot, dispatcher: Dispatcher) -> None:
    """
    Run the bot in the polling mode.

    :param bot: An instance of the Telegram bot.
    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    """
    dispatcher.startup.register(polling_startup)
    dispatcher.shutdown.register(polling_shutdown)
    dispatcher.run_polling(bot)


def run_webhook(dispatcher: Dispatcher, bot: Bot, config: Config) -> None:
    """
    Run the bot in the webhook mode.

    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    :param bot: An instance of the Telegram bot.
    :param config: An instance of the bot configuration.
    """
    app: web.Application = web.Application()

    server.SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=config.webhook.secret_token.get_secret_value(),
    ).register(app, path=config.webhook.path)
    server.setup_application(app, dispatcher, bot=bot)

    app.update(**dispatcher.workflow_data, bot=bot)

    dispatcher.startup.register(webhook_startup)
    dispatcher.shutdown.register(webhook_shutdown)
    web.run_app(app=app, host=config.webhook.host, port=config.webhook.port)
