from enum import StrEnum, auto


class Locale(StrEnum):
    """
    Enumeration representing supported locales.
    """

    EN = auto()
    UK = auto()

    DEFAULT = EN
