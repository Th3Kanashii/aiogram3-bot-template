from typing import Final

from aiogram import Router

from . import language, start


router: Final[Router] = Router(name=__name__)
router.include_routers(start.router, language.router)
