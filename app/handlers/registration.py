from aiogram import Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import user_crud


class Registration(StatesGroup):
    waiting_for_name = State()


router = Router(name='commands-router')

@router.message(Registration.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext, session: AsyncSession):
    user_name = message.text
    chat_id = message.chat.id
    await message.answer(text=f'Looking for name {user_name} in data base...')
    user = await user_crud.get_user_by_user_name(user_name=user_name, db=session)
    if user:
        if user.telegram_id == 0:
            await user_crud.update_user(chat_id=chat_id, user=user, db=session)
            await message.answer(text='Telegram and Price Sentinel connected successfully.')
        else:
            await message.answer(text='This user is already connected to Price Sentinel bot.')
        await state.clear()
    else:
        await message.answer(text=f'User with name {user_name} not found. Please Try again.')
    
    