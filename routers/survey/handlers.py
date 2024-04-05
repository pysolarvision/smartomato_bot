from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from .states import Survey

router = Router(name=__name__)
data = []


@router.message(Command('cut'))
async def hande_start_survey(msg: types.Message, state: FSMContext):
    await state.set_state(Survey.cut_top)
    await msg.answer(
        'Сколько нужно обрезать сверху?'
    )


@router.message(Survey.cut_top, F.text)
async def handle_survey_user_cut_top(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer("Пожалуйста, введите только число.")
        return
    await state.update_data(cut_top=msg.text)
    await state.set_state(Survey.cut_bottom)
    await msg.answer(
        f'Сверху будет срезано <b>{msg.text}</b>px. Сколько срезать снизу?',
    )


@router.message(Survey.cut_bottom, F.text)
async def handle_survey_user_cut_bottom(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer("Пожалуйста, введите только число.")
        return
    await state.update_data(cut_bottom=msg.text)
    await msg.answer(
        f'Снизу будет срезано <b>{msg.text}</b>px. Можешь загружать изображения.'
    )




