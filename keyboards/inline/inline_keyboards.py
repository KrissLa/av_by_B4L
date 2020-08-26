from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_markup = InlineKeyboardMarkup(row_width=2,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(
                                                 text="Отмена",
                                                 callback_data='cancel_filter_change'
                                             ),
                                         ],

                                     ])


to_filter_from_notifications = InlineKeyboardMarkup(row_width=2,
                                                    inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(
                                                                text='Настроить фильтр',
                                                                callback_data='to_filter_from_noti'
                                                            ),
                                                            InlineKeyboardButton(
                                                                text="Отмена",
                                                                callback_data='cancel_to_filter'
                                                            )
                                                        ]
                                                    ])