from typing import Final

from aiogram import Router

from . import echo


router: Final[Router] = Router(name=__name__)
router.include_routers(echo.router)
