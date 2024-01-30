from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel_button_kb = "❌ Прервать заполнение формы"

def form_cancel_kb() -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text=cancel_button_kb)]]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Прервать заполнение формы"
    )