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
async def start_ads_from_filter(call:CallbackQuery):
    """Запуск рассылки сразу после настройки фильтра"""
    await Notifications.NotificationsOn.set()
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    await db.change_status(user_id, True)
    await call.message.answer('Рассылка включена. Я отправлю Вам новые объявления как только они появятся.',
                              reply_markup=running_notification_menu)
    status = await db.get_status(user_id)
    user_filter = await db.get_filter(user_id)
    av_by = AvBySearch(await db.get_last_ads_id_list(user_id), user_filter)
    await get_ads_call(status, db, user_id, av_by, user_filter, bot, call, time_interval)


@dp.callback_query_handler(text='resume_noti', state=Notifications.NotificationsOn)
async def cancel_change_filter(call: CallbackQuery):
    """Возобновление рассылки после перезагрузки бота"""
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    await db.change_status(user_id, True)
    await call.message.answer('Рассылка включена. Я отправлю Вам новые объявления как только они появятся.',
                              reply_markup=running_notification_menu)
    status = await db.get_status(user_id)
    user_filter = await db.get_filter(user_id)
    av_by = AvBySearch(await db.get_last_ads_id_list(user_id), user_filter)
    await get_ads_call(status, db, user_id, av_by, user_filter, bot, call, time_interval)

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
async def start_notification(message: types.Message):
    """Нажатие на кнопку Включить рассылку"""
    user_id = message.from_user.id
    await Notifications.NotificationsOn.set()
    await db.change_status(user_id, True)
    await message.answer('Рассылка включена. Я отправлю Вам новые объявления как только они появятся.',
                         reply_markup=running_notification_menu)

    status = await db.get_status(user_id)
    user_filter = await db.get_filter(user_id)
    av_by = AvBySearch(await db.get_last_ads_id_list(user_id), user_filter)
    await get_ads(status, db, user_id, av_by, user_filter, bot, message, time_interval)


@dp.message_handler(Text(endswith='Остановить рассылку'), state=Notifications.NotificationsOn)
async def stop_notification(message: types.Message):
    """Нажатие на кнопку Остановить рассылку"""
    await db.change_status(message.from_user.id, False)
    await message.answer(f'Рассылка остановлена. Возможно в течении 20 секунд Вам придет объявление, '
                         f'которое уже находится в обработке',
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
