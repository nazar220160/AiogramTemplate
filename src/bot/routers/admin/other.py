from aiogram import F, types

from src.bot.common.filters import IsAdmin
from src.bot.routers.admin.router import admin_router


@admin_router.message(F.photo, IsAdmin())
async def answer_photo_id(message: types.Message):
    photo_id = message.photo[-1].file_id
    await message.answer(photo_id)


@admin_router.message(F.sticker, IsAdmin())
async def answer_sticker_id(message: types.Message):
    sticker_id = message.sticker.file_id
    await message.answer(sticker_id)
