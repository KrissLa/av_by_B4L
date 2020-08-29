from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    """Стейты для админ панели"""
    AdminMenu = State()
    AdminMessageType = State()

    AdminMessagePhoto = State()
    AdminMessagePhotoCaption = State()
    AdminMessagePhotoConfirmation = State()
    MessagePhotoRecipients = State()
    MessagePhotoRecipientsGetID = State()

    MessageText = State()
    MessageTextRecipients = State()
    MessageTextRecipientsGetID = State()