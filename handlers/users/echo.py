from aiogram import types

from data.config import CHANNEL, GROUP
from filters.user_filters import IsGroupMemberMessage, IsChannelMemberMessage, IsNotGroupMemberMessage, \
    IsNotChannelMemberMessage, IsMemberMessage, IsNotMemberMessage, IsNotMemberCallback, IsChannelMemberCallback, \
    IsNotGroupMemberCallback, IsGroupMemberCallback, IsNotChannelMemberCallback
from keyboards.inline.inline_keyboards import check_subscriptionsewq
from loader import dp


@dp.message_handler(IsChannelMemberMessage(), IsNotGroupMemberMessage())
async def send_invite_in_group(message: types.Message):
    await message.answer(f'Для доступа к функциям бота Вам необходимо подписаться на наш чат \n{GROUP}',
                         reply_markup=check_subscriptionsewq)


@dp.message_handler(IsGroupMemberMessage(), IsNotChannelMemberMessage())
async def send_invite_in_channel(message: types.Message):
    await message.answer(f'Для доступа к функциям бота Вам необходимо подписаться на наш канал с новостями \n{CHANNEL}',
                         reply_markup=check_subscriptionsewq)


@dp.message_handler(IsNotMemberMessage())
async def send_invite_to_group_and_channel(message: types.Message):
    await message.answer(f'Для доступа к функциям бота Вам необходимо подписаться на наш канал с новостями '
                         f'и вступить в наш чат \n{CHANNEL}\n{GROUP}',
                         reply_markup=check_subscriptionsewq)


@dp.message_handler(IsMemberMessage())
async def bot_echo(message: types.Message):
    await message.answer("Неизвестная команда...\n Пожалуйста, пользуйтесь кнопками из /menu")


@dp.callback_query_handler(IsChannelMemberCallback(), IsNotGroupMemberCallback())
async def send_invite_in_group(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer(f'Для доступа к функциям бота Вам необходимо подписаться на наш чат \n{GROUP}',
                              reply_markup=check_subscriptionsewq)


@dp.callback_query_handler(IsGroupMemberCallback(), IsNotChannelMemberCallback())
async def send_invite_in_channel(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer(
        f'Для доступа к функциям бота Вам необходимо подписаться на наш канал с новостями \n{CHANNEL}',
        reply_markup=check_subscriptionsewq)


@dp.callback_query_handler(IsNotMemberCallback())
async def send_invite_to_group_and_channel(call: types.CallbackQuery):
    """Проверяем подписку"""
    await call.message.edit_reply_markup()
    await call.message.answer(f'Для доступа к функциям бота Вам необходимо подписаться на наш канал с новостями '
                              f'и вступить в наш чат \n{CHANNEL}\n{GROUP}',
                              reply_markup=check_subscriptionsewq)
