from aiogram import Router, F, Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from telegram_bot import text_message
from telegram_bot.config_reader import config
from telegram_bot.database_methods.database_request import *
from telegram_bot.keyboards import inline_markup, reply_markup


class TeacherForm(StatesGroup):
    name = State()
    surname = State()
    sticker = State()
    patronymic = State()
    subject = State()


router = Router()
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


async def register_teacher(message: Message, state: FSMContext) -> None:
    await message.answer(text=text_message.CHOOSE_TEACHER_NAME)
    await state.set_state(TeacherForm.name)


@router.message(TeacherForm.name)
async def process_teacher_name(message: Message, state: FSMContext) -> None:
    teacher_name = message.text
    try:
        await state.update_data(name=teacher_name)
        await message.answer(text=text_message.CHOOSE_TEACHER_SURNAME)
        await state.set_state(TeacherForm.surname)

    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


@router.message(TeacherForm.surname)
async def process_teacher_surname(message: Message, state: FSMContext) -> None:
    teacher_surname = message.text
    try:
        await state.update_data(surname=teacher_surname)
        await message.answer(text=text_message.CHOOSE_TEACHER_PATRONYMIC)
        await state.set_state(TeacherForm.patronymic)

    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


@router.message(TeacherForm.patronymic)
async def process_teacher_patronymic(message: Message, state: FSMContext) -> None:
    teacher_patronymic = message.text
    class_id = get_users(telegram_id=message.chat.id)[0][1]
    try:

        await state.update_data(patronymic=teacher_patronymic)
        await message.answer(text=text_message.CHOOSE_SUBJECT,
                             reply_markup=reply_markup.get_subjects_keyboard(class_id))
        await state.set_state(TeacherForm.subject)

    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


@router.message(TeacherForm.subject)
async def process_teacher_subject(message: Message, state: FSMContext) -> None:
    teacher_subject = message.text
    try:
        await state.update_data(subject=teacher_subject)
        await send_teacher(message, state)

    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()

async def send_teacher(message: Message, state: FSMContext) -> None:
    try:
        teacher_data = await state.get_data()
        teacher_name, surname, patronymic, subject_name = teacher_data.values()
        print(teacher_data)
        class_id = get_users(telegram_id=message.chat.id)[0][1]
        subject_sticker = get_subject(class_ids=class_id)[0][2]
        teacher_text = text_message.TEACHER_DATA_TO_SEND.format(
            teacher_name=teacher_name, surname=surname, patronymic=patronymic, subject_sticker=subject_sticker,
            subject_name=subject_name)
        markup = inline_markup.get_send_teacher_keyboard()
        await message.answer(text=teacher_text, reply_markup=markup)

    except KeyError:
        await message.answer(text_message.TRY_AGAIN_ERROR,
                             reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()

@router.callback_query(F.data == 'send_teacher_data')
async def send_data(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        teacher_data = await state.get_data()
        # surname have been not needed
        teacher_name, surname, patronymic, subject_name = teacher_data.values()
        class_id = get_admins(telegram_id=callback.message.chat.id)[0][4]
        subject_id = get_subject(name=subject_name, class_ids=class_id)[0][0]
        # fullname = surname + teacher_name + patronymic
        fullname = f'{teacher_name} {patronymic}'
        add_teacher_value(fullname, subject_id, class_id)

        await callback.message.answer(text_message.ADDING_TEACHER_COMPLETE.format(
            teacher_name=teacher_name, patronymic=patronymic, subject_name=subject_name)
        )
        await callback.message.delete()
        await state.clear()

    except KeyError:
        await callback.message.answer(text_message.INCORRECT_REQUEST,
                                      reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()
