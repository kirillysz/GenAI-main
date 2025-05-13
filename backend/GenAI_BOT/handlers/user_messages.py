from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router

from keyboards.inline.inline import keyboard

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("welcome", reply_markup=keyboard)
