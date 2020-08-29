from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from keyboards.default.menu_keyboards import stopped_notification_menu, running_notification_menu, menu
from loader import dp, db, bot
from states.menu_states import Notifications
from utils.noti import get_ads, get_ads_call
from utils.parsers.av_by import AvBySearch

time_interval = 15


@dp.callback_query_handler(text='start_ads_from_filter')
async def start_ads_from_filter(call:CallbackQuery, state:FSMContext):
    """Запуск рассылки сразу после настройки фильтра"""
    await Notifications.NotificationsOn.set()
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    await db.change_status(user_id, True)
    await call.message.answer('Рассылка включена. Я отправлю Вам новые объявления как только они появятся.',
                              reply_markup=running_notification_menu)
    state_name = await state.get_state()
    user_filter = await db.get_filter(user_id)
    av_by = AvBySearch(await db.get_last_ads_id_list(user_id), user_filter)
    await get_ads_call(state_name, db, user_id, av_by, user_filter, bot, call, time_interval, state)


@dp.callback_query_handler(text='resume_noti', state=Notifications.NotificationsOn)
async def cancel_change_filter(call: CallbackQuery, state: FSMContext):
    """Возобновление рассылки после перезагрузки бота"""
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    await db.change_status(user_id, True)
    await call.message.answer('Рассылка включена. Я отправлю Вам новые объявления как только они появятся.',
                              reply_markup=running_notification_menu)
    state_name = await state.get_state()
    user_filter = await db.get_filter(user_id)
    av_by = AvBySearch(await db.get_last_ads_id_list(user_id), user_filter)
    await get_ads_call(state_name, db, user_id, av_by, user_filter, bot, call, time_interval, state)

@dp.callback_query_handler(text='stop_noti', state=Notifications.NotificationsOn)
async def cancel_change_filter(call: CallbackQuery, state: FSMContext):
    """Возобновление рассылки после перезагрузки бота"""
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    await db.change_status(user_id, False)
    await call.message.answer('Рассылка остановлена. Вы в главном меню',
                              reply_markup=menu)
    await state.finish()


@dp.message_handler(Text(endswith='Включить рассылку'), state=Notifications.WaitNotificationStatus)
async def start_notification(message: types.Message, state: FSMContext):
    """Нажатие на кнопку Включить рассылку"""
    user_id = message.from_user.id
    await Notifications.NotificationsOn.set()
    await db.change_status(user_id, True)
    await message.answer('Рассылка включена. Я отправлю Вам новые объявления как только они появятся.',
                         reply_markup=running_notification_menu)

    print(await state.get_state())
    state_name = await state.get_state()
    user_filter = await db.get_filter(user_id)
    av_by = AvBySearch(await db.get_last_ads_id_list(user_id), user_filter)
    await get_ads(state_name, db, user_id, av_by, user_filter, bot, message, time_interval, state)


@dp.message_handler(Text(endswith='Остановить рассылку'), state=Notifications.NotificationsOn)
async def stop_notification(message: types.Message):
    """Нажатие на кнопку Остановить рассылку"""
    await db.change_status(message.from_user.id, False)
    await message.answer(f'Рассылка будет остановлена в течении {time_interval} секунд',
                         reply_markup=stopped_notification_menu)
    await Notifications.WaitNotificationStatus.set()


@dp.message_handler(Text(endswith='Главное меню'),
                    state=Notifications.WaitNotificationStatus)
async def back_to_menu(message: types.Message, state: FSMContext):
    """Нажатие на кнопку Главное меню"""
    await message.answer('Вы нажали Главное меню',
                         reply_markup=menu)
    await state.finish()

# Закинуть user_id  в state и попробовать запустить отдельную функцию по кругу
