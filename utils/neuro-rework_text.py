import os

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

# Авторизация в сервисе GigaChat
from dotenv import load_dotenv

load_dotenv()

credentials = os.getenv('NEURO_CREDENTIALS')

def rework_post(title):
    """
    GigaChat возвращает текст с таким же смыслом но другими словами
    """

    chat = GigaChat(credentials=f'{credentials}',
                    verify_ssl_certs=False)
    messages = [SystemMessage(
        content="Ты лучший в сфере СММ"),
        HumanMessage(content=f"Перефразируй описание поста: '{title}'")]

    res = chat(messages)
    messages.append(res)
    return res.content
