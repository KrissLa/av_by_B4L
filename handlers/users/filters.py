from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from filters.user_filters import IsMemberCallback
from keyboards.inline.inline_keyboards import start_ads_from_filters
from loader import dp, db
from states.menu_states import NewFilters
from utils.parsers.av_by import get_last_auto_from_av
from utils.send_menu import send_menu_callback, send_menu_message


@dp.callback_query_handler(text='cancel_filter_change', state=NewFilters.WaitFilter)
async def cancel_change_filter(call: CallbackQuery, state: FSMContext):
    """Отмена изменения фильтра"""
    await call.message.edit_reply_markup()
    await send_menu_callback(call)
    await state.finish()



@dp.message_handler(Text(endswith='Главное меню'), state=NewFilters.WaitFilter)
async def get_cancel(message: types.Message, state: FSMContext):
    """Нажатие на кнопку Главное меню"""
    await send_menu_message(message)
    await state.finish()


@dp.message_handler(state=NewFilters.WaitFilter)
async def set_filter(message: types.Message, state: FSMContext):
    """Получаем ссылку"""
    link = message.text
    print(len(link))
    try:
        last_auto_list = get_last_auto_from_av(link)
        print("Пробую")
        print(last_auto_list)
        await db.change_filter(user_id=message.from_user.id, filter_value=str(link))
        print("Готово")
        await db.set_ads_ids(user_id=message.from_user.id, ads_id_1=last_auto_list[0], ads_id_2=last_auto_list[1],
                             ads_id_3=last_auto_list[2],
                             ads_id_4=last_auto_list[3], ads_id_5=last_auto_list[4])
        await send_menu_message(message)
        await message.answer(f"Фильтр установлен!", reply_markup=start_ads_from_filters)
        await state.finish()
    except:
        await message.answer(f'С Вашей ссылкой что-то не так. Пожалуйста проверьте все еще раз и повторите попытку')
