from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Перейти", 
                                 web_app=WebAppInfo(url="https://mechanisms-sofa-chronicles-emotions.trycloudflare.com"))
        ]
    ]
)