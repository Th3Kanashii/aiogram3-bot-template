from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import Router
from aiogram.filters import Command

from bot.keyboards.inline import Language, language_keyboard
from bot.utils import set_commands


if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import CallbackQuery, Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser


router: Final[Router] = Router(name=__name__)


@router.message(Command("language"))
async def language_command(message: Message, i18n: I18nContext, user: DBUser) -> None:
    """
    Handle the /language command.
    Show the language selection keyboard.

    :param message: The object represents a message.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await message.answer(i18n.get("language", name=user.mention), reply_markup=language_keyboard())


@router.callback_query(Language.filter())
async def language_callback(
    callback: CallbackQuery,
    callback_data: Language,
    bot: Bot,
    i18n: I18nContext,
) -> None:
    """
    Handle the language selection callback.
    Set the user language.

    :param callback: The object represents a callback query.
    :param callback_data: The object represents the callback data.
    :param bot: An instance of the Telegram bot.
    :param i18n: The i18n context object.
    """
    await i18n.set_locale(locale=callback_data.language)
    await set_commands(bot=bot, chat_id=callback.from_user.id, i18n=i18n)
    await callback.message.edit_text(text=i18n.get("language-changed"))
