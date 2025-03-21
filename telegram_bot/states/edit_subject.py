from aiogram import Router, F, Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from telegram_bot import text_message
from telegram_bot.config_reader import config
from telegram_bot.database_methods.database_request import update_subject, get_subject
from telegram_bot.keyboards import inline_markup


class EditSubjectForm(StatesGroup):
    subject_id = State()
    name = State()
    sticker = State()


router = Router()
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


async def update_edit_data(message: Message, state: FSMContext, subject_id: int | str) -> None:
    subject_data = get_subject(id=subject_id)[0]
    name, sticker = subject_data[1], subject_data[2]
    data = {
        'subject_id': subject_id,
        'name': name,
        'sticker': sticker
    }

    await state.update_data(data)
    await process_edit_subject(message, state, is_edited=False)


# Main editing menu with choose action
async def process_edit_subject(message: Message, state: FSMContext, is_edited: bool = True) -> None:
    try:
        # Take homework data from Homework (StatesGroup)
        data = await state.get_data()

        subject_id, name, sticker = data.values()

        subject_text = text_message.EDIT_SUBJECT.format(sticker=sticker, name=name)
        await message.answer(text=subject_text,
                             reply_markup=inline_markup.get_edit_subject_keyboard(subject_id=subject_id, is_edited=is_edited))

    except KeyError:
        await message.answer(text=text_message.TRY_AGAIN_ERROR,
                             reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


@router.message(EditSubjectForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    try:
        subject_name = message.text
        if len(subject_name) > 20:
            raise ValueError
        await state.update_data(name=subject_name)
    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
    finally:
        await state.set_state(EditSubjectForm.subject_id)
        await process_edit_subject(message, state)


@router.message(EditSubjectForm.sticker)
async def process_sticker(message: Message, state: FSMContext) -> None:
    try:
        subject_sticker = message.text
        if subject_sticker is None or len(subject_sticker) != 1:
            # not integer
            raise TypeError
        await state.update_data(sticker=subject_sticker)
    except TypeError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
    finally:
        await state.set_state(EditSubjectForm.subject_id)
        await process_edit_subject(message, state)


@router.callback_query(F.data == 'edit_name')
async def edit_name(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(text_message.CHOOSE_SUBJECT_NAME)
    await state.set_state(EditSubjectForm.name)


@router.callback_query(F.data == 'edit_sticker')
async def edit_sticker(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(text_message.CHOOSE_SUBJECT_STICKER)
    await state.set_state(EditSubjectForm.sticker)



# Edit homework (create request to database)
@router.callback_query(F.data == 'edit_subject_data')
async def edit_subject_data(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        # Take homework data from Homework (StatesGroup)
        data = await state.get_data()
        update_subject(**data)  # create editing request to database

        # Stop state (editing homework's data)
        await state.clear()
        await callback.message.delete()
        await callback.message.answer(text_message.EDIT_SUBJECT_COMPLETE)

    except KeyError:
        await callback.message.answer(text_message.TRY_AGAIN_ERROR,
                                      reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()
