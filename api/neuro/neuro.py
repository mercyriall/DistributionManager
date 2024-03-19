from langchain.schema import  HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

# Авторизация в сервисе GigaChat


def generate_reviews(title):
    chat = GigaChat(credentials='MzI3MGM5NmUtODNkOC00MjY1LWI5Yjgt'
                                'OTc3MDc1YTQ5Y2IyOjM5OWU1NTJlLTFkM'
                                'TMtNGE5Zi05ZGE5LTliMDNlNGRjZjc0ZA==',
                    verify_ssl_certs=False)
    messages = [SystemMessage(
        content="Ты лучший в сфере СММ"),
        HumanMessage(content=f"Перефразируй описание поста: '{title}'")]

    res = chat(messages)
    messages.append(res)
    return res.content
