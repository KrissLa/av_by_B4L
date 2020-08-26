from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from data.config import INSTRUCTION_LINK
from keyboards.default.menu_keyboards import stopped_notification_menu, running_notification_menu, menu, cancel_menu, \
    back_to_menu_menu
from keyboards.inline.inline_keyboards import cancel_markup, to_filter_from_notifications
from loader import dp, db
from states.menu_states import NewFilters, Notifications





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
                              f'1. Зайдите на сайт https://cars.av.by/\n'
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
                         f'1. Зайдите на сайт https://cars.av.by/\n'
                         f'2. Настройте фильтр на сайте (не забудьте установить сортировку "По дате подачи")\n'
                         f'3. Нажмите кнопку "Показать"\n'
                         f'4. Скопируйте получившуюся ссылку из Вашего браузера\n'
                         f'5. Отправьте ссылку мне\n\n'
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
    await message.answer('Вы нажали Помощь / Инструкция')


@dp.message_handler(Text(endswith='О нас'))
async def get_about_us(message: types.Message):
    await message.answer('Вы нажали О нас')


@dp.message_handler(Text(endswith='Сообщить об ошибке'))
async def get_report_a_bug(message: types.Message):
    await message.answer('Вы нажали Сообщить об ошибке')
