from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Начать диалог с ботом"),
        types.BotCommand("help", "Получить список доступных команд"),
        types.BotCommand("menu", "Показать меню"),
        types.BotCommand("restart", "На случай, если что-то пошло не так"),
        types.BotCommand("reset_filter", "Сбросить фильтр"),
    ])
