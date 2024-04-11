from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# кнопочная клавиатура для ситуаций, где нужно подтвердить\отклонить
kb_yes_no = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Да✔️")],
        [types.KeyboardButton(text="Нет❌")]
    ],
    resize_keyboard=True
)


# кнопочная клавиатура для заполнения поста
kb_continue = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Продолжить заполнять пост✏️")]
    ],
    resize_keyboard=True
)


# кнопочная клавиатура для отмены
kb_no = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Нет❌")]
    ],
    resize_keyboard=True
)


# кнопочная клавиатура для отмены постинга
kb_cancel = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Отменить отправку❌")],
        [types.KeyboardButton(text="Нет❌")]
    ],
    resize_keyboard=True
)

# кнопочная клавиатура для основного меню
kb_menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Привязанные соц. сети📝")],
        [types.KeyboardButton(text="Создать пост💬")],
        [types.KeyboardButton(text="Инструкция по использованию🎓")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Воспользуйтесь меню ниже"
)


# кнопочная клавиатура для меню привязки\отвязки социальных сетей
kb_networks = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Привязать соц. сеть🆕")],
        [types.KeyboardButton(text="Отвязать соц. сеть🗑️")],
        [types.KeyboardButton(text="Меню☰")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Воспользуйтесь меню ниже"
)


# кнопочная клавиатура для подменю вконтакте
kb_change_link = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Поменять ссылку на страницу постинга")],
        [types.KeyboardButton(text="Отвязать соц. сеть🗑️")],
        [types.KeyboardButton(text="Меню☰")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Воспользуйтесь меню ниже"
)


# функция для генерации сообщения привязаных соц сетей
def str_with_soc_networks(curr_state: list):
    res = '<u>Ваши привязанные соц. сети:</u>\n(🟢 если привязана, 🔴 если не привязана)\n\n'
    soc_networks = ('Вконтакте', 'Twitter', 'Telegram')
    for i in range(len(soc_networks)):
        if curr_state[i] == 1:
            res += f"🟢 {soc_networks[i]}\n"
        else:
            res += f"🔴 {soc_networks[i]}\n"
    res += ("\nЧтобы привязать какую-либо не привязанную соц. сеть (🔴),"
            " нажмите на кнопку с её названием.\n\nЧтобы отвязать какую-либо привязанную соц. сеть (🟢),"
            " нажмите на кнопку с её названием.")
    return res


# функция для генерации клавиатуры привязанных соц сетей
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


# функция для генерации клавиатуры выбора привязанных соц сетей
def reply_kb_builder_soc(socs: dict):
    count = 0
    builder = ReplyKeyboardBuilder()
    soc_networks = ('Вконтакте', 'Twitter', 'Telegram')
    for elem in soc_networks:
        if socs[elem] == 1:
            count +=1
            builder.add(types.KeyboardButton(text=f"🟢 {elem}"))
        if socs[elem] == 0:
            count += 1
            builder.add(types.KeyboardButton(text=f"🔴 {elem}"))
    builder.add(types.KeyboardButton(text="Опубликовать пост📢"))
    builder.add(types.KeyboardButton(text="Меню☰"))
    if count == 1:
        builder.adjust(1)
    elif count == 2:
        builder.adjust(2)
    else:
        builder.adjust(3)
    return builder
