from aiogram.dispatcher.filters.state import StatesGroup, State


class NewFilters(StatesGroup):
    """Стейты для фильтров"""
    WaitFilter = State()


class Notifications(StatesGroup):
    """Стейты для рассылки"""
    WaitNotificationStatus = State()
    NotificationsOn = State()
    ToFilter = State()

class Reports(StatesGroup):
    """Стейты для отчетов об ошибках"""
    WaitReport = State()