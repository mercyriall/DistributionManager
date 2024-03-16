from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb_menu = [
    [types.KeyboardButton(text="Привязанные соц. сети📝")],
    [types.KeyboardButton(text="Создать пост💬")]
]

kb_networks = [
    [types.KeyboardButton(text="Привязать новую соц. сеть🆕")],
    [types.KeyboardButton(text="Отвязать соц. сеть🗑️")],
    [types.KeyboardButton(text="Меню☰")]
]

kb_ = [
    [types.KeyboardButton(text="Привязать новую соц. сеть🆕")],
    [types.KeyboardButton(text="Отвязать соц. сеть🗑️")],
    [types.KeyboardButton(text="Меню☰")]
]

def reply_kb_builder(current_state: list):
    i = 0
    soc_networks = ('Telegram', 'Вконтакте', 'Twitter')
    builder = ReplyKeyboardBuilder()
    for elem in soc_networks:
        if current_state[i] == 1:
            builder.add(types.KeyboardButton(text=f"✅ {elem}"))
        else:
            builder.add(types.KeyboardButton(text=f"❌ {elem}"))
        i+=1