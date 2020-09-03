from keyboards.default.menu_keyboards import menu_with_on_notification, menu
from loader import db


async def send_menu_message(message):
    """Проверяем статус рассылки и отправляем нужное меню"""
    status = await db.get_status(message.from_user.id)
    if status:
        await message.answer("Вы в главном меню",
                             reply_markup=menu_with_on_notification)
    else:
        await message.answer("Вы в главном меню",
                             reply_markup=menu)


async def send_menu_callback(call):
    """Проверяем статус рассылки и отправляем нужное меню"""
    status = await db.get_status(call.from_user.id)
    if status:
        await call.message.answer("Вы в главном меню",
                                  reply_markup=menu_with_on_notification)
    else:
        await call.message.answer("Вы в главном меню",
                                  reply_markup=menu)


async def send_menu_start_message(message):
    """Проверяем статус рассылки после кнопки старт"""
    status = await db.get_status(message.from_user.id)
    if status:
        await message.answer(f'Привет, {message.from_user.full_name}! '
                             f'Теперь бот доступен для Вас '
                             f'Если Вам нужна помощь, нажмите на клавиатуре кнопку Помощь/Инструкция или '
                             f'введите команду /help для просмотра доступных команд',
                             reply_markup=menu_with_on_notification)
    else:
        await message.answer(f'Привет, {message.from_user.full_name}! '
                             f'Теперь бот доступен для Вас '
                             f'Если Вам нужна помощь, нажмите на клавиатуре кнопку Помощь/Инструкция или '
                             f'введите команду /help для просмотра доступных команд',
                             reply_markup=menu)


async def send_menu_check_subs_callback(call):
    """Проверяем статус рассылки после проверки подписки"""
    status = await db.get_status(call.from_user.id)
    if status:
        await call.message.answer(f'Привет, {call.from_user.full_name}! '
                                  f'Теперь бот доступен для Вас '
                                  f'Если Вам нужна помощь, нажмите на клавиатуре кнопку Помощь/Инструкция или '
                                  f'введите команду /help для просмотра доступных команд',
                                  reply_markup=menu_with_on_notification)
    else:
        await call.message.answer(f'Привет, {call.from_user.full_name}! '
                                  f'Теперь бот доступен для Вас '
                                  f'Если Вам нужна помощь, нажмите на клавиатуре кнопку Помощь/Инструкция или '
                                  f'введите команду /help для просмотра доступных команд',
                                  reply_markup=menu)


async def send_menu_after_report(message, report_id):
    """Проверяем статус подписки после отправки отчета об ошибке и отправляем нужное меню"""
    status = await db.get_status(message.from_user.id)
    if status:
        await message.answer('Спасибо за Ваше сообщение!\n'
                             f'Номер Вашего отчета: {report_id}\n'
                             'Мы исправим ошибку в ближайшее время',
                             reply_markup=menu_with_on_notification)
    else:
        await message.answer('Спасибо за Ваше сообщение!\n'
                             f'Номер Вашего отчета: {report_id}\n'
                             'Мы исправим ошибку в ближайшее время',
                             reply_markup=menu)


async def send_menu_with_notification(message):
    """Проверяем статус рассылки и отправляем нужное меню после включения """
    status = await db.get_status(message.from_user.id)
    if status:
        await message.answer("Вы в главном меню",
                             reply_markup=menu_with_on_notification)
    else:
        await message.answer("Вы в главном меню",
                             reply_markup=menu)


async def send_menu_admin_callback(call, count):
    status = await db.get_status(call.from_user.id)
    if status:
        await call.message.answer(f'Сообщение отправлено.\n Количество пользователей = {count}',
                             reply_markup=menu_with_on_notification)
    else:
        await call.message.answer(f'Сообщение отправлено.\n Количество пользователей = {count}',
                                  reply_markup=menu)


async def send_menu_admin_message(message, count):
    status = await db.get_status(message.from_user.id)
    if status:
        await message.answer(f'Сообщение отправлено.\n Количество пользователей = {count}',
                             reply_markup=menu_with_on_notification)
    else:
        await message.answer(f'Сообщение отправлено.\n Количество пользователей = {count}',
                                  reply_markup=menu)
