from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import loggers

from bot.utils.commands import set_default_commands


if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher
    from aiogram_i18n import I18nMiddleware
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

    from bot.config import Config


async def webhook_startup(dispatcher: Dispatcher, bot: Bot, config: Config) -> None:
    """
    Set webhook for main bot.

    :param bot: An instance of the Telegram bot.
    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    :param config: An instance of the bot configuration.
    """
    url: str = config.webhook.url
    i18n: I18nMiddleware = dispatcher["i18n_middleware"]
    with i18n.use_context() as _i18n:
        await set_default_commands(bot=bot, i18n=_i18n)

    if await bot.set_webhook(
        url=url,
        allowed_updates=dispatcher.resolve_used_update_types(),
        secret_token=config.webhook.secret_token.get_secret_value(),
        drop_pending_updates=config.bot.drop_pending_updates,
    ):
        return loggers.webhook.info("Main bot webhook successfully set on url '%s'", url)
    return loggers.webhook.error("Failed to set main bot webhook on url '%s'", url)


async def webhook_shutdown(bot: Bot, dispatcher: Dispatcher, config: Config) -> None:
    """
    Drop webhook for bot.

    :param bot: An instance of the Telegram bot.
    :param dispatcher: An instance of the Dispatcher for the Telegram bot.
    :param config: An instance of the bot configuration.
    """
    if not config.webhook.reset:
        return

    if await bot.delete_webhook():
        loggers.webhook.info("Dropped main bot webhook.")
    else:
        loggers.webhook.error("Failed to drop bot webhook.")

    session_pool: async_sessionmaker[AsyncSession] = dispatcher["session_pool"]
    async with session_pool() as session:
        await session.close_all()
        await session.bind.dispose()

    await dispatcher.storage.close()
    await bot.session.close()
