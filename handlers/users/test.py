from aiogram import types
from aiogram.types import InputMediaPhoto

from keyboards.inline.answerKB import answer
from loader import dp, db, bot


@dp.message_handler(text="Начать прохождение теста")
async def back_main_menu(message: types.Message):
    count = 1
    questions = await db.get_questions(count)
    markup = types.InlineKeyboardMarkup()
    types.InlineKeyboardMarkup()

    #await message.answer(f'Вопрос № {questions[0][0]}', reply_markup= markup)
    await message.answer_photo(questions[0][1], caption=f'Вопрос № {questions[0][0]}', reply_markup=await answer(count))



async def update_questions(message: types.Message, questions, count_questions, next_questions, img, user_id):
    #await message.edit_caption(caption='asd')
    if count_questions == 200:
        correct_answer = await db.get_correct_answer_users(user_id)

        count_all_questions = await db.get_all_questions()  # Колличество всех вопросов
        un_correct_answer = int(count_all_questions[0]) - int(correct_answer[0])
        result = float(100 / un_correct_answer)

        await db.update_passet_answer('Прошел', user_id)

        await message.answer(f'{questions}\n'
                             f'Ваш результат: {round(result, 1)} %')
    else:
        # await bot.edit_message_text(text=f'Вопрос № {count_questions}\n'
        #                             f' {questions}', chat_id=message.chat.id,
        #                             message_id=message.message_id, inline_message_id=message.message_id)

        await bot.edit_message_media(InputMediaPhoto(img),  message.chat.id, message_id=message.message_id, reply_markup=await answer(next_questions))




@dp.callback_query_handler(lambda call: "answer_" in call.data)
async def user_answer(call: types.CallbackQuery):
    current_int_questions = call.data.split("_")[2]  # текущий вопрос
    answer = call.data.split("_")[1]  # выбранный ответ

    next_question = int(current_int_questions) + 1

    current_questions = await db.get_questions(int(current_int_questions))  # выводим текущий вопрос
    next_questions = await db.get_questions(int(next_question))  # выводим следующий вопрос

    count_all_questions = await db.get_all_questions()  # Колличество всех вопросов

    count_questions = int(count_all_questions[0])  # преобразуем в число

    if count_questions > int(current_int_questions):  # проверяем вопрос
        if answer == current_questions[0][2]:  # если пользователь ответил правильно
            correct_answer = await db.get_correct_answer_users(call.from_user.id)
            new_correct = int(correct_answer[0]) + 1
            await db.update_correct_answer(new_correct, call.from_user.id)

        await update_questions(call.message, next_questions[0][2], next_questions[0][0], next_question,
                               str(next_questions[0][1]), call.from_user.id)
    else:
        await update_questions(call.message, 'Вы ответили на вопросы', 200, next_question, current_questions[0][1], call.from_user.id)
