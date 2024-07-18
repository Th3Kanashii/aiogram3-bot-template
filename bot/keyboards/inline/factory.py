from aiogram.filters.callback_data import CallbackData


class Language(CallbackData, prefix="language"):
    """
    Language callback data
    """

    language: str
