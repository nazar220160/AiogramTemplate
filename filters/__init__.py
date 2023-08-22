from aiogram import Dispatcher

from filters.main import IsAdmin


def register_all_filters(dp: Dispatcher):
    filters = (
        IsAdmin,
    )
    for bound_filter in filters:
        dp.message.filter(bound_filter)
