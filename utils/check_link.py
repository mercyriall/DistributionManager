from aiogram.types import Message

from database.init_db import database as db


# функция для определения привязанных соц сетей
async def check_linked_soc_list(msg: Message):
    user = await db.get_data_user(msg.from_user.id)

    usr_list = list(user)

    networks = []

    for elem in usr_list:
        if bool(elem) is True:
            networks.append(1)
        else:
            networks.append(0)
    return networks


# функция для выбора соц сетей для постинга
async def check_for_buttons(msg: Message):
    user = await db.get_data_user(msg.from_user.id)

    usr_list = list(user)

    networks_dict ={}

    networks = ["Вконтакте", "Twitter", "Telegram"]

# 1 - если привязана, 2 - если не привязана, 0 - если отменят
    for i in range(3):
        if bool(usr_list[i]) is False:
            networks_dict[networks[i]] = 2
        else:
            networks_dict[networks[i]] = 1

    return networks_dict
