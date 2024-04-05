__all__ = ('router', )


from aiogram import Router
from .commands import router as start_commands_router

router = Router(name=__name__)

router.include_router(start_commands_router)