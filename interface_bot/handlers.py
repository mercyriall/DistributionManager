from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import interface_bot.keyboards as keyboards
from database.db_user import DB_Users

router = Router()

db = DB_Users()


@router.message(Command('start'))
async def start_handler(msg: Message):
    if await db.check(msg.from_user.id) is False:
        await db.insert_new_user(msg.from_user.id)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=keyboards.kb_menu,
        resize_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню ниже"
    )
    await msg.answer("Привет! Я бот по управлению соц сетями. Для взаимодействия со мной воспользуйся меню.",
                     reply_markup=keyboard)


@router.message(F.text == "Меню☰")
async def menu_handler(msg: Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=keyboards.kb_menu,
        resize_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню ниже"
    )
    await msg.answer("Выбери один из пунктов ниже⬇️.",
                     reply_markup=keyboard)


@router.message(F.text == "Привязанные соц. сети📝")
async def check_networks_handler(msg: Message):
    user = db.find_user(msg.from_user.id)

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=keyboards.kb_networks,
        resize_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню ниже"
    )
    await msg.answer("Тут крч ф строка с оформлением и проверкой из бд",
                     reply_markup=keyboard)

@router.message(F.text == "Создать пост💬")
async def check_networks_handler(msg: Message):
    #тут должна быть проверка на привязанные аккаунты
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=keyboards.kb_networks,
        resize_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню ниже"
    )
    await msg.answer("Напиши пост в следующем сообщении и прикрепи картинки, если есть.",
                     reply_markup=keyboard)
    