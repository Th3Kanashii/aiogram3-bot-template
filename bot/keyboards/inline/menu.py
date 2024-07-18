from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.enums.locale import Locale

from .factory import Language


if TYPE_CHECKING:
    from aiogram.types import InlineKeyboardMarkup


def language_keyboard() -> InlineKeyboardMarkup:
    """
    Select language keyboard

    :return: InlineKeyboardMarkup with language selection
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard.row(
        *[
            InlineKeyboardButton(text="🇬🇧", callback_data=Language(language=Locale.EN).pack()),
            InlineKeyboardButton(text="🇺🇦", callback_data=Language(language=Locale.UK).pack()),
        ],
        width=2,
    )
    return keyboard.as_markup()
