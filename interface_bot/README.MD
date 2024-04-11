
### handlers.py
```python
    class UserInput(StatesGroup):
    """класс для сохранения информации, которую вводит пользователь, а также для хранения состояний программы"""
```
---

```python
async def menu_instruction_handler(msg: Message, state: FSMContext):
    """обработчик нажатия на кнопку инструкции"""
```
 ```python
async def menu_handler(msg: Message, state: FSMContext):
    """обработчик нажатия на кнопку меню"""
```
```python
async def check_networks_handler(msg: Message):
    """обработчик нажатия на кнопку создания поста"""
```
```python
async def create_post_handler(msg: Message, state: FSMContext):
    """обработчик нажатия на кнопку создания поста"""
```
```python
async def image_uploading(msg: Message, bot: Bot):
    """обработчик загрузки картинки"""
```
```python
async def continue_post(msg: Message, state: FSMContext):
    """обработчик нажатия на кнопку продолжения заполнения поста"""
```
```python
async def image_error(msg: Message, state: FSMContext):
    """обработчик неверного ввода при загрузке картинки"""
```
```python
async def continue_posting(msg: Message, state: FSMContext):
    """обработчик нажатия на кнопку отмены загрузки картинки для поста"""
```
```python
async def cancel_posting(msg: Message, state: FSMContext, bot: Bot):
    """обработчик нажатия на кнопку отмены постинга"""
```
```python
async def unselecting_vk(msg: Message, bot: Bot):
    """обработчик нажатия на кнопку переключения постить соц сети вконтакте"""
```
```python
async def selecting_vk(msg: Message, bot: Bot):
    """обработчик нажатия на кнопку переключения не постить соц сети вконтакте"""
```
```python
async def unselecting_tg(msg: Message, bot: Bot):
    """обработчик нажатия на кнопку переключения постить соц сети телеграм"""
```
```python
async def selecting_tg(msg: Message, bot: Bot):
    """обработчик нажатия на кнопку переключения не постить соц сети телеграм"""
```
```python
async def unselecting_tw(msg: Message, bot: Bot):
    """обработчик нажатия на кнопку переключения постить соц сети твиттер"""
```
```python
async def selecting_tw(msg: Message, bot: Bot):
    """обработчик нажатия на кнопку переключения не постить соц сети твиттер"""
```
```python
async def posting_with_out_ai(msg: Message, state: FSMContext, bot: Bot):
    """обработчик нажатия на кнопку опубликования поста"""
```
```python
async def posting_with_ai(msg: Message, state: FSMContext, bot: Bot):
    """обработчик нажатия на кнопку использования функции генерации оригинального текста для поста"""
```
```python
async def posting_without_ai(msg: Message, state: FSMContext, bot: Bot):
    """обработчик нажатия на кнопку не использования функции генерации оригинального текста для поста"""
```
```python
async def soc_select(msg: Message,):
    """обработчик выбора соц сетей для постинга"""
```
```python
async def vk_input_cookie(msg: Message, state: FSMContext):
    """обработчик нажатия на кнопку привязки вконтакте"""
```
```python
async def vk_cookie_inputed(msg: Message, state: FSMContext, bot: Bot):
    """обработчик загрузки файла с куки для вконтакте"""
```
```python
async def vk_link_inputed(msg: Message, state: FSMContext, bot: Bot):
    """обработчик ввода ссылки на страницу для постинга вконтакте"""
```
```python
async def vk_handler(msg: Message, state: FSMContext):
    """обработчик нажатия на кнопку вконтакте для редактирования или удаления куки"""
```
```python
async def vk_unsigning(msg: Message, state: FSMContext):
    """обработчик нажатия на кнопку вконтакте для отвязки соц сети"""
```
```python
async def vk_unsigning(msg: Message, state: FSMContext):
    """обработчик нажатия на кнопку вконтакте для изменения страницы постинга"""
```
```python
async def tg_handler(msg: Message, state: FSMContext):
    """обработчик нажатия на кнопку телеграм для привязки соц сети"""
```
```python
async def tg_inputer(msg: Message, state: FSMContext):
    """обработчик нажатия на кнопку телеграм для привязки соц сети"""
```
```python
async def tg_adding_admn(msg: Message, bot: Bot):
    """обработчик добавления бота в администраторы канала"""
```
```python
async def tg_adding_admn(msg: Message, bot: Bot):
    """обработчик нажатия на кнопку телеграм для отвязки соц сети"""
```
```python
async def tw_input_cookie(msg: Message, state: FSMContext):
    """обработчик нажатия на кнопку привязки твиттера"""
```
```python
async def tw_cookie_inputed(msg: Message, state: FSMContext, bot: Bot):
    """обработчик нажатия на кнопку привязки твиттера"""
```
```python
async def tw_handler(msg: Message, state: FSMContext):
    """обработчик нажатия на кнопку твиттер для отвязки соц сети"""
```
```python
async def tw_handler(msg: Message, state: FSMContext):
    """обработчик отвязывания соц сети твиттер"""
```
```python
async def tw_handler(msg: Message, state: FSMContext):
    """обработчик отмены отвязывания соц сети твиттер"""
```
```python
async def tg_handler(msg: Message):
    """обработчик подтверждения отвязывания соц сети телеграм"""
```
```python
async def tg_handler(msg: Message):
    """обработчик отмены отвязывания соц сети телеграм"""
```
```python
async def start_handler(msg: Message):
    """обработчик команды начала работы бота"""
```
```python
async def start_handler(msg: Message):
    """обработчик сообщения для начала работы бота"""
```
```python
async def unknown_handler(msg: Message):
    """обработчик непонятных для бота команд"""
```

### keyboards.py

---

```python
def str_with_soc_networks(curr_state: list):
    """функция для генерации сообщения привязаных соц сетей"""
```
 ```python
def reply_kb_builder(current_state: list):
    """функция для генерации клавиатуры привязанных соц сетей"""
```
```python
def reply_kb_builder_soc(socs: dict):
    """функция для генерации клавиатуры выбора привязанных соц сетей"""
```