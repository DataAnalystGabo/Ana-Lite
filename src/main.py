import os
import sys
import env
import asyncio
import logging
from backend_sql import querySQL
from aiogram import Bot, Dispatcher,types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


os.environ['TELEGRAM_API_KEY'] = env.TELEGRAM_API_KEY
dp = Dispatcher()
bot = Bot(env.TELEGRAM_API_KEY , parse_mode=ParseMode.HTML)

#----------------------------------------------------------------
#                      Función de incio
#----------------------------------------------------------------
async def main() -> None:
    await dp.start_polling(bot)
#----------------------------------------------------------------
#----------------------------------------------------------------


#----------------------------------------------------------------
#                      Command Start
#----------------------------------------------------------------
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f'¡Ey! {hbold(message.from_user.full_name)}, dime que consulta deseas hacer 😊. Abajo te dejo las opciones:', reply_markup=keyboard)
#----------------------------------------------------------------
#----------------------------------------------------------------


#----------------------------------------------------------------
#                      Definiendo botones
#----------------------------------------------------------------
keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Todos los permisos sobre una dirección exacta', callback_data='all_permissions')]
])

#Declarando estados para capturar respuestas.
class Form(StatesGroup):
    waiting_for_address = State()
#----------------------------------------------------------------
#----------------------------------------------------------------


#----------------------------------------------------------------
#                  HANDLE_ALL_PERMISSIONS
#----------------------------------------------------------------
@dp.callback_query(lambda c: c.data == 'all_permissions')
async def process_callback_button(callback_query: types.CallbackQuery, state: FSMContext):

    await state.set_state(Form.waiting_for_address)

    await bot.send_message(callback_query.from_user.id, f'Dame la dirección que deseas buscar. {hbold('Recuerda que debe ser exacta.')} Ejemplo: AV. RIVADAVIA 3210')


@dp.message(Form.waiting_for_address)
async def process_user_message(message: types.Message, state: FSMContext):
    user_response = message.text

    #IDA
    sql_response = await querySQL(user_response)

    #VUELTA
    await message.answer(sql_response)

    await state.clear()
#----------------------------------------------------------------
#----------------------------------------------------------------





#----------------------------------------------------------------
#                      Función __main__
#----------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
#----------------------------------------------------------------
#----------------------------------------------------------------























