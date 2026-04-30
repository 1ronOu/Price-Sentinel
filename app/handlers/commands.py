from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.cruds import user_crud

class Registration(StatesGroup):
    waiting_for_name = State()


router = Router(name='commands-router')


@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(text='Hello! Enter your name, which is listed on the website:')
    await state.set_state(Registration.waiting_for_name)