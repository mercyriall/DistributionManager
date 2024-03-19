from aiogram.types import Message

from database.init_db import database as db


async def check_linked_soc(msg: Message):
    user = await db.get_data_user(msg.from_user.id)

    usr_list = list(user[1:])

    networks = []

    for elem in usr_list:
        if bool(elem) is True:
            networks.append(1)
        else:
            networks.append(0)
    return networks
