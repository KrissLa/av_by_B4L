from aiogram import types

from aiogram.dispatcher.filters import BoundFilter

from data.config import GROUP, CHANNEL, admins
from loader import bot

member_status = ['creator', 'administrator', 'member']


class IsMemberMessage(BoundFilter):
    async def check(self, message: types.Message):
        ch1 = await bot.get_chat_member(chat_id=GROUP, user_id=message.from_user.id)
        ch2 = await bot.get_chat_member(chat_id=CHANNEL, user_id=message.from_user.id)
        return ch1.status in member_status and ch2.status in member_status


class IsMemberCallback(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        ch1 = await bot.get_chat_member(chat_id=GROUP, user_id=call.from_user.id)
        ch2 = await bot.get_chat_member(chat_id=CHANNEL, user_id=call.from_user.id)
        return ch1.status in member_status and ch2.status in member_status


class IsAdminMessage(BoundFilter):
    async def check(self, message: types.Message):
        print(admins)
        return message.from_user.id in admins


class IsAdminCallback(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        return call.from_user.id in admins


class IsGroupMemberMessage(BoundFilter):
    async def check(self, message: types.Message):
        user_status = await bot.get_chat_member(chat_id=GROUP, user_id=message.from_user.id)
        return user_status.status in member_status


class IsGroupMemberCallback(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        user_status = await bot.get_chat_member(chat_id=GROUP, user_id=call.from_user.id)
        return user_status.status in member_status


class IsNotGroupMemberMessage(BoundFilter):
    async def check(self, message: types.Message):
        user_status = await bot.get_chat_member(chat_id=GROUP, user_id=message.from_user.id)
        return user_status.status not in member_status


class IsNotGroupMemberCallback(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        user_status = await bot.get_chat_member(chat_id=GROUP, user_id=call.from_user.id)
        return user_status.status not in member_status


class IsChannelMemberMessage(BoundFilter):
    async def check(self, message: types.Message):
        user_status = await bot.get_chat_member(chat_id=CHANNEL, user_id=message.from_user.id)
        return user_status.status in member_status


class IsChannelMemberCallback(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        user_status = await bot.get_chat_member(chat_id=CHANNEL, user_id=call.from_user.id)
        return user_status.status in member_status


class IsNotChannelMemberMessage(BoundFilter):
    async def check(self, message: types.Message):
        user_status = await bot.get_chat_member(chat_id=CHANNEL, user_id=message.from_user.id)
        return user_status.status not in member_status


class IsNotChannelMemberCallback(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        user_status = await bot.get_chat_member(chat_id=CHANNEL, user_id=call.from_user.id)
        return user_status.status not in member_status


class IsNotMemberMessage(BoundFilter):
    async def check(self, message: types.Message):
        ch1 = await bot.get_chat_member(chat_id=GROUP, user_id=message.from_user.id)
        ch2 = await bot.get_chat_member(chat_id=CHANNEL, user_id=message.from_user.id)
        return ch1.status not in member_status and ch2.status not in member_status


class IsNotMemberCallback(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        ch1 = await bot.get_chat_member(chat_id=GROUP, user_id=call.from_user.id)
        ch2 = await bot.get_chat_member(chat_id=CHANNEL, user_id=call.from_user.id)
        return ch1.status not in member_status and ch2.status not in member_status
