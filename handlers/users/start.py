from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from filters.user_filters import IsMemberMessage, IsMemberCallback
from keyboards.default.menu_keyboards import menu
from loader import dp, db
from utils.send_menu import send_menu_start_message, send_menu_check_subs_callback, send_menu_message


@dp.message_handler(CommandStart(), IsMemberMessage())
async def bot_start(message: types.Message):
    await db.add_user(user_id=message.from_user.id, name=message.from_user.full_name, status=False,
                      filter=None, ads_id_1=None, ads_id_2=None, ads_id_3=None, ads_id_4=None,
                      ads_id_5=None)
    await send_menu_start_message(message)


@dp.callback_query_handler(IsMemberCallback(), text='check_subs')
async def check_subscriptions(call: types.CallbackQuery):
    """Проверяем подписку"""
    await call.message.edit_reply_markup()
    await db.add_user(user_id=call.from_user.id, name=call.from_user.full_name, status=False,
                      filter=None, ads_id_1=None, ads_id_2=None, ads_id_3=None, ads_id_4=None,
                      ads_id_5=None)
    await send_menu_check_subs_callback(call)


@dp.message_handler(IsMemberMessage(), commands=['menu'], state="*")
async def get_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await send_menu_message(message)


@dp.message_handler(IsMemberMessage(), commands=['restart'], state="*")
async def restart(message: types.Message, state: FSMContext):
    """Restart"""
    await state.finish()
    await db.change_status(message.from_user.id, False)
    await message.answer("Перезагружен\nРассылка остановлена\nФильтр не сброшен",
                         reply_markup=menu)


@dp.message_handler(commands=['reset_filter'], state="*")
async def restart(message: types.Message, state: FSMContext):
    """Restart"""
    await state.finish()
    await db.change_status(message.from_user.id, False)
    await db.reset_filter(message.from_user.id)
    await message.answer("Фильтр сброшен.",
                         reply_markup=menu)