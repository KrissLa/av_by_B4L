from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.menu_keyboards import menu
from loader import dp, bot, db

from data.config import GROUP, CHANNEL


@dp.message_handler(commands=['restart'], state="*")
async def restart(message: types.Message, state: FSMContext):
    """Restart"""
    await state.finish()
    await message.answer("Перезагружен",
                         reply_markup=menu)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        ch1 = await bot.get_chat_member(chat_id=GROUP, user_id=message.from_user.id)
        print(ch1.status)
        ch = await bot.get_chat_member(chat_id=CHANNEL, user_id=message.from_user.id)
        print(ch.status)
        if ch1.status == ch.status == 'member':
            try:
                await db.add_user(user_id=message.from_user.id, name=message.from_user.full_name, status=False, filter=None)
            except:
                print("Что-то пошло не так")
            await message.answer(f'Привет, {message.from_user.full_name}!',
                                reply_markup=menu)
        elif ch1.status == ch.status == 'left':
            await message.answer(f'Привет, {message.from_user.full_name}!.\n'
                                 f' Вам нужно подписаться:\n{GROUP}\n{CHANNEL}\n'
                                 f' После подписки нажмите /start',
                                 reply_markup=ReplyKeyboardRemove())
        elif ch1.status == 'left' and ch.status == 'member':
            await message.answer(f' Вам нужно подписаться:\n{GROUP}\n'
                                 f' После подписки нажмите /start',
                                 reply_markup=ReplyKeyboardRemove())
        elif ch1.status == 'member' and ch.status == 'left':
            await message.answer(f' Вам нужно подписаться:\n{CHANNEL}\n'
                                 f' После подписки нажмите /start',
                                 reply_markup=ReplyKeyboardRemove())


    except:
        await message.answer(f'Привет, {message.from_user.full_name}!.\n'
                             f' Вам нужно подписаться:\n{GROUP}\n{CHANNEL}\n'
                             f' После подписки нажмите /start',
                             reply_markup=ReplyKeyboardRemove())



        # try:
        #     await db.add_user(user_id=message.from_user.id, name=message.from_user.full_name, status=False, filter=None)
        # except:
        #     print("Что-то пошло не так")
        # await message.answer(f'Привет, {message.from_user.full_name}!',
        #                      reply_markup=menu)