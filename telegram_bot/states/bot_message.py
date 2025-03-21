import logging

from aiogram import Router, F, Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from telegram_bot import text_message
from telegram_bot.config_reader import config
from telegram_bot.database_methods.database_request import *
from telegram_bot.keyboards import inline_markup


# Form for message data
class MessageForm(StatesGroup):
    text = State()


logger = logging.getLogger('Sender')
router = Router()
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


# Start registering a bot's message
async def register_message(message: Message, state: FSMContext) -> None:
    await message.answer(text=text_message.BOT_MESSAGE_INPUT_TEXT)
    await state.set_state(MessageForm.text)


# Process message text
@router.message(MessageForm.text)
async def process_message_text(message: Message, state: FSMContext) -> None:
    text_to_send = message.text
    await state.update_data(text=text_to_send)
    await message.answer(text=text_message.BOT_MESSAGE_TEXT.format(message=text_to_send),
                         reply_markup=inline_markup.get_send_message_keyboard())



# Send message to all users
@router.callback_query(F.data == 'send_message')
async def send_message(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    class_id = get_admins(telegram_id=callback.message.chat.id)[0][1]

    users_list = get_users(class_id=class_id)
    data = await state.get_data()
    text_to_send = data['text']
    await state.clear()

    for telegram_id in list(map(lambda elem: elem[0], users_list)):
        try:
            await bot.send_message(chat_id=telegram_id, text=text_to_send)
        except Exception as error:
            logger.info(f"Handle {error.__class__.__name__} while sending message to {telegram_id}")

    await callback.message.answer(text=text_message.BOT_MESSAGE_SUCCESS)