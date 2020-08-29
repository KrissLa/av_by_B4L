from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.menu_keyboards import menu
from keyboards.inline.inline_keyboards import check_subscriptionsewq
from loader import dp, bot, db

from data.config import GROUP, CHANNEL


@dp.message_handler(commands=['restart'], state="*")
async def restart(message: types.Message, state: FSMContext):
    """Restart"""
    allowed_users = await db.select_all_user_id()
    if message.from_user.id in allowed_users:
        await state.finish()
        await db.change_status(message.from_user.id, False)
        await message.answer("Перезагружен",
                             reply_markup=menu)
    else:
        try:
            ch1 = await bot.get_chat_member(chat_id=GROUP, user_id=message.from_user.id)
            print(ch1.status)
            ch = await bot.get_chat_member(chat_id=CHANNEL, user_id=message.from_user.id)
            print(ch.status)
            if ch1.status == ch.status == 'member':
                try:
                    await db.add_user(user_id=message.from_user.id, name=message.from_user.full_name, status=False,
                                      filter=None, ads_id_1=None, ads_id_2=None, ads_id_3=None, ads_id_4=None,
                                      ads_id_5=None)
                    await message.answer(f'Привет, {message.from_user.full_name}! '
                                         f'Если Вам нужна помощь, нажмите на клавиатуре кнопку Помощь/Инструкция или '
                                         f'введите команду /help',
                                         reply_markup=menu)
                except:
                    print("Что-то пошло не так")

            elif ch1.status == ch.status == 'left':
                await message.answer(f'Для того, чтобы пользоваться ботом'
                                     f' Вам нужно подписаться на нашу группу и новостной канал\n{GROUP}\n{CHANNEL}\n',
                                     reply_markup=ReplyKeyboardRemove())
                await message.answer(f'Если вы уже подписались нажмите',
                                     reply_markup=check_subscriptionsewq)
            elif ch1.status == 'left' and ch.status == 'member':
                await message.answer(f'Для того, чтобы пользоваться ботом'
                                     f' Вам нужно подписаться на нашу группу\n{GROUP}\n',
                                     reply_markup=ReplyKeyboardRemove())
                await message.answer(text=f'Если вы уже подписались нажмите',
                                     reply_markup=check_subscriptionsewq)
            elif ch1.status == 'member' and ch.status == 'left':
                await message.answer(f'Для того, чтобы пользоваться ботом'
                                     f' Вам нужно подписаться на наш новостной канал\n{CHANNEL}\n',
                                     reply_markup=ReplyKeyboardRemove())
                await message.answer(text=f'Если вы уже подписались нажмите',
                                     reply_markup=check_subscriptionsewq)


        except:
            await message.answer(f'Для того, чтобы пользоваться ботом'
                                 f' Вам нужно подписаться на нашу группу и новостной канал\n{GROUP}\n{CHANNEL}\n',
                                 reply_markup=ReplyKeyboardRemove())
            await message.answer(text=f'Если вы уже подписались нажмите',
                                 reply_markup=check_subscriptionsewq)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        ch1 = await bot.get_chat_member(chat_id=GROUP, user_id=message.from_user.id)
        print(ch1.status)
        ch = await bot.get_chat_member(chat_id=CHANNEL, user_id=message.from_user.id)
        print(ch.status)
        if ch1.status == ch.status == 'member':
            try:
                try:

                    await db.add_user(user_id=message.from_user.id, name=message.from_user.full_name, status=False,
                                      filter=None, ads_id_1=None, ads_id_2=None, ads_id_3=None, ads_id_4=None,
                                      ads_id_5=None)
                    await message.answer(f'Привет, {message.from_user.full_name}! '
                                         f'Если Вам нужна помощь, нажмите на клавиатуре кнопку Помощь/Инструкция или '
                                         f'введите команду /help',
                                         reply_markup=menu)
                except:
                    await message.answer(f'Привет, {message.from_user.full_name}! '
                                         f'Если Вам нужна помощь, нажмите на клавиатуре кнопку Помощь/Инструкция или '
                                         f'введите команду /help',
                                         reply_markup=menu)
            except:
                print("Что-то пошло не так")

        elif ch1.status == ch.status == 'left':
            await message.answer(f'Для того, чтобы пользоваться ботом'
                                 f' Вам нужно подписаться на нашу группу и новостной канал\n{GROUP}\n{CHANNEL}\n',
                                 reply_markup=ReplyKeyboardRemove())
            await message.answer(f'Если вы уже подписались нажмите',
                                 reply_markup=check_subscriptionsewq)
        elif ch1.status == 'left' and ch.status == 'member':
            await message.answer(f'Для того, чтобы пользоваться ботом'
                                 f' Вам нужно подписаться на нашу группу\n{GROUP}\n',
                                 reply_markup=ReplyKeyboardRemove())
            await message.answer(text=f'Если вы уже подписались нажмите',
                                 reply_markup=check_subscriptionsewq)
        elif ch1.status == 'member' and ch.status == 'left':
            await message.answer(f'Для того, чтобы пользоваться ботом'
                                 f' Вам нужно подписаться на наш новостной канал\n{CHANNEL}\n',
                                 reply_markup=ReplyKeyboardRemove())
            await message.answer(text=f'Если вы уже подписались нажмите',
                                 reply_markup=check_subscriptionsewq)


    except:
        await message.answer(f'Для того, чтобы пользоваться ботом'
                             f' Вам нужно подписаться на нашу группу и новостной канал\n{GROUP}\n{CHANNEL}\n',
                             reply_markup=ReplyKeyboardRemove())
        await message.answer(text=f'Если вы уже подписались нажмите',
                             reply_markup=check_subscriptionsewq)


@dp.callback_query_handler(text='check_subs')
async def check_subscriptions(call: types.CallbackQuery):
    """Проверяем подписку"""
    try:
        ch1 = await bot.get_chat_member(chat_id=GROUP, user_id=call.from_user.id)
        print(ch1.status)
        ch = await bot.get_chat_member(chat_id=CHANNEL, user_id=call.from_user.id)
        print(ch.status)
        if ch1.status == ch.status == 'member':
            try:
                await db.add_user(user_id=call.from_user.id, name=call.from_user.full_name, status=False,
                                  filter=None, ads_id_1=None, ads_id_2=None, ads_id_3=None, ads_id_4=None,
                                  ads_id_5=None)
                await call.message.answer(f'Привет, {call.from_user.full_name}! '
                                          f'Если Вам нужна помощь, нажмите на клавиатуре кнопку Помощь/Инструкция или '
                                          f'введите команду /help',
                                          reply_markup=menu)
            except:
                print("Что-то пошло не так")

        elif ch1.status == ch.status == 'left':
            await call.message.edit_reply_markup()
            await call.message.answer(f'Для того, чтобы пользоваться ботом'
                                      f' Вам нужно подписаться на нашу группу и новостной канал\n{GROUP}\n{CHANNEL}\n',
                                      reply_markup=ReplyKeyboardRemove())
            await call.message.answer(text=f'Если вы уже подписались нажмите', reply_markup=check_subscriptionsewq)
        elif ch1.status == 'left' and ch.status == 'member':
            await call.message.edit_reply_markup()
            await call.message.answer(f'Для того, чтобы пользоваться ботом'
                                      f' Вам нужно подписаться на нашу группу\n{GROUP}\n',
                                      reply_markup=ReplyKeyboardRemove())
            await call.message.answer(text=f'Если вы уже подписались нажмите',
                                      reply_markup=check_subscriptionsewq)
        elif ch1.status == 'member' and ch.status == 'left':
            await call.message.edit_reply_markup()
            await call.message.answer(f'Для того, чтобы пользоваться ботом'
                                      f' Вам нужно подписаться на наш новостной канал\n{CHANNEL}\n',
                                      reply_markup=ReplyKeyboardRemove())
            await call.message.answer(text=f'Если вы уже подписались нажмите',
                                      reply_markup=check_subscriptionsewq)


    except:
        await call.message.edit_reply_markup()

        await call.message.answer(f'Для того, чтобы пользоваться ботом'
                                  f' Вам нужно подписаться на нашу группу и новостной канал\n{GROUP}\n{CHANNEL}\n',
                                  reply_markup=ReplyKeyboardRemove())
        await call.message.answer(text=f'Если вы уже подписались нажмите',
                                  reply_markup=check_subscriptionsewq)
