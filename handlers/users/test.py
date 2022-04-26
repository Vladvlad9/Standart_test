import random

from aiogram import types
from aiogram.types import InputMediaPhoto

from handlers.users.start import send_email
from keyboards.inline.answerKB import answer
from loader import dp, db, bot



@dp.message_handler(text="Начать прохождение теста")
async def back_main_menu(message: types.Message):
    count = 1
    questions = await db.get_questions(count)
    markup = types.InlineKeyboardMarkup()
    types.InlineKeyboardMarkup()

    user = await db.get_users(message.from_user.id)
    if user[0][6] == 'Не прошел':
        await message.answer_photo(questions[0][1], caption=f'Вопрос № {questions[0][0]}', reply_markup=await answer(count))
    else:
        present = float(user[0][8])
        await message.answer(f'Вы уже прошли данный тест на {round(int(present), 1)}%')



async def update_questions(message: types.Message, questions, count_questions, next_questions, img, user_id):
    if count_questions == 200:
        correct_answer = await db.get_correct_answer_users(user_id)

        count_all_questions = await db.get_all_questions()  # Колличество всех вопросов
        un_correct_answer = int(count_all_questions[0]) - int(correct_answer[0])

        result = (int(correct_answer[0]) / int(count_all_questions[0])) * 100

        await db.update_passet_answer('Прошел', user_id)

        await db.update_percent_user(str(result), user_id)

        await message.answer(f'{questions}\n'
                             f'Ваш результат: {round(result, 1)} %')

        user = await db.get_users(user_id)
        wrong_answer = user[0][10]
        wrong_answer_selected = user[0][9]

        data = []
        data_wrong_answer = []
        description = ''

        if wrong_answer != '' and wrong_answer_selected != '':
            data = wrong_answer.split(' ')
            data_wrong_answer = wrong_answer_selected.split(' ')

            for delete_data in data:
                if delete_data == "":
                    data.remove(delete_data)

            for delete_data_wrong_answer in data_wrong_answer:
                if delete_data_wrong_answer == "":
                    data_wrong_answer.remove(delete_data_wrong_answer)

            count = 0
            for k in data:
                for l in range(count, len(data_wrong_answer)):
                    questins_descriptions = await db.get_questions(int(k))
                    description += f'Вопрос {questins_descriptions[0][0]}:' + questins_descriptions[0][3] + "\n" \
                                                                                                            f'Ответил {data_wrong_answer[l]}\n\n'
                    count += 1
                    break

        await send_email(f"Персональные данные пользователя:\n"
                         f"Фамилия - {user[0][2]}\n"
                         f"Имя - {user[0][3]}\n"
                         f"Ресторан {user[0][5]}\n\n"
                         f"Статистика по тесту пользователя {user[0][2]}:\n"
                         f"Всего вопросов {count_all_questions} в тесте\n"
                         f"Прошел тест на {round(result, 1)} %\n"
                         f"Ответил правильно - {user[0][7]}\n\n"
                         f"Статистика по Ошибкам\n"
                         f"Допустил ошибок - {un_correct_answer}\n\n {description}")
    else:
        await bot.edit_message_media(media=InputMediaPhoto(img),
                                     chat_id=message.chat.id,
                                     message_id=message.message_id,
                                     reply_markup=await answer(next_questions))

        await bot.edit_message_caption(chat_id=message.chat.id,
                                       message_id=message.message_id,
                                       caption=f'Вопрос № {next_questions}',
                                       reply_markup=await answer(next_questions))



@dp.callback_query_handler(lambda call: "answer_" in call.data)
async def user_answer(call: types.CallbackQuery):
    current_int_questions = call.data.split("_")[2]  # текущий вопрос
    answer = call.data.split("_")[1]  # выбранный ответ

    next_question = int(current_int_questions) + 1

    current_questions = await db.get_questions(int(current_int_questions))  # выводим текущий вопрос
    next_questions = await db.get_questions(int(next_question))  # выводим следующий вопрос

    count_all_questions = await db.get_all_questions()  # Колличество всех вопросов

    count_questions = int(count_all_questions[0])  # преобразуем в число

    if count_questions >= int(current_int_questions):  # проверяем вопрос
        if answer == current_questions[0][2] or answer == 'L3 (Закрытие ресторана)':  #если пользователь ответил правильно
            correct_answer = await db.get_correct_answer_users(call.from_user.id)
            await db.update_correct_answer(int(correct_answer[0]) + 1, call.from_user.id)
        else:
            current_wrong_answer = await db.get_wrong_answers(call.from_user.id)
            current_wrong_answer_selected = await db.get_wrong_answer_selected(call.from_user.id)

            wrong_answer = ''
            wrong_answer_selected = ''

            if current_wrong_answer[0][0] is None and current_wrong_answer_selected[0][0]  is None:
                b = str(answer).split()
                b = ''.join(b)

                wrong_answer += str(int(current_int_questions))
                wrong_answer_selected += b
            else:
                for i in current_wrong_answer:
                    wrong_answer += i[0] + ' '

                wrong_answer += ' ' + str(int(current_int_questions))

                for j in current_wrong_answer_selected:
                    wrong_answer_selected += j[0] + ' '

                b = str(answer).split()
                b = ''.join(b)

                wrong_answer_selected += ' ' + b

            await db.update_wrong_answer(wrong_answer, call.from_user.id)
            await db.update_wrong_answer_selected(wrong_answer_selected, call.from_user.id)

        if count_questions == int(current_int_questions):
            await update_questions(call.message, 'Вы ответили на вопросы', 200, next_question, current_questions[0][1],
                                   call.from_user.id)
        else:
            await update_questions(call.message, next_questions[0][2],
                                   next_questions[0][0],
                                   next_question,
                                   str(next_questions[0][1]),
                                   call.from_user.id)

    # else:
    #     await update_questions(call.message, 'Вы ответили на вопросы', 200, next_question, current_questions[0][1],
    #                            call.from_user.id)




