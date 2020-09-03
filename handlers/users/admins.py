from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentTypes

from filters.user_filters import IsAdminMessage, IsAdminCallback
from keyboards.default.menu_keyboards import menu, back_to_menu_menu, cancel_menu
from keyboards.inline.callback_datas import report_data, feedback_data
from keyboards.inline.inline_keyboards import admin_menu, set_message_type_keyboard, confirm_message_photo, \
    set_recipients_markup
from loader import dp, db, bot
from states.admin_states import Admin
from utils.send_menu import send_menu_message, send_menu_admin_message, send_menu_admin_callback


@dp.message_handler(Text(endswith='Отмена'), state='*')
async def get_cancel(message: types.Message, state: FSMContext):
    """Нажатие на кнопку Отмена"""
    await state.finish()
    await message.answer('Вы нажали Отмена',
                         reply_markup=menu)


@dp.message_handler(IsAdminMessage(), commands=['admin'], state='*')
async def get_admin_panel(message: types.Message):
    """Вход в админ панель"""
    await message.answer('Просто отправляю меню',
                         reply_markup=back_to_menu_menu)
    await message.answer("Вы в админке",
                         reply_markup=admin_menu)
    await Admin.AdminMenu.set()


@dp.message_handler(Text(endswith='Главное меню'), state=Admin.AdminMenu)
async def back_to_menu(message: types.Message, state: FSMContext):
    """Нажатие на кнопку Главное меню"""
    await send_menu_message(message)
    await state.finish()


# @dp.callback_query_handler(text='bot_was_restarted', user_id=admins, state=Admin.AdminMenu)
# async def bot_was_restarted(call:types.CallbackQuery, state: FSMContext):
#     """Отправка уведомления о перезагрузке бота"""
#     users_list = await db.select_all_user_id_with_status_1()
#     users_list_0 = await db.select_all_user_id_with_status_0()
#     for user in users_list:
#         await bot.send_message(chat_id=user, text='По техническим причинам бот был перезагружен. '
#                                                   'Приносим извинения за неудобства.',
#                                reply_markup=ReplyKeyboardRemove())
#         await bot.send_message(chat_id=user, text="Для возобновления рассылки, пожалуйста, нажмите кнопку.",
#                                reply_markup=resume_notifications)
#     for user in users_list_0:
#         await bot.send_message(chat_id=user, text='По техническим причинам бот был перезагружен. '
#                                                   'Приносим извинения за неудобства.',
#                                reply_markup=menu)
#         state = dp.current_state()
#         await state.set_state()
#     await call.answer('Сообщения отправлены')


@dp.callback_query_handler(text='count_all_users', state=Admin.AdminMenu)
async def get_count_all_users(call: types.CallbackQuery):
    """Получение количества всех пользователей зарегистрированных в боте"""
    count_users = await db.count_users()
    await call.message.answer(f"Количество всех пользователей: {count_users}")


@dp.callback_query_handler(text='count_users_with_status_1', state=Admin.AdminMenu)
async def get_count_users_with_status_1(call: types.CallbackQuery):
    """Получение количества всех пользователей с включенной рассылкой"""
    count_users = await db.count_users_with_status_1()
    await call.message.answer(f"Количество пользователей, у которых включена рассылка: {count_users}")


@dp.callback_query_handler(text='select_all_reports_with_status_0', state=Admin.AdminMenu)
async def get_reports_with_status_0(call: types.CallbackQuery):
    """Получение всех репортов"""
    all_reports = await db.select_all_reports_with_status(status_report=False)

    for report in all_reports:
        print(report['id'])
        await call.message.answer(f"id отчета: {report['id']}\n"
                                  f"Дата: {report['date']}\n"
                                  f"Пользователь: {report['name']}\n"
                                  f"id Пользователя: {report['user_id']}\n"
                                  f"{report['report']}\n",
                                  reply_markup=InlineKeyboardMarkup(row_width=2,
                                                                    inline_keyboard=[
                                                                        [
                                                                            InlineKeyboardButton(
                                                                                text='Отметить как исправленный',
                                                                                callback_data=report_data.new(
                                                                                    report_id=report['id'],
                                                                                    user_id=report['user_id'])
                                                                            )
                                                                        ]
                                                                    ]))


@dp.callback_query_handler(report_data.filter(), state='*')
async def set_report_status_1(call: types.CallbackQuery, callback_data: dict):
    """Отметить отчет как испраленный"""
    report_id = callback_data.get('report_id')
    user_id = callback_data.get('user_id')
    print(report_id)
    await db.change_status_report(status_report=True, id=report_id)
    await call.message.answer('Отчет отмечен как испраленный. Отправим ответ пользователю?',
                              reply_markup=InlineKeyboardMarkup(row_width=2,
                                                                inline_keyboard=[
                                                                    [
                                                                        InlineKeyboardButton(
                                                                            text='Да',
                                                                            callback_data=feedback_data.new(
                                                                                report_id=report_id, user_id=user_id)
                                                                        ),
                                                                        InlineKeyboardButton(
                                                                            text='Нет',
                                                                            callback_data='send_feedback_false'
                                                                        )
                                                                    ]

                                                                ]))
    await call.message.edit_reply_markup()


@dp.callback_query_handler(feedback_data.filter(), state='*')
async def send_feedback_true(call: types.CallbackQuery, callback_data: dict):
    """Отправка сообщения пользователю об исправлении ошибки"""
    report_id = callback_data.get('report_id')
    user_id = callback_data.get('user_id')
    await bot.send_message(chat_id=user_id,
                           text=f'Исправлена ошибка, о которой Вы сообщили в отчете номер {report_id}\n'
                                f'Благодарим Вас)')
    await call.answer('Сообщение отправлено')
    await call.message.edit_reply_markup()


@dp.callback_query_handler(text='send_feedback_false', state='*')
async def send_feedback_false(call: types.CallbackQuery):
    """Не отправлять отчет пользователю"""
    await call.answer('ок')
    await call.message.edit_reply_markup()


@dp.callback_query_handler(text='mailing', state=Admin.AdminMenu)
async def mailing(call: types.CallbackQuery):
    """Раздел рассылки"""
    await call.message.answer('Отправляю кнопку отмены',
                              reply_markup=cancel_menu)
    await call.message.answer('Что будем отправлять?',
                              reply_markup=set_message_type_keyboard)
    await Admin.AdminMessageType.set()


@dp.callback_query_handler(text='message_type_photo', state=Admin.AdminMessageType)
async def set_admin_message_photo(call: types.CallbackQuery):
    """Предлагаем админу загрузить фото"""
    await call.message.answer('Пожалуйста, загрузите фотографию')
    await Admin.AdminMessagePhoto.set()


@dp.message_handler(state=Admin.AdminMessagePhoto, content_types=ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    """Получаем и сохраняем фото в стейт"""
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    await message.answer('Отлично. Теперь подпись к фото.')
    await Admin.AdminMessagePhotoCaption.set()


@dp.message_handler(state=Admin.AdminMessagePhotoCaption)
async def get_captions(message: types.Message, state: FSMContext):
    """Получааем подпись к фото"""
    caption = message.text
    await state.update_data(caption=caption)
    data = await state.get_data()
    photo_id = data.get('photo_id')
    await bot.send_photo(chat_id=message.from_user.id, photo=photo_id,
                         caption=f'{caption}')
    await message.answer('Вот так это будет выглядеть:',
                         reply_markup=confirm_message_photo)
    await Admin.AdminMessagePhotoConfirmation.set()


@dp.callback_query_handler(state=Admin.AdminMessagePhotoConfirmation, text='new_message_photo')
async def new_message_photo(call: types.CallbackQuery, state: FSMContext):
    """Вернуться к началу загрузки фото"""
    await call.message.edit_reply_markup()
    await call.message.answer('Начинаем сначала\n'
                              'Пожалуйста, загрузите фотографию')

    await state.finish()
    await Admin.AdminMessagePhoto.set()


@dp.callback_query_handler(state=Admin.AdminMessagePhotoConfirmation, text='send_photo_next')
async def set_recipients(call: types.CallbackQuery):
    """Выбираем получателей"""
    await call.message.edit_reply_markup()
    await call.message.answer('Кому будем отправлять?',
                              reply_markup=set_recipients_markup)
    await Admin.MessagePhotoRecipients.set()


@dp.callback_query_handler(state=Admin.MessagePhotoRecipients, text='send_message_to_all_users')
async def send_photo_to_all_users(call: types.CallbackQuery, state: FSMContext):
    """Отправляем фотографию всем пользователям бота"""
    await call.message.edit_reply_markup()
    users = await db.select_all_user_id()
    data = await state.get_data()
    photo_id = data.get('photo_id')
    caption = data.get('caption')
    count_messages = 0
    for user in users:
        count_messages += 1
        await bot.send_photo(chat_id=user, photo=photo_id,
                             caption=f'{caption}')
    await send_menu_admin_callback(call, count_messages)
    await state.finish()


@dp.callback_query_handler(state=Admin.MessagePhotoRecipients,
                           text='send_message_to_users_with_status_1')
async def send_photo_to_users_with_status_1(call: types.CallbackQuery, state: FSMContext):
    """Отправляем фотографию пользователям бота, у которых включена рассылка"""
    await call.message.edit_reply_markup()
    users = await db.select_all_user_id_with_status_1()
    data = await state.get_data()
    photo_id = data.get('photo_id')
    caption = data.get('caption')
    count_messages = 0
    for user in users:
        count_messages += 1
        await bot.send_photo(chat_id=user, photo=photo_id,
                             caption=f'{caption}')
    await send_menu_admin_callback(call, count_messages)
    await state.finish()


@dp.callback_query_handler(state=Admin.MessagePhotoRecipients,
                           text='send_message_to_users_with_status_0')
async def send_photo_to_users_with_status_1(call: types.CallbackQuery, state: FSMContext):
    """Отправляем фотографию пользователям бота, у которых включена рассылка"""
    await call.message.edit_reply_markup()
    users = await db.select_all_user_id_with_status_0()
    data = await state.get_data()
    photo_id = data.get('photo_id')
    caption = data.get('caption')
    count_messages = 0
    for user in users:
        count_messages += 1
        await bot.send_photo(chat_id=user, photo=photo_id,
                             caption=f'{caption}')
    await send_menu_admin_callback(call, count_messages)
    await state.finish()


@dp.callback_query_handler(state=Admin.MessagePhotoRecipients, text='send_private_message')
async def set_recipients_ids(call: types.CallbackQuery):
    """Просим ввести id пользователей для отправки сообщения"""
    await call.message.edit_reply_markup()
    await call.message.answer('Пожалуйста введите id одного пользователя или несколько id через ПРОБЕЛ')
    await Admin.MessagePhotoRecipientsGetID.set()


@dp.message_handler(state=Admin.MessagePhotoRecipientsGetID)
async def get_recipients_ids(message: types.Message, state: FSMContext):
    """Получаем id пользователей для отправки и отправляем сообщение"""
    recipients = message.text.split(' ')
    data = await state.get_data()
    photo_id = data.get('photo_id')
    caption = data.get('caption')
    count_messages = 0
    for user in recipients:
        try:
            await bot.send_photo(chat_id=int(user), photo=photo_id,
                                 caption=f'{caption}')
            count_messages += 1
        except:
            pass
    await send_menu_admin_message(message, count_messages)
    await state.finish()


@dp.callback_query_handler(text='message_type_text', state=Admin.AdminMessageType)
async def set_admin_message_text(call: types.CallbackQuery):
    """Предлагаем написать сообщение"""
    await call.message.answer('Пожалуйста, напишите сообщение')
    await Admin.MessageText.set()


@dp.message_handler(state=Admin.MessageText)
async def get_message_text(message: types.Message, state: FSMContext):
    """Получаем и сохраняем текст сообщения в стейт"""
    message_text = message.text
    await state.update_data(message_text=message_text)
    await message.answer('Отлично.\n'
                         'Кому будем отправлять?',
                         reply_markup=set_recipients_markup)
    await Admin.MessageTextRecipients.set()


@dp.callback_query_handler(state=Admin.MessageTextRecipients, text='send_message_to_all_users')
async def send_message_text_to_all_users(call: types.CallbackQuery, state: FSMContext):
    """Отправляем сообщение всем пользователям бота"""
    await call.message.edit_reply_markup()
    users = await db.select_all_user_id()
    data = await state.get_data()
    message_text = data.get('message_text')
    count_messages = 0
    for user in users:
        await bot.send_message(chat_id=user, text=message_text, disable_web_page_preview=True)
        count_messages += 1
    await send_menu_admin_callback(call, count_messages)
    await state.finish()


@dp.callback_query_handler(state=Admin.MessageTextRecipients,
                           text='send_message_to_users_with_status_1')
async def send_message_text_to_users_with_status_1(call: types.CallbackQuery, state: FSMContext):
    """Отправляем сообщение пользователям бота, у которых включена рассылка"""
    await call.message.edit_reply_markup()
    users = await db.select_all_user_id_with_status_1()
    data = await state.get_data()
    message_text = data.get('message_text')
    count_messages = 0
    for user in users:
        await bot.send_message(chat_id=user, text=message_text, disable_web_page_preview=True)
        count_messages += 1
    await send_menu_admin_callback(call, count_messages)
    await state.finish()


@dp.callback_query_handler(state=Admin.MessageTextRecipients,
                           text='send_message_to_users_with_status_0')
async def send_message_text_to_users_with_status_1(call: types.CallbackQuery, state: FSMContext):
    """Отправляем сообщение пользователям бота, у которых включена рассылка"""
    await call.message.edit_reply_markup()
    users = await db.select_all_user_id_with_status_0()
    data = await state.get_data()
    message_text = data.get('message_text')
    count_messages = 0
    for user in users:
        await bot.send_message(chat_id=user, text=message_text, disable_web_page_preview=True)
        count_messages += 1
    await send_menu_admin_callback(call, count_messages)
    await state.finish()


@dp.callback_query_handler(state=Admin.MessageTextRecipients, text='send_private_message')
async def set_recipients_ids(call: types.CallbackQuery):
    """Просим ввести id пользователей для отправки сообщения"""
    await call.message.edit_reply_markup()
    await call.message.answer('Пожалуйста введите id одного пользователя или несколько id через ПРОБЕЛ')
    await Admin.MessageTextRecipientsGetID.set()


@dp.message_handler(state=Admin.MessageTextRecipientsGetID)
async def get_recipients_ids(message: types.Message, state: FSMContext):
    """Получаем id пользователей для отправки и отправляем сообщение"""
    recipients = message.text.split(' ')
    data = await state.get_data()
    message_text = data.get('message_text')
    count_messages = 0
    for user in recipients:
        try:
            await bot.send_message(chat_id=user, text=message_text, disable_web_page_preview=True)
            count_messages += 1
        except:
            pass
    await send_menu_admin_message(message, count_messages)
    await state.finish()

# @dp.callback_query_handler(text='message_type_photo', state=Admin.AdminMessageType)
# async def
