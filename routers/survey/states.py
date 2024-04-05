from aiogram.fsm.state import StatesGroup, State


class Survey(StatesGroup):
    cut_top = State()
    cut_bottom = State()