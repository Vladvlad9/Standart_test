from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.edit_question import Edit_Question

from loader import dp, db


@dp.message_handler(text="Изменить вопрос")
async def stock_name(message: types.Message):
    await message.answer("Введите номер вопроса")
    await Edit_Question.id.set()


@dp.message_handler(state=Edit_Question.id)
async def description_stock(message: types.Message, state: FSMContext):
    await state.update_data(id=message.text)
    await Edit_Question.next()
    await Edit_Question.img.set()
    await message.answer("Загрузить изображение")


@dp.message_handler(content_types=['photo'], state=Edit_Question.img)
async def description_adds_stock(message: types.Message, state: FSMContext):
    await state.update_data(img=message.photo[0].file_id)

    data_state = await state.get_data()
    img = data_state['img']
    id = data_state['id']

    await db.update_question(img, id)
    await message.answer('Вы успешно изменили вопрос вопрос')
    await state.finish()
