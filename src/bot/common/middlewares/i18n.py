from typing import Final

from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware

from src.core.config import Config

DEFAULT_LOCALE_PATH: str = Config.path("src", "bot", "common", "locales")
DEFAULT_LOCALE: Final[str] = 'en'

i18n = I18n(path=DEFAULT_LOCALE_PATH, default_locale=DEFAULT_LOCALE)
simple_locale_middleware = SimpleI18nMiddleware(i18n)

gettext = i18n.gettext
