import smtplib

from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.admin import adminKB
from keyboards.default.user.main_user_KD import registr_user, main_kb
from loader import dp, db, bot

from aiogram import types
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import random

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
            result = await db.get_percent_users(message.from_user.id)
            new_res = result[0]
            f_new = float(new_res)
            await message.answer('Вы уже проходили данный тест\n'
                                 f'Вы прошли тест на {round(int(f_new), 1)} %')


async def send_email(message):
    sender = "uvalovtutas@gmail.com"
    password = 'vladvlad67'

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        
        msg['Subject'] = 'Пользователь Прошел тест'
        server.sendmail(sender, 'kristina.pastushenko@kfc-vostok.by', msg.as_string())
        server.sendmail(sender, 'pavle4kovlad@yandex.by', msg.as_string())

        return print("Сообщение отправлено")
    except Exception as _ex:
        return print(f'{_ex}\nПроверте email или пароль')


@dp.message_handler(commands=["create_database", "create_db", ])
async def create_database(message: types.Message):
    await message.answer(text="База данных успешно создана!")
    await db.create_all_database()


@dp.message_handler(commands=["moderator", "admin", ])
async def create_database(message: types.Message):
    await message.answer(text="Вы вошли как админ", reply_markup=await adminKB.start_kb_admin())


@dp.message_handler(commands=["test_email"])
async def create_database(message: types.Message):
    await message.answer(text="Данные успешно отправлены на почту", reply_markup=await adminKB.start_kb_admin())
    user = await db.get_users(message.from_user.id)
    l_name = user[0][2]
    f_name = user[0][3]
    m_mane = user[0][4]
    restaurant = user[0][5]
    percentage_correct_answers = user[0][7]
    wrong_answer = user[0][10]

    data = []
    description = ''
    data = wrong_answer.split(' ')

    for i in data:
        if i != '':
            questins_descriptions = await db.get_questions(int(i))
            description += f'Вопрос {questins_descriptions[0][0]}:' + questins_descriptions[0][3] + '\n\n'
            print('asd')
    print('asd')




    await send_email(f"Персональные данные пользователя:\n"
                         f"Фамилия - {user[0][2]}\n"
                         f"Имя - {user[0][3]}\n"
                         f"Отчество - {user[0][4]}\n"
                         f"Ресторан {user[0][5]}\n\n"
                         f"Статистика по тесту пользователя {user[0][2]}:\n"
                         f"Всего вопросов 6 в тесте\n"
                         f"Прошел тест на 25 %\n"
                         f"Ответил правильно - 2\n\n"
                         f"Статистика по Ошибкам\n"
                         f"Допустил ошибок - 4\n {description}")


