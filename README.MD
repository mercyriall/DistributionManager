# <p style="text-align: left;">Distribution bot

<p style="text-align: center;"> <img src="md_assets/img_4.png" width="400" height="230"/></p>



## <a name="Доступные-соц-сети">Доступные соц. сети</a>
 - [X] __[vk](https://vk.com)__
   - [X] _группа_
   - [X] _профиль_
 - [ ] __[~~instagram~~](https://www.instagram.com)__
 - [X] __[telegram](https://web.telegram.org/a/)__
 - [X] __[twitter](https://twitter.com)__
   - [ ] ~~группа~~
   - [X] профиль
 - [ ] __[~~yandex dzen~~](https://dzen.ru)__
---

> __Telegram-bot: [@DistributionBot](https://t.me/TgInstVK_bot)__

---
 ## Установка и запуск

 ### Необходимые библиотеки:
 - _python 3.10_
 - _aiogram 3.4.1_
 - _asyncio 3.12.3_
 - _gigachat 0.1.22_
 - _asyncpg 0.29.0_

установка: _pip install -r requirements.txt_

 ### Для запуска:

запустить файл _main.py_

 ## Начало работы

- __Предоставить боту cookie аккаунтов от соц. сетей, которые вас интересуют__
  - [_инструкция извлечения cookie_](#извлечение-cookie)
  - [_инструкция передачи cookie боту_](#передача-cookie)
  - [_дополнительно_](#дополнительно)
- __Написать пост соответствуя указанным ограничениям ( выставляются соц. сетью )__
  - длина текста
  - количество изображений
  - разрешение изображения

---
## Инструкции
### <a name="извлечение-cookie">__Извлечение cookie__</a>
1) Установить расширение [EditThisCookie](https://chromewebstore.google.com/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=ru) для вашего браузера
2) Создаем текстовый файл формата _.txt_ на компьютере, для удобства рекомендуем называть его в соответствии с соц. сетью ( _cookie_vk.txt_, _cookie_tw.txt_ ), но можно и любым другим образом.
3) Входим в аккаунт соц. сети ( [доступные](#доступные-соц-сети) )
4) Находясь в аккаунте ищем кнопку с имеющимися расширениями

    ![img_1.png](md_assets/img_1.png)
5) Открываем EditThisCookie

    ![img_2.png](md_assets/img_2.png)
> __Находясь в _ВК_ у вас должны быть похожие поля__
6) Нажимаем кнопку 'экспортировать'

    ![img_3.png](md_assets/img_3.png)
7) Открываем раннее созданный txt файл и импортируем наши куки ( сочетание клавиш ctrl+v или правая кнопка мыши --> вставить )

    ![img_5.png](md_assets/img_5.png)
8) Отправляем файл нашему боту

 ### <a name="передача-cookie">__Передача cookie__</a>
1) Переходим в меню привязанные соц. сети

    ![img.png](md_assets/img0.png)
2) Выбираем какую соц. сеть хотим привязать

    ![img_1.png](md_assets/img_98.png)
1) Далее следуйте пошаговой инструкции относительно данной соц. сети
    
    ![img_4.png](md_assets/img_44.png)
2) - В телеграмме необходимо написать id группы или переслать сообщение, как показанно на скриншоте, затем добавить бота в администраторы канала ( не обязательно перед этим его добавлять на канал )
   - В вк необходимо передать файл с куки, затем указать ссылку на профиль/группу в которую планируете постить
   - Для твитера достаточно только файла с куки
2) После прохождения инструкции сразу видно какие соц. сети успешно привязаны

    ![img_5.png](md_assets/img_54.png)

   3) Если подключение по куки не успешно
      - Убедиться, что в момент получения куки вы авторизованы в аккаунте
      - Попробовать получить еще раз, обновив страницу и перед получением находиться на странице своего профиля
      - Проверить целостность отправленного файла

 ### <a name="дополнительно">__Дополнительно__</a>
- Для vk кроме cookie небходимо передать ссылку на страницу, в которой вы хотите сделать пост ( это может быть группа или страница профиля ). Это сделанно для того, чтобы вы могли определить место размещения поста.
 
  ![img.png](md_assets/img.png)
