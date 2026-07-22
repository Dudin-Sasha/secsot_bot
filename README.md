# Важные моменты
### Необходимое ПО

Всё необходимое ПО можно скачать при открытии файла reqireWin.bat (reqireLinux.sh для линукс), либо же установить вручную.

Для запуска ботов необходимо включить запусить файл bots starts.bat (.sh для систем линукс)

Python 3.14 и выше
Пакетный менеджер UV для python
Все библиотеки указаны в файле (requirements.txt)


### data.json
В data.json **Необходимо** указать токен для бота Max 'MAX_TOKEN' и Телеграм 'TG_TOKEN', пароль администратора 'ADMIN_PASSWORD', и данные от корпоративной почты (обязательно корпоративной, рассылка от имени частной почты невозможна).

В этом же файле заменяются и основные реплики бота


### Авторизация
Для того чтобы получать входящие формы нужно войти как администратор.
По умолчанию пароль не установлен.  

Для этого нужно ввести в чате с ботом команду
    /regadmin ваш_пароль ваша_почта@домен.
Например:
    /regadmin my_admin_pass_123 example@mail.ru

Для смены пароля нужно поменять значение в переменной 'ADMINS_PASSWORD' в data.json внутри кавычек, на ваш пароль.


## uv python

### менеджер пакетов

UV менеджер пакетов, в разы быстрее чем предустановленный pip

`powershell -c "irm https://astral.sh/uv/install.ps1"` для win

`curl -LsSf https://astral.sh/uv/install.sh | sh` для linux

  
**Для работы cо сторонними библиотеками нужно создать виртуальную среду**
`uv init 'название проекта'` - для создания среды python
`cd 'название проекта'` - переход к папке
`uv venv` - для создания виртуальной среды 

`uv pip install -r requirements.txt`
(загружает все библиотеки из списка, в этом случае тоже самое что и `uv pip install aiogram maxapi mail json`)


### Основная библиотека: aiogram, maxapi

`uv pip install aiogram maxapi mail json`

Команда также загружает необходимые зависимости

  

## Все библиотеки включая зависимости

    aiofiles==25.1.0
    aiogram==3.28.2
    aiohappyeyeballs==2.6.2
    aiohttp==3.13.5
    aiosignal==1.4.0
    annotated-types==0.7.0
    attrs==26.1.0
    backoff==2.2.1
    certifi==2026.5.20
    filetype==1.2.0
    frozenlist==1.8.0
    idna==3.16
    magic-filter==1.0.12
    maxapi==1.1.0
    multidict==6.7.1
    propcache==0.5.2
    puremagic==1.30
    pydantic==2.13.4
    pydantic-core==2.46.4
    typing-extensions==4.15.0
    typing-inspection==0.4.2
    yarl==1.24.2
