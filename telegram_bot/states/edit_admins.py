from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from telegram_bot.database_methods.database_request import change_admin, get_class
from telegram_bot.keyboards import reply_markup, inline_markup
from telegram_bot import text_message


# Form for register admin
class AdminForm(StatesGroup):
    telegram_id = State()
    class_id = State()
    is_admin = State()


router = Router()


# Start registering an admin
async def edit_admins(message: Message, state: FSMContext, is_admin: bool) -> None:
    await message.edit_text(text_message.CHOOSE_ADMIN_ID)
    await state.update_data(is_admin=True) if is_admin else await state.update_data(is_admin=False)
    await state.set_state(AdminForm.telegram_id)


# Process admin's telegram id
@router.message(AdminForm.telegram_id)
async def process_telegram_id(message: Message, state: FSMContext) -> None:
    try:
        telegram_id = message.text
        # Checking conditions for telegram_id
        if not telegram_id.isalnum() or 10 < len(telegram_id) < 6 or telegram_id == str(message.chat.id):
            raise ValueError

        await state.update_data(telegram_id=telegram_id)
        data = await state.get_data()

        telegram_id, is_admin = data['telegram_id'], data['is_admin']
        if is_admin:
            await state.set_state(AdminForm.class_id)
            await message.answer(text_message.CHOOSE_CLASS, reply_markup=reply_markup.get_class_keyboard())
        else:
            change_admin(telegram_id, value=False)
            await message.answer(text_message.EDIT_ADMINS)
            await state.clear()

    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


# Process class id
@router.message(AdminForm.class_id)
async def process_class_id(message: Message, state: FSMContext) -> None:
    try:
        class_name = message.text.split(' ')
        class_id = get_class(letter=class_name[1], number=class_name[0])[0][0]

        data = await state.get_data()

        telegram_id = data['telegram_id']
        change_admin(telegram_id=telegram_id, class_id=class_id, value=True)

        await message.answer(text_message.EDIT_ADMINS.format(telegram_id), reply_markup=ReplyKeyboardRemove())

    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
    await state.clear()
