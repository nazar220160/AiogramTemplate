from src.bot.routers.admin.main import *  # noqa

from src.bot.routers.admin.com_sub import *  # noqa
from src.bot.routers.admin.newsletter import *  # noqa
from src.bot.routers.admin.admins import *  # noqa
from src.bot.routers.admin.ban_users import *  # noqa

from src.bot.routers.admin.support import *  # noqa
from src.bot.routers.admin.other import *  # noqa

from src.bot.routers.admin.router import admin_router

__all__ = ("admin_router",)
