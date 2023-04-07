from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
        text='Сообщение в голос'
        ),
        KeyboardButton(
        text='Файл txt в голос'
        )
    ],
    [
        KeyboardButton(
            text='Файл pdf в голос'
        ),
        KeyboardButton(
            text='Файл docx в голос'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выбери кнопку ↓', selective=True)