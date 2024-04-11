import asyncio
from aiogram import types, F, Router, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR
import os
from dotenv import load_dotenv

import interface_bot.keyboards as keyboards
from utils.check_link import check_linked_soc_list
from utils.check_link import check_for_buttons
from utils.post_functions import post_tg, post_tw, post_vk
from database.init_db import database as db

load_dotenv()

abs_path_2_project = os.getenv('ABSOLUTE_PATH_FOR_PROJECT')

router = Router()

greetings = ["привет", "privet", "qq", "зкшмуе", "ghbdtn"]

networks = ["Вконтакте", "Twitter", "Telegram"]

channel_start = "-100"


# класс для сохранения информации, которую вводит пользователь, а также для хранения состояний программы
class UserInput(StatesGroup):
    vk_inputing_cookie = State()
    vk_inputing_link = State()
    vk_unsigning = State()
    tw_inputing_cookie = State()
    tw_unsigning = State()
    tg_inputing_channel = State()
    tg_adding_admin = State()
    getting_images = State()
    gathering_info = State()
    posting = State()
    images_for_post_dict ={}
    text_for_post_dict = {}
    posting_socs_dict = {}


# обработчик нажатия на кнопку инструкции
@router.message(F.text == "Инструкция по использованию🎓")
async def menu_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Для того, чтобы узнать о том, как пользоваться этим ботом - посетите страницу GitHub проекта: "
                     "https://github.com/mercyriall/DistributionManager", keyboards.kb_menu)


# обработчик нажатия на кнопку меню
@router.message(F.text == "Меню☰")
async def menu_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Выбери один из пунктов ниже⬇️.",
                     reply_markup=keyboards.kb_menu)


# обработчик нажатия на кнопку привязывания соц сетей
@router.message(F.text == "Привязанные соц. сети📝")
async def check_networks_handler(msg: Message):
    networks_str = keyboards.str_with_soc_networks(await check_linked_soc_list(msg))

    await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                     reply_markup=keyboards.reply_kb_builder(await check_linked_soc_list(msg)).as_markup(
                         resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))


# обработчик нажатия на кнопку создания поста
@router.message(F.text == "Создать пост💬")
async def create_post_handler(msg: Message, state: FSMContext):
    count = 0
    net_list = await check_linked_soc_list(msg)
    for elem in net_list:
        if elem == 0:
            count += 1
    if count == len(net_list):
        await msg.answer("У вас не привязано ни одной соц. сети. Сначала привяжите хотя бы одну сеть.",
                         reply_markup=keyboards.kb_menu)
    else:
        await msg.answer("Окей, вы планировали прикреплять картинки к посту?\n"
                         "Если да, то отправьте картинки следующим сообщением"
                         "и нажмите кнопку \"Продолжить заполнять пост\","
                         "когда будет загружена последняя картинка.\n"
                         "Если нет - нажми на кнопку \"Нет\"",
                         reply_markup=keyboards.kb_no)
        await state.set_state(UserInput.getting_images)


# обработчик загрузки картинки
@router.message(UserInput.getting_images, F.photo)
async def image_uploading(msg: Message, bot: Bot):
    if msg.from_user.id not in UserInput.images_for_post_dict:
        UserInput.images_for_post_dict[msg.from_user.id] = [msg.photo[-1].file_id]
    else:
        UserInput.images_for_post_dict[msg.from_user.id] = UserInput.images_for_post_dict.get(msg.from_user.id, []) + \
                                                           [msg.photo[-1].file_id]
        print(UserInput.images_for_post_dict)
    path = 'database/images'

    os.chdir(path)
    if not os.path.isdir(str(msg.from_user.id)):
        os.mkdir(str(msg.from_user.id))
        print('папка создана')
    os.chdir('../..')

    await bot.download(
        msg.photo[-1],
        destination=f"{path}/{msg.from_user.id}/{msg.photo[-1].file_id}.jpg"
    )
    await msg.answer("Картинка загружена.", reply_markup=keyboards.kb_continue)
    print(UserInput.images_for_post_dict)


# обработчик нажатия на кнопку продолжения заполнения поста
@router.message(UserInput.getting_images, F.text == "Продолжить заполнять пост✏️")
async def continue_post(msg: Message, state: FSMContext):
    await state.set_state(UserInput.gathering_info)
    await msg.answer("Напишите текст поста:", reply_markup=keyboards.kb_cancel)


# обработчик неверного ввода при загрузке картинки
@router.message(UserInput.getting_images, F.text != "Нет❌")
async def image_error(msg: Message, state: FSMContext):
    await msg.answer("Не понимаю вас вы хотите загрузить картинки?Если да, то загружайте картинки для поста и "
                     "нажмите \"Продолжить заполнять пост\" как загрузите последнюю.",
                     reply_markup=keyboards.kb_cancel)


# обработчик нажатия на кнопку отмены загрузки картинки для поста
@router.message(UserInput.getting_images, F.text == "Нет❌")
async def continue_posting(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Хорошо, двигаемся дальше. Напиши текст поста в следующем сообщении.",
                     reply_markup=keyboards.kb_cancel)
    await state.set_state(UserInput.gathering_info)


# обработчик нажатия на кнопку отмены постинга
@router.message(UserInput.gathering_info, F.text == "Отменить отправку❌")
async def cancel_posting(msg: Message, state: FSMContext, bot: Bot):
    path = 'database/images'
    os.chdir(f'{path}/{str(msg.from_user.id)}')
    for paths, dirs, files in os.walk(os.getcwd()):
        for file in files:
            os.remove(file)
        break
    os.chdir('../../..')
    UserInput.images_for_post_dict[msg.from_user.id] = []
    UserInput.text_for_post_dict[msg.from_user.id] = []
    await state.clear()
    await msg.answer("Вы отменили создание поста.",
                     reply_markup=keyboards.kb_menu)


# обработчик нажатия на кнопку переключения постить соц сети вконтакте
@router.message(UserInput.gathering_info, F.text == "🔴 Вконтакте")
async def unselecting_vk(msg: Message, bot: Bot):
    await bot.delete_message(msg.from_user.id, (msg.message_id - 1))
    await bot.delete_message(msg.from_user.id, msg.message_id)
    for elem in UserInput.posting_socs_dict:
        if elem == "Вконтакте":
            UserInput.posting_socs_dict[elem] = 1
    await msg.answer(
        "Выберите соц. сети, в которых хотите запостить:\nЧтобы исключить соц сеть из списка, нажмите на кнопку с ней.",
        reply_markup=keyboards.reply_kb_builder_soc(UserInput.posting_socs_dict).as_markup(
            resize_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню ниже"))


# обработчик нажатия на кнопку переключения не постить соц сети вконтакте
@router.message(UserInput.gathering_info, F.text == "🟢 Вконтакте")
async def selecting_vk(msg: Message, bot: Bot):
    await bot.delete_message(msg.from_user.id, (msg.message_id - 1))
    await bot.delete_message(msg.from_user.id, msg.message_id)
    for elem in UserInput.posting_socs_dict:
        if elem == "Вконтакте":
            UserInput.posting_socs_dict[elem] = 0
    await msg.answer(
        "Выберите соц. сети, в которых хотите запостить:\nЧтобы исключить соц сеть из списка, нажмите на кнопку с ней.",
        reply_markup=keyboards.reply_kb_builder_soc(UserInput.posting_socs_dict).as_markup(
            resize_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню ниже"))


# обработчик нажатия на кнопку переключения постить соц сети телеграм
@router.message(UserInput.gathering_info, F.text == "🔴 Telegram")
async def unselecting_tg(msg: Message, bot: Bot):
    await bot.delete_message(msg.from_user.id, (msg.message_id - 1))
    await bot.delete_message(msg.from_user.id, msg.message_id)
    for elem in UserInput.posting_socs_dict:
        if elem == "Telegram":
            UserInput.posting_socs_dict[elem] = 1
    await msg.answer(
        "Выберите соц. сети, в которых хотите запостить:\nЧтобы исключить соц сеть из списка, нажмите на кнопку с ней.",
        reply_markup=keyboards.reply_kb_builder_soc(UserInput.posting_socs_dict).as_markup(
            resize_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню ниже"))


# обработчик нажатия на кнопку переключения не постить соц сети телеграм
@router.message(UserInput.gathering_info, F.text == "🟢 Telegram")
async def selecting_tg(msg: Message, bot: Bot):
    await bot.delete_message(msg.from_user.id, (msg.message_id - 1))
    await bot.delete_message(msg.from_user.id, msg.message_id)
    for elem in UserInput.posting_socs_dict:
        if elem == "Telegram":
            UserInput.posting_socs_dict[elem] = 0
    await msg.answer(
        "Выберите соц. сети, в которых хотите запостить:\nЧтобы исключить соц сеть из списка, нажмите на кнопку с ней.",
        reply_markup=keyboards.reply_kb_builder_soc(UserInput.posting_socs_dict).as_markup(
            resize_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню ниже"))


# обработчик нажатия на кнопку переключения постить соц сети твиттер
@router.message(UserInput.gathering_info, F.text == "🔴 Twitter")
async def unselecting_tw(msg: Message, bot: Bot):
    await bot.delete_message(msg.from_user.id, (msg.message_id - 1))
    await bot.delete_message(msg.from_user.id, msg.message_id)
    for elem in UserInput.posting_socs_dict:
        if elem == "Twitter":
            UserInput.posting_socs_dict[elem] = 1
    await msg.answer(
        "Выберите соц. сети, в которых хотите запостить:\nЧтобы исключить соц сеть из списка, нажмите на кнопку с ней.",
        reply_markup=keyboards.reply_kb_builder_soc(UserInput.posting_socs_dict).as_markup(
            resize_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню ниже"))


# обработчик нажатия на кнопку переключения не постить соц сети твиттер
@router.message(UserInput.gathering_info, F.text == "🟢 Twitter")
async def selecting_tw(msg: Message, bot: Bot):
    await bot.delete_message(msg.from_user.id, (msg.message_id - 1))
    await bot.delete_message(msg.from_user.id, msg.message_id)
    for elem in UserInput.posting_socs_dict:
        if elem == "Twitter":
            UserInput.posting_socs_dict[elem] = 0
    print(UserInput.posting_socs_dict)
    await msg.answer(
        "Выберите соц. сети, в которых хотите запостить:\nЧтобы исключить соц сеть из списка, нажмите на кнопку с ней.",
        reply_markup=keyboards.reply_kb_builder_soc(UserInput.posting_socs_dict).as_markup(
            resize_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню ниже"))


# обработчик нажатия на кнопку опубликования поста
@router.message(UserInput.gathering_info, F.text == "Опубликовать пост📢")
async def posting_with_out_ai(msg: Message, state: FSMContext, bot: Bot):
    count = 0
    for elem in UserInput.posting_socs_dict:
        if UserInput.posting_socs_dict[elem] == 0:
            count += 1
    if count == len(UserInput.posting_socs_dict):
        await state.clear()
        await msg.answer("Вы не выбрали ни одной соц сети для постинга. Пожалуйста, попробуйте создать пост ещё раз",
                         reply_markup=keyboards.kb_menu)
    else:
        await state.set_state(UserInput.posting)
        await msg.answer("Хотите ли воспользоваться функцией оригинальности текста?\nВ случае положительного ответа, "
                         "в телеграм будет опубликован оригинальный пост, а в остальные выбранные соц. сети пост, "
                         "который будет отражать смысл оригинального поста, но написан будет другими словами."
                         "\nВ случае отрицательного ответа, все соц. сети получат один и тот же пост.",
                         reply_markup=keyboards.kb_yes_no)


# обработчик нажатия на кнопку использования функции генерации оригинального текста для поста
@router.message(UserInput.posting, F.text == "Да✔️")
async def posting_with_ai(msg: Message, state: FSMContext, bot: Bot):
    for elem in UserInput.posting_socs_dict:
        if elem == "Telegram" and UserInput.posting_socs_dict[elem] == 1:
            await post_tg(UserInput.images_for_post_dict, UserInput.text_for_post_dict, msg, bot)
            await msg.answer("Пост опубликован в Телеграм.")
        if elem == "Twitter" and UserInput.posting_socs_dict[elem] == 1:
            await post_tw(UserInput.text_for_post_dict, msg, True)
            await msg.answer("Пост опубликован в Твиттер.")
        if elem == "Вконтакте" and UserInput.posting_socs_dict[elem] == 1:
            await post_vk(UserInput.text_for_post_dict, msg, True)
            await msg.answer("Пост опубликован в Вконтакте.")
    await msg.answer("Пост опубликован во всех соц сетях.",
                     reply_markup=keyboards.kb_menu)
    path = 'database/images'
    os.chdir(f'{path}/{str(msg.from_user.id)}')
    for paths, dirs, files in os.walk(os.getcwd()):
        for file in files:
            os.remove(file)
        break
    os.chdir('../../..')
    await state.clear()
    UserInput.images_for_post_dict[msg.from_user.id] = []
    UserInput.text_for_post_dict[msg.from_user.id] = ''


# обработчик нажатия на кнопку не использования функции генерации оригинального текста для поста
@router.message(UserInput.posting, F.text == "Нет❌")
async def posting_without_ai(msg: Message, state: FSMContext, bot: Bot):
    for elem in UserInput.posting_socs_dict:
        if elem == "Telegram" and UserInput.posting_socs_dict[elem] == 1:
            await post_tg(UserInput.images_for_post_dict, UserInput.text_for_post_dict, msg, bot)
            await msg.answer("Пост опубликован в Телеграм.")
        if elem == "Twitter" and UserInput.posting_socs_dict[elem] == 1:
            await post_tw(UserInput.text_for_post_dict, msg, False)
            await msg.answer("Пост опубликован в Твиттер.")
        if elem == "Вконтакте" and UserInput.posting_socs_dict[elem] == 1:
            await post_vk(UserInput.text_for_post_dict, msg, False)
            await msg.answer("Пост опубликован в Вконтакте.")
    await msg.answer("Пост опубликован во всех соц сетях.",
                     reply_markup=keyboards.kb_menu)
    path = 'database/images'
    os.chdir(f'{path}/{str(msg.from_user.id)}')
    for paths, dirs, files in os.walk(os.getcwd()):
        for file in files:
            os.remove(file)
        break
    os.chdir('../../..')
    await state.clear()
    UserInput.images_for_post_dict[msg.from_user.id] = []
    UserInput.text_for_post_dict[msg.from_user.id] = ''


# обработчик выбора соц сетей для постинга
@router.message(UserInput.gathering_info)
async def soc_select(msg: Message,):
    UserInput.posting_socs_dict = await check_for_buttons(msg)
    UserInput.text_for_post_dict[msg.from_user.id] = msg.text
    await msg.answer("Выберите соц. сети, в которых хотите запостить:\n"
                     "Чтобы исключить соц сеть из списка, нажмите на кнопку с ней.",
                     reply_markup=keyboards.reply_kb_builder_soc(UserInput.posting_socs_dict).as_markup(
                         resize_keyboard=True,
                         input_field_placeholder="Воспользуйтесь меню ниже")
                     )


# обработчик нажатия на кнопку привязки вконтакте
@router.message(StateFilter(None), F.text == "🔴 Вконтакте")
async def vk_input_cookie(msg: Message, state: FSMContext):
    await msg.answer("Загрузите файл с куки данной соц. сети, формат файла должен быть \".txt\"."
                     "При возникновении вопросов, читайте инструкцию.\n", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserInput.vk_inputing_cookie)


# обработчик загрузки файла с куки для вконтакте
@router.message(UserInput.vk_inputing_cookie, F.document)
async def vk_cookie_inputed(msg: Message, state: FSMContext, bot: Bot):
    extension = '.txt'
    path = 'database/uploaded_cookies'
    if extension in str(msg.document.file_name):
        os.chdir(path)
        if not os.path.isdir(str(msg.from_user.id)):
            os.mkdir(str(msg.from_user.id))
            print('папка создана')
        print(os.getcwd())
        os.chdir('../..')

        await bot.download(
            msg.document.file_id,
            destination=f"{path}/{str(msg.from_user.id)}/vk_cookie.txt"
        )

        await db.update_cookie(msg.from_user.id, "vk_cookie.txt")
        await msg.answer("Куки успешно импортированы.")
        os.chdir(f'{path}/{str(msg.from_user.id)}')
        for paths, dirs, files in os.walk(os.getcwd()):
            for file in files:
                os.remove(file)
            break
        os.chdir('../../..')
        await state.clear()
        if (await db.check_link_vk(msg.from_user.id)) is False:
            await msg.answer("Введите ссылку на группу или страницу, с которой предполагается постинг.",
                             reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(UserInput.vk_inputing_link)
        else:
            networks_str = keyboards.str_with_soc_networks(await check_linked_soc_list(msg))

            await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                             reply_markup=keyboards.reply_kb_builder(await check_linked_soc_list(msg)).as_markup(
                                 resize_keyboard=True,
                                 input_field_placeholder="Воспользуйтесь меню ниже"))
    else:
        await msg.answer("Что-то не так, вы точно отправили файл с расширением \".txt\"?")


# обработчик ввода ссылки на страницу для постинга вконтакте
@router.message(UserInput.vk_inputing_link)
async def vk_link_inputed(msg: Message, state: FSMContext, bot: Bot):
    start = 'https://vk.com/'
    if start in str(msg.text):
        await db.insert_link_vk(msg.from_user.id, msg.text)
        await msg.answer(f"Вы успешно добавили ссылку: {msg.text}")
        await state.clear()
        networks_str = keyboards.str_with_soc_networks(await check_linked_soc_list(msg))

        await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.reply_kb_builder(await check_linked_soc_list(msg)).as_markup(
                             resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))
    else:
        await msg.answer("Что-то не так, попробуйте ввести ссылку ещё раз.")


# обработчик нажатия на кнопку вконтакте для редактирования или удаления куки
@router.message(F.text == "🟢 Вконтакте")
async def vk_handler(msg: Message, state: FSMContext):
    await msg.answer("Что вы хотите сделать?",
                     reply_markup=keyboards.kb_change_link)
    await state.set_state(UserInput.vk_unsigning)


# обработчик нажатия на кнопку вконтакте для отвязки соц сети
@router.message(UserInput.vk_unsigning, F.text == "Отвязать соц. сеть🗑️")
async def vk_unsigning(msg: Message, state: FSMContext):
    await db.delete_vk_cookie(msg.from_user.id)
    await db.delete_link_vk(msg.from_user.id)
    await msg.answer("Вы успешно отвязали эту соц. сеть.")
    networks_str = keyboards.str_with_soc_networks(await check_linked_soc_list(msg))

    await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                     reply_markup=keyboards.reply_kb_builder(await check_linked_soc_list(msg)).as_markup(
                         resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))
    await state.clear()


# обработчик нажатия на кнопку вконтакте для изменения страницы постинга
@router.message(UserInput.vk_unsigning, F.text == "Поменять ссылку на страницу постинга")
async def vk_unsigning(msg: Message, state: FSMContext):
    await msg.answer("Введите ссылку на группу или страницу, с которой предполагается постинг.",
                     reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserInput.vk_inputing_link)


# обработчик нажатия на кнопку телеграм для привязки соц сети
@router.message(F.text == "🔴 Telegram")
async def tg_handler(msg: Message, state: FSMContext):
    await msg.answer("Пришлите id канала, на котором нужно постить, или перешлите любое сообщение с этого канала.",
                     reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserInput.tg_inputing_channel)


# обработчик нажатия на кнопку телеграм для привязки соц сети
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


# обработчик добавления бота в администраторы канала
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR))
async def tg_adding_admn(msg: Message, bot: Bot):
    await bot.send_message(msg.from_user.id,"Теперь я админ, постинг в телеграм привязан.")
    networks_str = keyboards.str_with_soc_networks(await check_linked_soc_list(msg))

    await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                     reply_markup=keyboards.reply_kb_builder(await check_linked_soc_list(msg)).as_markup(
                         resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))


# обработчик удаления бота из администраторов канала
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR >> IS_NOT_MEMBER))
async def tg_adding_admn(msg: Message, bot: Bot):
    await db.delete_tg_channel_id(msg.from_user.id)
    await bot.send_message(msg.from_user.id,
                           "Меня удалили из админов вашего канала, больше не могу постить.",
                           reply_markup=keyboards.kb_menu)


# обработчик нажатия на кнопку телеграм для отвязки соц сети
@router.message(F.text == "🟢 Telegram")
async def tg_handler(msg: Message):
    await msg.answer(f"Вы уверены, что хотите отвязать эту соц сеть?",
                     reply_markup=keyboards.kb_yes_no)


# обработчик нажатия на кнопку привязки твиттера
@router.message(StateFilter(None), F.text == "🔴 Twitter")
async def tw_input_cookie(msg: Message, state: FSMContext):
    await msg.answer("Загрузите файл с куки данной соц. сети, формат файла должен быть \".txt\"."
                     "При возникновении вопросов, читайте документацию.\n", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserInput.tw_inputing_cookie)


# обработчик загрузки файла с куки для твиттера
@router.message(UserInput.tw_inputing_cookie, F.document)
async def tw_cookie_inputed(msg: Message, state: FSMContext, bot: Bot):
    extension = '.txt'
    path = 'database/uploaded_cookies'
    if extension in str(msg.document.file_name):
        os.chdir(path)
        if not os.path.isdir(str(msg.from_user.id)):
            os.mkdir(str(msg.from_user.id))
            print('папка создана')
        os.chdir('../..')

        await bot.download(
            msg.document.file_id,
            destination=f"{path}/{str(msg.from_user.id)}/tw_cookie.txt"
        )

        await db.update_cookie(msg.from_user.id, "tw_cookie.txt")
        await msg.answer("Куки успешно импортированы.")
        os.chdir(f'{path}/{str(msg.from_user.id)}')
        for paths, dirs, files in os.walk(os.getcwd()):
            for file in files:
                os.remove(file)
            break
        os.chdir('../../..')
        await state.clear()
        networks_str = keyboards.str_with_soc_networks(await check_linked_soc_list(msg))

        await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.reply_kb_builder(await check_linked_soc_list(msg)).as_markup(
                             resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))
    else:
        await msg.answer("Что-то не так, вы точно отправили файл с расширением \".txt\"?")


# обработчик нажатия на кнопку твиттер для отвязки соц сети
@router.message(F.text == "🟢 Twitter")
async def tw_handler(msg: Message, state: FSMContext):
    await msg.answer(f"Вы уверены, что хотите отвязать эту соц сеть?",
                     reply_markup=keyboards.kb_yes_no)
    await state.set_state(UserInput.tw_unsigning)


# обработчик отвязывания соц сети твиттер
@router.message(UserInput.tw_unsigning, F.text == "Да✔️")
async def tw_handler(msg: Message, state: FSMContext):
    await db.delete_tw_cookie(msg.from_user.id)
    await msg.answer("Вы успешно отвязали соц. сеть.")
    networks_str = keyboards.str_with_soc_networks(await check_linked_soc_list(msg))

    await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                     reply_markup=keyboards.reply_kb_builder(await check_linked_soc_list(msg)).as_markup(
                         resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))
    await state.clear()


# обработчик отмены отвязывания соц сети твиттер
@router.message(UserInput.tw_unsigning, F.text == "Нет❌")
async def tw_handler(msg: Message, state: FSMContext):
    networks_str = keyboards.str_with_soc_networks(await check_linked_soc_list(msg))

    await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                     reply_markup=keyboards.reply_kb_builder(await check_linked_soc_list(msg)).as_markup(
                         resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))
    await state.clear()


# обработчик подтверждения отвязывания соц сети телеграм
@router.message(F.text == "Да✔️")
async def tg_handler(msg: Message):
    await db.delete_tg_channel_id(msg.from_user.id)
    networks_str = keyboards.str_with_soc_networks(await check_linked_soc_list(msg))

    await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                     reply_markup=keyboards.reply_kb_builder(await check_linked_soc_list(msg)).as_markup(
                         resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))


# обработчик отмены отвязывания соц сети телеграм
@router.message(F.text == "Нет❌")
async def tg_handler(msg: Message):
    networks_str = keyboards.str_with_soc_networks(await check_linked_soc_list(msg))

    await msg.answer(networks_str, parse_mode=ParseMode.HTML,
                     reply_markup=keyboards.reply_kb_builder(await check_linked_soc_list(msg)).as_markup(
                         resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню ниже"))


# обработчик команды начала работы бота
@router.message(Command('start'))
async def start_handler(msg: Message):
    if await db.check(msg.from_user.id) is False:
        await db.insert_new_user(msg.from_user.id)

    await msg.answer("Привет! Я бот по управлению соц сетями. Для взаимодействия со мной воспользуйся меню.",
                     reply_markup=keyboards.kb_menu)


# обработчик сообщения для начала работы бота
@router.message(F.text.lower().in_(greetings))
async def start_handler(msg: Message):
    if await db.check(msg.from_user.id) is False:
        await db.insert_new_user(msg.from_user.id)

    await msg.answer("Привет! Я бот по управлению соц сетями. Для взаимодействия со мной воспользуйся меню.",
                     reply_markup=keyboards.kb_menu)


# обработчик непонятных для бота команд
@router.message()
async def unknown_handler(msg: Message):
    await msg.reply("Я тебя не понимаю😢\nПопробуй написать \"\start\" или \"Привет\"!")
