from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def main_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="Начать прохождение теста")
            ]
        ]
    )
    return keyboard


async def registr_user() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="Зарегистрироватся")
            ]
        ]
    )
    return keyboard