from .adminKB import *

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


async def start_kb_admin():
    keyboard = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [
                KeyboardButton(text='Добавить вопрос')
            ]
        ]
    )
    return keyboard