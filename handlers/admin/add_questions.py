from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states import questions

from loader import dp, db


@dp.message_handler(text="Добавить вопрос")
async def stock_name(message: types.Message):
    await message.answer("Введите ответ")
    await questions.answer.set()


@dp.message_handler(state=questions.answer)
async def description_stock(message: types.Message, state: FSMContext):
    await state.update_data(name_questions=message.text)
    await questions.next()
    await questions.photo.set()
    await message.answer("Загрузить изображение")


@dp.message_handler(content_types=['photo'], state=questions.photo)
async def description_adds_stock(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id)

    data_state = await state.get_data()
    photo = data_state['photo']
    answer = data_state['name_questions']


    if await db.add_questions(photo, answer):
        await message.answer('Вы успешно добавили вопрос')
    await state.finish()
