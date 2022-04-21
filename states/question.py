from aiogram.dispatcher.filters.state import StatesGroup, State


class questions(StatesGroup):
    photo = State()
    answer = State()
