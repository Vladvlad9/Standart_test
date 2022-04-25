from aiogram.dispatcher.filters.state import StatesGroup, State


class Edit_Question(StatesGroup):
    id = State()
    img = State()
