from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import Router
from aiogram.filters import CommandStart


if TYPE_CHECKING:
    from aiogram.types import Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser


router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message, i18n: I18nContext, user: DBUser) -> None:
    """
    Handle the /start command.

    :param message: The object represents a message.
    :param i18n: The i18n context.
    :param user: The user.
    """
    await message.answer(text=i18n.get("start", name=user.mention))
