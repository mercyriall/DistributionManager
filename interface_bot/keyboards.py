from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


kb_menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Привязанные соц. сети📝")],
        [types.KeyboardButton(text="Создать пост💬")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Воспользуйтесь меню ниже"
)


kb_networks = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Привязать соц. сеть🆕")],
        [types.KeyboardButton(text="Отвязать соц. сеть🗑️")],
        [types.KeyboardButton(text="Меню☰")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Воспользуйтесь меню ниже"
)


def str_with_soc_networks(curr_state: list):
    i = 0
    res = '<u>Ваши привязанные соц. сети:</u>\n(🟢 если привязана, 🔴 если не привязана)\n\n'
    soc_networks = ('Вконтакте', 'Twitter', 'Telegram')
    for elem in soc_networks:
        if curr_state[i] == 1:
            res += f"🟢 {elem}\n"
        else:
            res += f"🔴 {elem}\n"
        i += 1
    res += "\nЧтобы привязать какую-либо не привязанную соц. сеть (🔴), нажмите на кнопку с её названием.\n\nЧтобы отвязать какую-либо привязанную соц. сеть (🟢), нажмите на кнопку с её названием."
    return res


def reply_kb_builder(current_state: list):
    i = 0
    soc_networks = ('Вконтакте', 'Twitter', 'Telegram')
    builder = ReplyKeyboardBuilder()
    for elem in soc_networks:
        if current_state[i] == 1:
            builder.add(types.KeyboardButton(text=f"🟢 {elem}"))
        else:
            builder.add(types.KeyboardButton(text=f"🔴 {elem}"))
        i += 1
    builder.add(types.KeyboardButton(text="Меню☰"))
    builder.adjust(3)
    return builder

