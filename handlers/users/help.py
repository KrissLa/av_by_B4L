from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from filters.user_filters import IsMemberMessage
from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(IsMemberMessage(), CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог с ботом',
        '/help - Получить список доступных команд',
        '/menu - Показать меню',
        '/restart - На случай, если что-то пошло не так',
        '/reset_filter - Сбросить фильтр'
    ]
    await message.answer('\n'.join(text))
