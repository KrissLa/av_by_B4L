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

resume_notifications = InlineKeyboardMarkup(row_width=2,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(
                                                        text='Возобновить рассылку объявлений',
                                                        callback_data='resume_noti'
                                                    )
                                                ],
                                                [
                                                    InlineKeyboardButton(
                                                        text='Отмена',
                                                        callback_data='stop_noti'
                                                    )
                                                ]
                                            ])

start_ads_from_filters = InlineKeyboardMarkup(row_width=2,
                                              inline_keyboard=[
                                                  [
                                                      InlineKeyboardButton(
                                                          text='Включить рассылку',
                                                          callback_data='start_ads_from_filter'
                                                      )
                                                  ]

                                              ])

check_subscriptionsewq = InlineKeyboardMarkup(row_width=2,
                                              inline_keyboard=[
                                                  [
                                                      InlineKeyboardButton(
                                                          text='Проверить подписку',
                                                          callback_data='check_subs'
                                                      )
                                                  ]

                                              ])

admin_menu = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                              text='Количество всех пользователей',
                                              callback_data='count_all_users'
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Количество пользователей с включенной рассылкой',
                                              callback_data='count_users_with_status_1'
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Все неисправленные репорты',
                                              callback_data='select_all_reports_with_status_0'
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Рассылка / Сообщение',
                                              callback_data='mailing'
                                          )
                                      ]

                                  ])

set_message_type_keyboard = InlineKeyboardMarkup(row_width=2,
                                                 inline_keyboard=[
                                                     [
                                                         InlineKeyboardButton(
                                                             text='Фото',
                                                             callback_data='message_type_photo'
                                                         ),
                                                         InlineKeyboardButton(
                                                             text='Обычное сообщение',
                                                             callback_data='message_type_text'
                                                         )
                                                     ]
                                                 ])
confirm_message_photo = InlineKeyboardMarkup(row_width=2,
                                             inline_keyboard=[
                                                 [
                                                     InlineKeyboardButton(
                                                         text='Продолжаем',
                                                         callback_data='send_photo_next'
                                                     ),
                                                     InlineKeyboardButton(
                                                         text='Начать сначала',
                                                         callback_data='new_message_photo'
                                                     )
                                                 ]
                                             ])

set_recipients_markup = InlineKeyboardMarkup(row_width=2,
                                             inline_keyboard=[
                                                 [
                                                     InlineKeyboardButton(
                                                         text='Всем пользователям бота',
                                                         callback_data='send_message_to_all_users'
                                                     )
                                                 ],
                                                 [
                                                     InlineKeyboardButton(
                                                         text='Пользователям с включенной рассылкой',
                                                         callback_data='send_message_to_users_with_status_1'
                                                     )
                                                 ],
                                                 [
                                                     InlineKeyboardButton(
                                                         text='Пользователям с выключенной рассылкой',
                                                         callback_data='send_message_to_users_with_status_0'
                                                     )
                                                 ],
                                                 [
                                                     InlineKeyboardButton(
                                                         text='Личное сообщение от имени бота',
                                                         callback_data='send_private_message'
                                                     )
                                                 ]
                                             ])
