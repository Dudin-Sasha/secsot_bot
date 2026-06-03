# Python 3.14
Версия языка программирования на котором написан бот

## Важные моменты

## data.json
в data.json нужно указать токен для бота, и пароль администратора
также в этом файле можно заменить 

### Авторизация

Для того чтобы получать входящие формы нужно войти как администратор.

для этого нужно ввести в чате с ботом команду

    /regadmin ваш_пароль ваша_почта@домен.

По умолчанию пароль такой: my_admin_pass_123.  

    /regadmin my_admin_pass_123 secsotbot@kalinkovo.com

Для смены пароля нужно поменять значение в переменной ADMINS_PASSWORD в data.json внутри кавычек, на ваш пароль.



## Важно
Далее информация для самостоятельного написания, при клонировании репозитория всё *уже* будет установлено

## uv python

### менеджер пакетов

UV менеджер пакетов, в разы быстрее чем предустановленный pip

`powershell -c "irm https://astral.sh/uv/install.ps1 | more"` для win

`curl -LsSf https://astral.sh/uv/install.sh | less` для linux

  
**Для работы cо сторонними библиотеками нужно создать виртуальную среду**
`uv init 'название проекта'` - для создания среды python
`cd 'название проекта'` - переход к папке
`uv venv` - для создания виртуальной среды 

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