from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault


if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram_i18n import I18nContext


async def _remove_commands(bot: Bot, chat_id: int | str | None = None) -> None:
    """
    Remove commands from the chat.

    :param bot: Bot instance.
    :param chat_id: Chat ID.
    """
    if not chat_id:
        await bot.delete_my_commands(scope=BotCommandScopeDefault())
        return

    await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=chat_id))


async def set_default_commands(bot: Bot, i18n: I18nContext) -> None:
    """
    Set default commands for the bot.

    :param bot: Bot instance.
    :param i18n: I18nContext instance.
    """
    await _remove_commands(bot=bot)
    await bot.set_my_commands(
        commands=[
            BotCommand(command="language", description=i18n.get("command-language")),
        ],
        scope=BotCommandScopeDefault(),
    )


async def set_commands(bot: Bot, chat_id: int | str, i18n: I18nContext) -> None:
    """
    Set commands for the chat.

    :param bot: Bot instance.
    :param chat_id: Chat ID.
    :param i18n: I18nContext instance.
    """
    await _remove_commands(bot=bot, chat_id=chat_id)
    await bot.set_my_commands(
        commands=[
            BotCommand(command="language", description=i18n.get("command-language")),
        ],
        scope=BotCommandScopeChat(chat_id=chat_id),
    )
