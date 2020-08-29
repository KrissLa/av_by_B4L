from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from data.config import INSTRUCTION_LINK, SEARCH_LINK
from keyboards.default.menu_keyboards import stopped_notification_menu, menu, back_to_menu_menu
from keyboards.inline.inline_keyboards import cancel_markup, to_filter_from_notifications
from loader import dp, db, bot
from states.menu_states import NewFilters, Notifications, Reports


@dp.message_handler(Text(endswith='Рассылка'))
async def get_notification(message: types.Message):
    """Нажатие на кнопку Рассылка"""
    ads_filter = await db.get_filter(message.from_user.id)
    if ads_filter:
        await message.answer('Вы в разделе Рассылка\n'
                             'Включите рассылку, чтобы начать получать новые объявления',
                             reply_markup=stopped_notification_menu)
        await Notifications.WaitNotificationStatus.set()
    else:
        await message.answer('Сначала Вам нужно установить фильтр!',
                             reply_markup=to_filter_from_notifications)


@dp.callback_query_handler(text='to_filter_from_noti')
async def cancel_change_filter(call: CallbackQuery):
    """Переход к установке фильтра из рассылки"""
    await call.message.edit_reply_markup()
    await call.message.answer(f'Для настройки фильтра выполните следующее:\n'
                              f'1. Зайдите на сайт <a href="{SEARCH_LINK}">av.by</a>\n'
                              f'2. Настройте фильтр на сайте (не забудьте установить сортировку "По дате подачи")\n'
                              f'3. Нажмите кнопку "Показать"\n'
                              f'4. Скопируйте получившуюся ссылку из Вашего браузера\n'
                              f'5. Отправьте ссылку мне\n\n'
                              f'Сейчас у вас не установлен фильтр\n\n',
                              reply_markup=back_to_menu_menu,
                              disable_web_page_preview=True)
    await call.message.answer(f'Подробная инструкция здесь: <a href="{INSTRUCTION_LINK}">ИНСТРУКЦИЯ</a>',
                              reply_markup=cancel_markup,
                              disable_web_page_preview=True)
    await NewFilters.WaitFilter.set()


@dp.callback_query_handler(text='cancel_to_filter')
async def cancel_change_filter(call: CallbackQuery):
    """Отмена изменения фильтра"""
    await call.message.edit_reply_markup()


@dp.message_handler(Text(endswith='Главное меню'))
async def back_to_menu(message: types.Message):
    """Нажатие на кнопку Главное меню"""
    await message.answer('Вы нажали Главное меню',
                         reply_markup=menu)


@dp.message_handler(Text(endswith='Настройка фильтра'))
async def get_settings_filters(message: types.Message):
    """Нажатие на кнопку Настройка фильтра"""
    filter = await db.get_filter(message.from_user.id)
    print(filter)
    if filter:
        str_filter = f'установлен <a href="{filter}" target="_blank">фильтр</a>'
    else:
        str_filter = 'фильтр не установлен.'
    await message.answer(f'Для настройки фильтра выполните следующее:\n'
                         f'1. Зайдите на сайт <a href="{SEARCH_LINK}">av.by</a>\n'
                         f'2. Настройте фильтр на сайте\n'
                         f'3. Нажмите кнопку "Найти объъявления"\n'
                         f'4. Не забудьте установить сортировку "По дате подачи" (на мобильных устройствах - "сначала новые")\n'
                         f'5. Скопируйте получившуюся ссылку из Вашего браузера\n'
                         f'6. Отправьте ссылку мне\n\n'
                         f'Сейчас у вас {str_filter}\n\n',
                         reply_markup=back_to_menu_menu,
                         disable_web_page_preview=True)
    await message.answer(f'Подробная инструкция здесь: <a href="{INSTRUCTION_LINK}">ИНСТРУКЦИЯ</a>',
                         reply_markup=cancel_markup,
                         disable_web_page_preview=True)
    await NewFilters.WaitFilter.set()


@dp.message_handler(Text(endswith='Отмена'))
async def get_cancel(message: types.Message):
    """Нажатие на кнопку Отмена"""
    await message.answer('Вы нажали Отмена',
                         reply_markup=menu)


@dp.message_handler(Text(endswith='Помощь / Инструкция'))
async def get_help_or_instruction(message: types.Message):
    """Инструкция к боту"""
    user_id =message.from_user.id
    await message.answer(f'Для того, чтобы начать получать уведомления о новых объъявлениях Вам '
                         f'необходимо установить фильтр и включить рассылку\n'
                         f'1. Для начала нажмите "Настройка фильтра"')
    await bot.send_photo(chat_id=user_id,
                         photo='https://sun9-35.userapi.com/wnTrPNwWM3Ge8ayRIkc1paLSNAIlTjZmwLG5nA/VW5co-D_H2s.jpg')
    await message.answer(f'2. Следуя инструкции настройте фильтр.')
    await bot.send_photo(chat_id=user_id,
                         photo='https://sun9-63.userapi.com/EmxJqsFJZkwE5H4vMMLRxCqBBE7p2Tp9D6e-OA/01TMXkb79no.jpg')
    await message.answer(f'3. Нажмите кнопку "Включить рассылку"')
    await bot.send_photo(chat_id=user_id,
                         photo='https://sun9-51.userapi.com/s0SF6FdEDVl5kJioXYx_R6AjzI3X9u7HOqr7OA/zgP86Jdkwnw.jpg')
    await message.answer(f'Подробная инструкция здесь: <a href="{INSTRUCTION_LINK}">ИНСТРУКЦИЯ</a>',
                         disable_web_page_preview=True)


@dp.message_handler(Text(endswith='О нас'))
async def get_about_us(message: types.Message):
    await message.answer('Вы нажали О нас')


@dp.message_handler(Text(endswith='Сообщить об ошибке'))
async def get_report_a_bug(message: types.Message):
    await Reports.WaitReport.set()
    await message.answer('Спасибо за Вашу бдительность',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer('Пожалуйста опишите ошибку в одном сообщении',
                         reply_markup=cancel_markup)
