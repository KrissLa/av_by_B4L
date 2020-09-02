from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("menu", "Открыть меню"),
        types.BotCommand("restart", "Перезапустите бота, если что-то пошло не так"),
    ])