from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import Router


if TYPE_CHECKING:
    from aiogram.types import Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser

router: Final[Router] = Router(name=__name__)


@router.message()
async def echo(message: Message, i18n: I18nContext, user: DBUser) -> None:
    """
    Handle for echoing messages.

    :param message: The object represents a message.
    :param i18n: The i18n context object.
    :param user: The object represents a user in the database.
    """
    try:
        await message.copy_to(chat_id=user.id)
    except TypeError:
        await message.answer(text=i18n.get("something-went-wrong"))
