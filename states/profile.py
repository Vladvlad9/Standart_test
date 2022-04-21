from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileSG(StatesGroup):
    first_name = State()
    last_name = State()
    midle_name = State()
    restaraunt = State()
