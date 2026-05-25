# Python 3.14
    Версия языка программирования на котором написан бот
    можно установить через uv install python 3.14

## Важные моменты
### Токен.
    Для работы бота нужно прописать ему токен в переменную API_TOKEN внутри main.py, который можно получить через @BotFather
### Авторизация
    Для того чтобы получать входящие формы нужно войти как администратор.
    для этого нужно ввести в чате с ботом комманду /regadmin ваш_пароль.
    По умолчанию пароль такой: my_admin_pass_123.  /regadmin my_admin_pass_123
    Для смены пароля нужно поменять значение в переменной ADMINS_PASSWORD, на ваш пароль.


## uv python
### менеджер пакетов
    `uv pip install -r requirement-libs.txt`
    (загружает все библиотеки из списка, в этом случае тоже самое что и `uv pip install aiogram`)

## Основная библиотека: aiogram
    `uv pip install aiogram`
    Команда также загружает зависимости

## Все библиотеки включая зависимости
    aiofiles==25.1.0
    aiogram==3.28.2
    aiohappyeyeballs==2.6.2
    aiohttp==3.13.5
    aiosignal==1.4.0
    annotated-types==0.7.0
    attrs==26.1.0
    certifi==2026.5.20
    frozenlist==1.8.0
    idna==3.16
    magic-filter==1.0.12
    multidict==6.7.1
    propcache==0.5.2
    pydantic==2.13.4
    pydantic-core==2.46.4
    typing-extensions==4.15.0
    typing-inspection==0.4.2
    yarl==1.24.2


