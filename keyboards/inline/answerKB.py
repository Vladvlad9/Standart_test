from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db
import random


async def answer(count: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        row_width=1
    )
    all_anser = []
    answer = await db.get_answer()

    for j in answer:
        all_anser.append(j[1])

    random.shuffle(all_anser)

    for answ in all_anser:
        keyboard.add(*[InlineKeyboardButton(text=f"{answ}", callback_data=f"answer_{answ}_{count}")])

    keyboard.add(*[InlineKeyboardButton(text=f"Следующий вопрос", callback_data=f"next_{count}")])

    return keyboard