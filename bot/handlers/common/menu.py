from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import Router
from aiogram.filters import Command

from bot.keyboards.inline import language_keyboard


if TYPE_CHECKING:
    from aiogram.types import Message
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
