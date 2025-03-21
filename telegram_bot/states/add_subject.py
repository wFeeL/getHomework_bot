from aiogram import Router, F, Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from telegram_bot import text_message
from telegram_bot.config_reader import config
from telegram_bot.database_methods.database_request import *
from telegram_bot.keyboards import inline_markup, reply_markup


class SubjectForm(StatesGroup):
    name = State()
    sticker = State()


router = Router()
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


async def register_subject(message: Message, state: FSMContext) -> None:
    await message.answer(text=text_message.CHOOSE_SUBJECT_NAME)
    await state.set_state(SubjectForm.name)


@router.message(SubjectForm.name)
async def process_subject_name(message: Message, state: FSMContext) -> None:
    subject_name = message.text
    try:
        await state.update_data(name=subject_name)
        await message.answer(text=text_message.CHOOSE_SUBJECT_STICKER)
        await state.set_state(SubjectForm.sticker)

    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


@router.message(SubjectForm.sticker)
async def process_subject_sticker(message: Message, state: FSMContext) -> None:
    subject_sticker = message.text
    try:
        await state.update_data(sticker=subject_sticker)
        await send_subject(message, state)

    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()

async def send_subject(message: Message, state: FSMContext) -> None:
    try:
        subject_data = await state.get_data()
        name, sticker = subject_data.values()

        subject_text = text_message.SUBJECT_DATA_TO_SEND.format(sticker=sticker, name=name)
        markup = inline_markup.get_send_subject_keyboard()
        await message.answer(text=subject_text, reply_markup=markup)

    except KeyError:
        await message.answer(text_message.TRY_AGAIN_ERROR,
                             reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()

@router.callback_query(F.data == 'send_subject_data')
async def send_data(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        subject_data = await state.get_data()
        name, sticker = subject_data.values()
        class_id = get_admins(telegram_id=callback.message.chat.id)[0][4]
        add_subject_value(name, sticker, class_id)

        await callback.message.answer(text_message.ADDING_SUBJECT_COMPLETE.format(sticker=sticker, name=name))
        await callback.message.delete()
        await state.clear()

    except KeyError:
        await callback.message.answer(text_message.INCORRECT_REQUEST,
                                      reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()

@router.callback_query(F.data == 'cancel_send_data')
async def cancel_send_data(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text_message.CANCEL_ACTION, reply_markup=inline_markup.get_admin_menu())


