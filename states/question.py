from aiogram.dispatcher.filters.state import StatesGroup, State


class questions(StatesGroup):
    name_questions = State()
    photo = State()
    answer = State()
