from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from telegram_bot.database_methods.database_request import *
from telegram_bot import text_message


# Form for register admin
class AdminForm(StatesGroup):
    telegram_id = State()
    is_admin = State()


router = Router()


# Start registering an admin
async def register_admins(message: Message, state: FSMContext, is_admin: bool) -> None:
    await message.edit_text(text_message.CHOOSE_ADMIN_ID)
    await state.update_data(is_admin='True') if is_admin else await state.update_data(is_admin='False')
    await state.set_state(AdminForm.telegram_id)


# Process admin's id
@router.message(AdminForm.telegram_id)
async def process_admin(message: Message, state: FSMContext) -> None:
    try:
        telegram_id = message.text
        # Checking conditions for telegram_id
        if not telegram_id.isalnum() or 10 < len(telegram_id) < 6 or telegram_id == str(message.chat.id):
            raise ValueError

        await state.update_data(telegram_id=telegram_id)
        data = await state.get_data()

        telegram_id, is_admin = data['telegram_id'], data['is_admin']
        change_admin(telegram_id, is_admin)

        await message.answer(text_message.EDIT_ADMINS.format(telegram_id))
    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST)
    await state.clear()
