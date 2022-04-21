from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.admin import adminKB
from keyboards.default.user.main_user_KD import registr_user, main_kb
from loader import dp, db, bot


import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import deep_linking

from states import ProfileSG


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!')
    res = await db.get_id_users(message.from_user.id)

    if res is None:
        await message.answer('Что бы пройти тест необходимо пройти регистрацию', reply_markup=await registr_user())
    else:
        if res[0] == 'Не прошел':
            await message.answer('Вы еще не прошли опрос', reply_markup=await main_kb())
        else:
            correct_answer = await db.get_correct_answer_users(message.from_user.id)
            result = float(100 / int(correct_answer[0]))

            if res < 90:
                await message.answer('Вы уже проходили данный тест\n '
                                     'Вам необходимо подтянуть знания\n '
                                     f'Вы прошли тест на {round(result, 1)} %')
            else:
                await message.answer('Вы уже проходили данный тест\n'
                                     'Поздравляем вы хорошо владеете стандартами'
                                     f'Вы прошли тест на {round(result, 1)} %')


@dp.message_handler(commands=["create_database", "create_db", ])
async def create_database(message: types.Message):
    await message.answer(text="База данных успешно создана!")
    await db.create_all_database()


@dp.message_handler(commands=["moderator", "admin", ])
async def create_database(message: types.Message):
    await message.answer(text="Вы вошли как админ", reply_markup=await adminKB.start_kb_admin())



