from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.user import  main_kb
from states import ProfileSG

from loader import dp, db


@dp.message_handler(text="Зарегистрироватся")
async def stock_name(message: types.Message):
    await message.answer("Введите ваше имя")
    await ProfileSG.first_name.set()


@dp.message_handler(state=ProfileSG.first_name)
async def description_stock(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await ProfileSG.next()
    await ProfileSG.last_name.set()
    await message.answer("Введите вашу фалилию")


@dp.message_handler(state=ProfileSG.last_name)
async def description_stock(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await ProfileSG.next()
    await ProfileSG.midle_name.set()
    await message.answer("Введите вашу отчество")


@dp.message_handler(state=ProfileSG.midle_name)
async def description_stock(message: types.Message, state: FSMContext):
    await state.update_data(midle_name=message.text)
    await ProfileSG.next()
    await ProfileSG.restaraunt.set()
    await message.answer("Введите ваш ресторан в котором работаете")


@dp.message_handler(state=ProfileSG.restaraunt)
async def description_stock(message: types.Message, state: FSMContext):
    await state.update_data(restaraunt=message.text)

    data_state = await state.get_data()
    f_name = data_state['first_name']
    l_name = data_state['last_name']
    m_name = data_state['midle_name']
    restaraunt = data_state['restaraunt']

    if await db.add_user(message.from_user.id, f_name, l_name, m_name, restaraunt, 'Не прошел', 0):
        await message.answer('Вы успешно прошли регистрацию\n'
                             'Вам доступен тест для прохожедния', reply_markup=await main_kb())
    await state.finish()

