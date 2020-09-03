from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import admins
from keyboards.default.menu_keyboards import menu
from keyboards.inline.callback_datas import report_data
from loader import dp, db, bot
from states.menu_states import Reports
from utils.send_menu import send_menu_after_report, send_menu_callback


@dp.callback_query_handler(text='cancel_filter_change', state=Reports.WaitReport)
async def cancel_report(call: types.CallbackQuery, state: FSMContext):
    """Отмена отправки репорта"""
    await call.answer("Отмена")
    await call.message.edit_reply_markup()
    await send_menu_callback(call)
    await state.finish()


@dp.message_handler(state=Reports.WaitReport)
async def send_report(message: types.Message, state: FSMContext):
    """Отправка отчета об ошибке"""
    report = message.text
    await db.add_report(user_id=message.from_user.id, name=message.from_user.full_name, status_report=False,
                        report=report)
    report_id = await db.sellect_last_report_id()
    for user in admins:
        await bot.send_message(chat_id=user, text=f"Новое сообщение об ошибке!\n\nid репорта: {report_id}\n{report}",
                               reply_markup=InlineKeyboardMarkup(row_width=2,
                                                                 inline_keyboard=[
                                                                     [
                                                                         InlineKeyboardButton(
                                                                             text='Отметить как исправленный',
                                                                             callback_data=report_data.new(
                                                                                 report_id=report_id,
                                                                                 user_id=message.from_user.id)
                                                                         )
                                                                     ]
                                                                 ]))
    await send_menu_after_report(message, report_id)
    await state.finish()
