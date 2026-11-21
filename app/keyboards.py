from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🏳️ Мои задачи", callback_data="tasks")
        ]
    ]
)

edit = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Добавить план", callback_data="create")
        ],
        [
            InlineKeyboardButton(text="➖ Удалить план", callback_data="remove")
        ]
    ]
)