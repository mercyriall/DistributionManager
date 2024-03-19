import asyncio

from aiogram import types, F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram import Bot
import os
import interface_bot.keyboards as keyboards
from database.db_user import DB_Users

router = Router()

db = DB_Users()


class User_input(StatesGroup):
    vk_inputing_cookie = State()
    vk_inputing_link = State()
    tw_inputing_cookie = State()
    tw_inputing_link = State()
    tg_inputing_channel = State()


@router.message(Command('start'))
async def start_handler(msg: Message):
    if await db.check(msg.from_user.id) is False:
        await db.insert_new_user(msg.from_user.id)

    await msg.answer("Привет! Я бот по управлению соц сетями. Для взаимодействия со мной воспользуйся меню.",
                     reply_markup=keyboards.kb_menu)


@router.message(F.text == 'Привет')
async def start_handler(msg: Message):
    if await db.check(msg.from_user.id) is False:
        await db.insert_new_user(msg.from_user.id)

    await msg.answer("Привет! Я бот по управлению соц сетями. Для взаимодействия со мной воспользуйся меню.",
                     reply_markup=keyboards.kb_menu)


@router.message(F.text == "Меню☰")
async def menu_handler(msg: Message):
    await msg.answer("Выбери один из пунктов ниже⬇️.",
                     reply_markup=keyboards.kb_menu)


@router.message(F.text == "Привязанные соц. сети📝")
async def check_networks_handler(msg: Message):
    user = await db.get_data_user(msg.from_user.id)

    usr_list = list(user[2:])

    networks = []

    for elem in usr_list:
        if bool(elem) is True:
            networks.append(1)
        else:
            networks.append(0)

    networks_str = keyboards.str_with_soc_networks(networks)

    await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                     reply_markup=keyboards.reply_kb_builder(networks).as_markup(resize_keyboard=True,
                                                                                 input_field_placeholder="Воспользуйтесь меню ниже"))


@router.message(F.text == "Создать пост💬")
async def create_post_handler(msg: Message):
    # тут должна быть проверка на привязанные аккаунты
    await msg.answer("Напиши пост в следующем сообщении и прикрепи картинки, если есть.",
                     reply_markup=keyboards.kb_networks)


@router.message(StateFilter(None), F.text == "🔴 Вконтакте")
async def vk_input_cookie(msg: Message, state: FSMContext):
    await msg.answer("Загрузите файл с куки данной соц. сети, формат файла должен быть \".txt\"."
                     "При возникновении вопросов, читайте документацию.\n", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(User_input.vk_inputing_cookie)


@router.message(User_input.vk_inputing_cookie, F.document)
async def vk_cookie_inputed(msg: Message, state: FSMContext, bot: Bot):
    extension = '.txt'

    if extension in str(msg.document.file_name):
        path = "C:\\Users\\Endz\\Documents\\GitHub\\DistributionManager\\uploaded_cookies\\vk_cookie.txt"
        await bot.download(
            msg.document.file_id,
            destination=path
        )
        await db.update_cookie(msg.from_user.id, ["vk_cookie.txt"])
        await msg.answer("Куки успешно импортированы.", reply_markup=keyboards.kb_menu)
        await state.clear()
        if (await db.check_link_vk(msg.from_user.id)) is False:
            await msg.answer("Введите ссылку на группу или страницу, с которой предполагается постинг.",
                             reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(User_input.vk_inputing_link)
    else:
        await msg.answer("Что-то не так, вы точно отправили файл с расширением \".txt\"?")


@router.message(User_input.vk_inputing_link)
async def vk_link_inputed(msg: Message, state: FSMContext, bot: Bot):
    start = 'https://vk.com/'
    if start in str(msg.text):
        await msg.answer(f"Вы успешно добавили ссылку: {msg.text}", reply_markup=keyboards.kb_menu)
        await db.insert_link_vk(msg.from_user.id, msg.text)
        await state.clear()
    else:
        await msg.answer("Что-то не так, попробуйте ввести ссылку ещё раз.")



@router.message(F.text == "🟢 Вконтакте")
async def vk_handler(msg: Message):
    await db.delete_link_vk(msg.from_user.id)
    await db.delete_vk_cookie(msg.from_user.id)
    await msg.answer("Вы успешно отвязали эту соц сеть.",
                     reply_markup=keyboards.kb_menu)

@router.message(F.text == "🔴 Telegram")
async def tg_handler(msg: Message):
    await msg.answer("Выбери один из пунктов ниже⬇️.",
                     reply_markup=keyboards.kb_networks)


@router.message(F.text == "🟢 Telegram")
async def tg_handler(msg: Message):
    await db.delete_tg_channel_id(msg.from_user.id)
    await msg.answer("Вы успешно отвязали эту соц сеть.",
                     reply_markup=keyboards.kb_menu)


@router.message(F.text == "🔴 Twitter")
async def tw_handler(msg: Message):
    await msg.answer("Выбери один из пунктов ниже⬇️.",
                     reply_markup=keyboards.kb_networks)


@router.message(F.text == "🟢 Twitter")
async def tw_handler(msg: Message):
    await db.delete_tw_cookie(msg.from_user.id)
    await msg.answer("Вы успешно отвязали эту соц сеть.",
                     reply_markup=keyboards.kb_menu)


@router.message(StateFilter(None), F.text == "Привязать соц. сеть🆕")
async def add_soc_net_handler(msg: Message, state: FSMContext):
    await msg.answer("Загрузите файл с куки данной соц. сети, формат куки должен быть \"*названиесоцсети*_cookie.txt\"."
                     "При возникновении вопросов, читайте документацию.\n")
    await state.set_state(User_input.inputing_cookie)



@router.message(F.text == "Отвязать соц. сеть🗑️️")
async def rm_soc_net_handler(msg: Message):
    await msg.answer("Выбери один из пунктов ниже⬇️.",
                     reply_markup=keyboards.kb_networks)


# @router.message(User_input.inputing_cookie, F.document)
# async def inputing_cookie(msg: Message, bot: Bot):
#     await bot.download(
#         msg.document.file_id,
#         destination=f"./upload_cookies/{msg.file_id}.txt"
#     )


@router.message()
async def unknown_handler(msg: Message):
    await msg.reply("Я тебя не понимаю😢\nПопробуй написать \"\start\" или \"Привет\"!")
