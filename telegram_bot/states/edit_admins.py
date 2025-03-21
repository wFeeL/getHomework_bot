from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from telegram_bot.database_methods.database_request import add_admin, get_class, get_admins
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
        is_super_admin = False
        try:
            is_super_admin = get_admins(telegram_id=telegram_id)[0][3]
        except IndexError:
            pass

        if not telegram_id.isdigit() or len(telegram_id) > 10 or len(telegram_id) < 6:
            raise ValueError

        await state.update_data(telegram_id=telegram_id)
        admins_data = await state.get_data()
        print(admins_data, admins_data.values())
        is_admin, telegram_id = admins_data.values()
        if is_admin:
            await state.set_state(AdminForm.class_id)
            await message.answer(text_message.CHOOSE_CLASS, reply_markup=reply_markup.get_class_keyboard())
        else:
            add_admin(telegram_id, value=False, super_admin=is_super_admin)
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
        is_super_admin = False
        try:
            is_super_admin = get_admins(telegram_id=telegram_id)[0][3]
        except IndexError:
            pass
        add_admin(telegram_id=telegram_id, value=True, super_admin=is_super_admin, class_id=class_id)

        await message.answer(text_message.EDIT_ADMINS.format(telegram_id), reply_markup=ReplyKeyboardRemove())

    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
    await state.clear()
