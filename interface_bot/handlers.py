from aiogram import types, F, Router, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR

import interface_bot.keyboards as keyboards
from utils.check_link import check_linked_soc
from database.init_db import database as db


router = Router()

greetings = ["Привет", "привет", "Privet", "privet", "qq", "зкшмуе", "Зкшмуе", "Ghbdtn", "ghbdtn"]

channel_start = "-100"


class UserInput(StatesGroup):
    vk_inputing_cookie = State()
    vk_inputing_link = State()
    vk_unsigning = State()
    tw_inputing_cookie = State()
    tw_unsigning = State()
    tg_inputing_channel = State()
    tg_adding_admin = State()
    posting = State()


@router.message(Command('start'))
async def start_handler(msg: Message):
    if await db.check(msg.from_user.id) is False:
        await db.insert_new_user(msg.from_user.id)

    await msg.answer("Привет! Я бот по управлению соц сетями. Для взаимодействия со мной воспользуйся меню.",
                     reply_markup=keyboards.kb_menu)


@router.message(F.text.in_(greetings))
async def start_handler(msg: Message):
    if await db.check(msg.from_user.id) is False:
        await db.insert_new_user(msg.from_user.id)

    await msg.answer("Привет! Я бот по управлению соц сетями. Для взаимодействия со мной воспользуйся меню.",
                     reply_markup=keyboards.kb_menu)


@router.message(F.text == "Инструкция по использованию🎓")
async def menu_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("<u>Инструкция по использованию:</u>",
                     reply_markup=keyboards.kb_menu,parse_mode=ParseMode.HTML)


@router.message(F.text == "Меню☰")
async def menu_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Выбери один из пунктов ниже⬇️.",
                     reply_markup=keyboards.kb_menu)


@router.message(F.text == "Привязанные соц. сети📝")
async def check_networks_handler(msg: Message):

    networks_str = keyboards.str_with_soc_networks(await check_linked_soc(msg))

    await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                     reply_markup=keyboards.reply_kb_builder(await check_linked_soc(msg)).as_markup(
                         resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))


@router.message(F.text == "Создать пост💬")
async def create_post_handler(msg: Message, state: FSMContext):
    # тут должна быть проверка на привязанные аккаунты
    await msg.answer("Напиши пост в следующем сообщении и прикрепи картинки, если есть.",
                     reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserInput.posting)


@router.message(UserInput.posting)
async def posting(msg: Message, state: FSMContext):
    json_f = msg.model_dump_json()
    print(json_f)
    await msg.answer("Норм.",
                     reply_markup=types.ReplyKeyboardRemove())


@router.message(StateFilter(None), F.text == "🔴 Вконтакте")
async def vk_input_cookie(msg: Message, state: FSMContext):
    await msg.answer("Загрузите файл с куки данной соц. сети, формат файла должен быть \".txt\"."
                     "При возникновении вопросов, читайте инструкцию.\n", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserInput.vk_inputing_cookie)


@router.message(UserInput.vk_inputing_cookie, F.document)
async def vk_cookie_inputed(msg: Message, state: FSMContext, bot: Bot):
    extension = '.txt'

    if extension in str(msg.document.file_name):
        path = "database/uploaded_cookies/vk_cookie.txt"
        await bot.download(
            msg.document.file_id,
            destination=path
        )
        await db.update_cookie(msg.from_user.id, ["vk_cookie.txt"])
        await msg.answer("Куки успешно импортированы.")
        await state.clear()
        if (await db.check_link_vk(msg.from_user.id)) is False:
            await msg.answer("Введите ссылку на группу или страницу, с которой предполагается постинг.",
                             reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(UserInput.vk_inputing_link)
        else:
            networks_str = keyboards.str_with_soc_networks(await check_linked_soc(msg))

            await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                             reply_markup=keyboards.reply_kb_builder(await check_linked_soc(msg)).as_markup(
                                 resize_keyboard=True,
                                 input_field_placeholder="Воспользуйтесь меню ниже"))
    else:
        await msg.answer("Что-то не так, вы точно отправили файл с расширением \".txt\"?")


@router.message(UserInput.vk_inputing_link)
async def vk_link_inputed(msg: Message, state: FSMContext, bot: Bot):
    start = 'https://vk.com/'
    if start in str(msg.text):
        await db.insert_link_vk(msg.from_user.id, msg.text)
        await msg.answer(f"Вы успешно добавили ссылку: {msg.text}")
        await state.clear()
        networks_str = keyboards.str_with_soc_networks(await check_linked_soc(msg))

        await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.reply_kb_builder(await check_linked_soc(msg)).as_markup(
                             resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))
    else:
        await msg.answer("Что-то не так, попробуйте ввести ссылку ещё раз.")


@router.message(F.text == "🟢 Вконтакте")
async def vk_handler(msg: Message, state: FSMContext):
    await msg.answer("Что вы хотите сделать?",
                     reply_markup=keyboards.kb_change_link)
    await state.set_state(UserInput.vk_unsigning)


@router.message(StateFilter(UserInput.vk_unsigning), F.text == "Отвязать соц. сеть🗑️")
async def vk_unsigning(msg: Message, state: FSMContext):
    await db.delete_vk_cookie(msg.from_user.id)
    await db.delete_link_vk(msg.from_user.id)
    await msg.answer("Вы успешно отвязали эту соц. сеть.")
    networks_str = keyboards.str_with_soc_networks(await check_linked_soc(msg))

    await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                     reply_markup=keyboards.reply_kb_builder(await check_linked_soc(msg)).as_markup(
                         resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))
    await state.clear()


@router.message(StateFilter(UserInput.vk_unsigning), F.text == "Поменять ссылку на страницу постинга")
async def vk_unsigning(msg: Message, state: FSMContext):
    await msg.answer("Введите ссылку на группу или страницу, с которой предполагается постинг.",
                     reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserInput.vk_inputing_link)


@router.message(F.text == "🔴 Telegram")
async def tg_handler(msg: Message, state: FSMContext):
    await msg.answer("Пришлите id канала, на котором нужно постить, или перешлите любое сообщение с этого канала.",
                     reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserInput.tg_inputing_channel)


@router.message(UserInput.tg_inputing_channel)
async def tg_inputer(msg: Message, state: FSMContext):

    if msg.forward_origin:
        await db.insert_tg_channel_id(msg.from_user.id, str(msg.forward_origin.chat.id))
        await msg.answer("Id чата тг привязан, теперь добавьте бота в администраторы этого канала.")
        await state.clear()

    elif channel_start in msg.text:
        await db.insert_tg_channel_id(msg.from_user.id, msg.text)
        await msg.answer("Id чата тг привязан, теперь добавьте бота в администраторы этого канала.")
        await state.clear()

    else:
        await msg.answer("Что-то не так, Вы уверены, что это Id чата? Id чата начинаются с \"-100\"",
                         reply_markup=types.ReplyKeyboardRemove())


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR))
async def tg_adding_admn(msg: Message, bot: Bot):
    await bot.send_message(msg.from_user.id,
                           "Теперь я админ, постинг в телеграм привязан.",
                           reply_markup=keyboards.kb_menu)


@router.message(F.text == "🟢 Telegram")
async def tg_handler(msg: Message):
    await db.delete_tg_channel_id(msg.from_user.id)
    await msg.answer(f"Вы успешно отвязали эту соц сеть.")
    networks_str = keyboards.str_with_soc_networks(await check_linked_soc(msg))

    await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                     reply_markup=keyboards.reply_kb_builder(await check_linked_soc(msg)).as_markup(
                         resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))


@router.message(StateFilter(None), F.text == "🔴 Twitter")
async def tw_input_cookie(msg: Message, state: FSMContext):
    await msg.answer("Загрузите файл с куки данной соц. сети, формат файла должен быть \".txt\"."
                     "При возникновении вопросов, читайте документацию.\n", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserInput.tw_inputing_cookie)


@router.message(UserInput.tw_inputing_cookie, F.document)
async def tw_cookie_inputed(msg: Message, state: FSMContext, bot: Bot):
    extension = '.txt'

    if extension in str(msg.document.file_name):
        path = "database/uploaded_cookies/vk_cookie.txt"
        await bot.download(
            msg.document.file_id,
            destination=path
        )
        await db.update_cookie(msg.from_user.id, ["tw_cookie.txt"])
        await msg.answer("Куки успешно импортированы.")
        await state.clear()
        networks_str = keyboards.str_with_soc_networks(await check_linked_soc(msg))

        await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.reply_kb_builder(await check_linked_soc(msg)).as_markup(
                             resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))
    else:
        await msg.answer("Что-то не так, вы точно отправили файл с расширением \".txt\"?")


@router.message(F.text == "🟢 Twitter")
async def tw_handler(msg: Message):
    await db.delete_tw_cookie(msg.from_user.id)
    await msg.answer("Вы успешно отвязали эту соц сеть.")
    networks_str = keyboards.str_with_soc_networks(await check_linked_soc(msg))

    await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                     reply_markup=keyboards.reply_kb_builder(await check_linked_soc(msg)).as_markup(
                         resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))


@router.message()
async def unknown_handler(msg: Message):
    await msg.reply("Я тебя не понимаю😢\nПопробуй написать \"\start\" или \"Привет\"!")
