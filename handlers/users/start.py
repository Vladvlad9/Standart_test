from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.user.main_user_KD import main_kb
from loader import dp, db, bot


import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import deep_linking


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!')
    res = await db.get_id_users(message.from_user.id)

    if res[0] == 'Не прошел':
        await message.answer('Вы еще не прошли опрос', reply_markup= await main_kb())
    else:
        await message.answer('Вы уже проходили данный тест\n'
                             'Вы прошли тест на "__баллы__"')


@dp.message_handler(commands=["create_database", "create_db", ])
async def create_database(message: types.Message):
    await message.answer(text="База данных успешно создана!")
    await db.create_all_database()

