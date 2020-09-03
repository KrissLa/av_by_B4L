from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from filters.user_filters import IsMemberCallback, IsMemberMessage
from keyboards.default.menu_keyboards import menu, \
    menu_with_on_notification
from keyboards.inline.inline_keyboards import to_filter_from_notifications
from loader import dp, db


@dp.callback_query_handler(text='start_ads_from_filter')
async def start_ads_from_filter(call:CallbackQuery):
    """Запуск рассылки сразу после настройки фильтра"""
    await call.message.edit_reply_markup()
    await db.change_status(call.from_user.id, True)
    await call.message.answer('Рассылка включена. Я отправлю Вам новые объявления как только они появятся.',
                              reply_markup=menu_with_on_notification)


@dp.message_handler(IsMemberMessage(), Text(endswith='Включить рассылку'))
async def get_notification(message: types.Message):
    """Нажатие на кнопку Рассылка"""
    ads_filter = await db.get_filter(message.from_user.id)
    if ads_filter:
        await db.change_status(message.from_user.id, True)
        await message.answer('Рассылка включена. Я отправлю Вам новые объявления как только они появятся.',
                             reply_markup=menu_with_on_notification)
    else:
        await message.answer('Сначала Вам нужно установить фильтр!',
                             reply_markup=to_filter_from_notifications)


@dp.message_handler(Text(endswith='Остановить рассылку'))
async def stop_notification(message: types.Message):
    """Нажатие на кнопку Остановить рассылку"""
    await db.change_status(message.from_user.id, False)
    await message.answer(f'Рассылка остановлена. Возможно Вам придут объявления, '
                         f'которые уже находится в обработке',
                         reply_markup=menu)


# @dp.callback_query_handler(text='resume_noti', state='*')
# async def cancel_change_filter(call: CallbackQuery):
#     """Возобновление рассылки после перезагрузки бота"""
#     await Notifications.NotificationsOn.set()
#     await call.message.edit_reply_markup()
#     user_id = call.from_user.id
#     print(user_id)
#     await db.change_status(user_id, True)
#     await call.message.answer('Рассылка включена. Я отправлю Вам новые объявления как только они появятся.',
#                               reply_markup=running_notification_menu)
#     # status = await db.get_status(user_id)
#     # print(status)
#     # user_filter = await db.get_filter(user_id)
#     # print(user_filter)
#     # av_by = AvBySearch(await db.get_last_ads_id_list(user_id), user_filter)
#     # print(f'Приступаю к поиску {user_id}')
#     # await get_ads_call(status, db, user_id, av_by, user_filter, bot, call, time_interval)

# @dp.callback_query_handler(text='stop_noti', state='*')
# async def cancel_change_filter(call: CallbackQuery, state: FSMContext):
#     """Возобновление рассылки после перезагрузки бота"""
#     await call.message.edit_reply_markup()
#     user_id = call.from_user.id
#     await db.change_status(user_id, False)
#     await call.message.answer('Рассылка остановлена. Вы в главном меню',
#                               reply_markup=menu)
#     await state.finish()


# @dp.message_handler(Text(endswith='Включить рассылку'), state=Notifications.WaitNotificationStatus)
# async def start_notification(message: types.Message):
#     """Нажатие на кнопку Включить рассылку"""
#     user_id = message.from_user.id
#     await Notifications.NotificationsOn.set()
#     await db.change_status(user_id, True)
#     await message.answer('Рассылка включена. Я отправлю Вам новые объявления как только они появятся.',
#                          reply_markup=running_notification_menu)

    # status = await db.get_status(user_id)
    # user_filter = await db.get_filter(user_id)
    # av_by = AvBySearch(await db.get_last_ads_id_list(user_id), user_filter)
    # await get_ads(status, db, user_id, av_by, user_filter, bot, message, time_interval)


#
#
#
# @dp.message_handler(Text(endswith='Главное меню'),
#                     state=Notifications.WaitNotificationStatus)
# async def back_to_menu(message: types.Message, state: FSMContext):
#     """Нажатие на кнопку Главное меню"""
#     await message.answer('Вы нажали Главное меню',
#                          reply_markup=menu)
#     await state.finish()

# Закинуть user_id  в state и попробовать запустить отдельную функцию по кругу
