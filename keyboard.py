from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


# Button
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Start Work", callback_data="start_work")],
        [InlineKeyboardButton(text="Stop Work", callback_data="stop_work")],
        [InlineKeyboardButton(text="Show Time", callback_data="show_time")],
        [InlineKeyboardButton(text="Save Note", callback_data="save_note")], 
        [InlineKeyboardButton(text="Show Note", callback_data="show_note")]
    ])
    return keyboard