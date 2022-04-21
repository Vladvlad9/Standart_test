from aiogram import types

from keyboards.inline.answerKB import answer
from loader import dp, db, bot


@dp.message_handler(text="Начать прохождение теста")
async def back_main_menu(message: types.Message):
    count = 1
    questions = await db.get_questions(count)
    await message.answer(f'Вопрос № {questions[0][0]}\n'
                         f'{questions[0][2]}', reply_markup=await answer(count))


async def update_questions(message: types.Message, questions, count_questions, next_questions):
    if count_questions == 200:
        await message.answer(f'{questions}')
    else:
        await message.edit_text(f'Вопрос № {count_questions}\n'
                                f' {questions}', reply_markup=await answer(next_questions))


@dp.callback_query_handler(lambda call: "next_" in call.data)
async def next_questions(call: types.CallbackQuery):
    current_questions = call.data.split("_")[1]

    next_question = int(current_questions) + 1

    questions = await db.get_questions(int(next_question))
    a = await db.get_all_questions()

    count_questions = int(a[0])

    if count_questions > int(current_questions):
        await update_questions(call.message, questions[0][2], questions[0][0], next_question)

    else:
        await update_questions(call.message, 'Вы ответили на вопросы', 200, next_question)


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
        if answer == current_questions[0][3]:  # если пользователь ответил правильно
            correct_answer = await db.get_correct_answer_users(call.from_user.id)
            new_correct = int(correct_answer[0]) + 1
            await db.update_correct_answer(new_correct, call.from_user.id)

        await update_questions(call.message, next_questions[0][2], next_questions[0][0], next_question)

    else:
        await update_questions(call.message, 'Вы ответили на вопросы', 200, next_question)


