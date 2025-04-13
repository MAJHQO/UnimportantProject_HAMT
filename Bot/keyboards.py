from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

mainKeyboard=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Заявка на устранение проблемы", callback_data="New_Request")],
    [InlineKeyboardButton(text="Профиль", callback_data="User_Account")]])

accountKeyboard=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить ФИО", callback_data="Change_User_FSL")],
    [InlineKeyboardButton(text="Просмотреть текущие заявки", callback_data="View_Own_Request")],
    [InlineKeyboardButton(text="Назад",callback_data="Back_Scenario_0")]])

backButton=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад",callback_data="Back_Scenario_0")]])