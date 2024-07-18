from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import Router

from bot.keyboards.inline.factory import Language
from bot.utils.commands import set_commands


if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import CallbackQuery
    from aiogram_i18n import I18nContext


router: Final[Router] = Router(name=__name__)


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
