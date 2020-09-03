from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import emoji

start_ads_button = KeyboardButton(text=emoji.emojize(":envelope: Включить рассылку", use_aliases=True))
stop_ads_button = KeyboardButton(text=emoji.emojize(":no_bell: Остановить рассылку", use_aliases=True))
back_to_menu_button = KeyboardButton(text=emoji.emojize(":clipboard: Главное меню", use_aliases=True))
cancel_button = KeyboardButton(text=emoji.emojize(":no_entry_sign: Отмена", use_aliases=True))

edit_filter = KeyboardButton(text=emoji.emojize(":memo: Настройка фильтра", use_aliases=True))
help_button = KeyboardButton(text=emoji.emojize(":sos: Помощь / Инструкция", use_aliases=True))
about_button = KeyboardButton(text=emoji.emojize(":boy: О нас", use_aliases=True))
report_button = KeyboardButton(text=emoji.emojize(":heavy_exclamation_mark: Сообщить об ошибке", use_aliases=True))

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            start_ads_button,
            edit_filter
        ],
        [
            help_button,
            about_button
        ],
        [
            report_button,
        ]
    ],
    resize_keyboard=True
)

menu_with_on_notification = ReplyKeyboardMarkup(
    keyboard=[
        [
            stop_ads_button,
            edit_filter
        ],
        [
            help_button,
            about_button
        ],
        [
            report_button,
        ]

    ],
    resize_keyboard=True
)

stopped_notification_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            start_ads_button,
            back_to_menu_button
        ]
    ],
    resize_keyboard=True
)

running_notification_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            stop_ads_button,
        ]
    ],
    resize_keyboard=True
)

cancel_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            cancel_button,
        ]
    ],
    resize_keyboard=True
)

back_to_menu_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            back_to_menu_button,
        ]
    ],
    resize_keyboard=True
)
