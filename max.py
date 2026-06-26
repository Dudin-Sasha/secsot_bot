from aiogram.utils.markdown import text
from aiogram.filters import CommandStart
import json
import string
import asyncio
import logging
import jsonPart
import emailMessage
from datetime import datetime
import filetype


from maxapi import Bot, Dispatcher, F
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.types.attachments.buttons import (
    LinkButton,
    CallbackButton,
)
from maxapi.connection.base import BaseConnection
from maxapi.context import MemoryContext, StatesGroup, State
from maxapi.types import MessageCreated, Command, InputMedia, BotStarted, InputMediaBuffer
import io
import mimetypes

class Form(StatesGroup):
    description = State()
    time = State()
    date = State()
    file = State()
    card = State()


admins = jsonPart.load_admin_profile()
logging.basicConfig(level=logging.INFO)
__info = jsonPart.loadInfo()
bot = Bot(__info["MAX_TOKEN"])
dp = Dispatcher()



async def handle_media(file_url):
    async with bot.session.get(file_url) as response:
        if response.status == 200:
                    # Скачиваем байты из сети
            file_bytes = await response.read()
                    
                    # 2. Создаем буфер в ОЗУ и сразу наполняем его байтами
            global file_buffer
            file_buffer = io.BytesIO(file_bytes)
                    
                    # 3. Безопасно определяем тип файла, прочитав первые байты
            kind = filetype.guess(file_buffer.read(2048))
            file_buffer.seek(0)  # ОБЯЗАТЕЛЬНО возвращаем указатель в начало буфера!
                    
                    # Получаем тип и расширение
            file_mime = kind.mime if kind else "unknown"
            file_ext = kind.extension if kind else "bin"
                    
            file_buffer.name = f"pinned.{file_ext}"
            print(f"Файл успешно загружен в ОЗУ! Тип данных: {file_mime} (.{file_ext})")
            media_object = InputMediaBuffer(buffer=file_bytes, filename=file_buffer.name)
            return media_object



async def distribution(user_data):
    file = user_data.get('file')
    result =(f"📝 Описание: {user_data.get('description')}\n🕒 Время: {user_data.get('time')}\n📅 Дата: {user_data.get('date')}\n💳 Номер карты: {user_data.get('cardNumber')}")
    if file:
        media_object= await handle_media(file_url=file)
        await emailMessage.sendTo(file_buffer=file_buffer, header="Новая заявка", content=result, filename=file_buffer.name,admins = admins)
        for admin_id in admins:
            print(admin_id)
            try:
                await bot.send_message(user_id=admin_id["Max_id"],text=result,attachments=[media_object])
                #когда сделаю буфер обмена

            except Exception as e:
                logging.error(f"Не удалось отправить сообщение админу {admin_id}: {e}")
    else:    
        await emailMessage.sendTo(header="Новая заявка",content=result,admins=admins)




@dp.message_created(Command(commands="regadmin"))
async def register_admin(event: MessageCreated, command = Command):
    global admins

    parts = event.message.body.text.strip().split(maxsplit=1)
    command_part = parts[0]
    args = parts[1] if len(parts) > 1 else ""
    # Убираем ведущий слэш
    if command_part.startswith('/'):
        command_part = command_part[1:]
    
    print(f"com-parts: {command_part}\nargs: {args}")
    await event.message.answer(f"com-parts: {command_part}\nargs: {args}\n sender: {event.message.sender.user_id}")
    
    tmp = jsonPart.reg_new_admin(cmdArg=args, Max_id = event.message.sender.user_id)
    await event.message.answer(tmp)
    print(tmp)
    admins = jsonPart.loadInfo()



@dp.bot_started()
async def bot_started(event: BotStarted):
    builder = InlineKeyboardBuilder()
    builder.row(
        CallbackButton(text="Доложить", payload="start_form"),
    )
    builder.row(
        CallbackButton(text="О сексот", payload="about_us"),
        LinkButton(text="Наш Сайт", url="https://secsot.online"),
    )

    await bot.send_message(
        chat_id=event.chat_id,
        text=__info['START_TEXT'],
        attachments=[builder.as_markup()]
    )


@dp.message_created(F.message.body.text == "Привет")
async def button_creater(event: MessageCreated):
    builder = InlineKeyboardBuilder()
    builder.row(
        CallbackButton(text="Доложить", payload="start_form"),
    )
    builder.row(
        CallbackButton(text="О сексот", payload="about_us"),
        LinkButton(text="Наш Сайт", url="https://secsot.online"),
    )

    await bot.send_message(
        chat_id=event.chat_id,
        text=__info['START_TEXT'],
        attachments=[builder.as_markup()]
    )

@dp.message_created(F.message.body.text==("список"))
async def button_creater(event: MessageCreated):
    builder = InlineKeyboardBuilder()
    builder.row(
        CallbackButton(text="описание", payload="start_form"),
        CallbackButton(text="время", payload="time"),
    )

    builder.row(
        CallbackButton(text="дата", payload="date"),
        CallbackButton(text="файл", payload="file"),
        CallbackButton(text="карта", payload="card"),
    )

    await event.message.answer(
        text="Этапы:",
        attachments=[builder.as_markup()]
    )


@dp.message_callback(F.callback.payload == 'about_us')
async def About_us(event: MessageCreated):
    await event.message.answer(text = "тут еще ничего нет, я не придумал текст описание, я тут максимум для себя разбираюсь, помогити")

@dp.message_callback(F.callback.payload == 'pass_button')
async def pass_image(event: MessageCreated, context: MemoryContext):
    await context.update_data(file=None)
    print("пропустили этап прикрепления файла")
    await event.message.answer("Вы пропустили прикрепление файла")
    await event.message.answer(__info["CARD_NUMBER_TEXT"])
    await context.set_state(Form.card)

@dp.message_callback(F.callback.payload == 'pc_file')
async def pc_guide(event: MessageCreated):
    print("инструкция к прикреплению файла пк")
    await event.message.answer(text="Чтобы прикрепить файл или видео нужно:\n1) Нажать на скрепку\n2) Выбрать пункт 'файл'\n3) Выбрать нужное видео\\файл\n4) Отправить сообщение ", attachments=[InputMedia(path="max_PC_instructions.jpg")])

@dp.message_callback(F.callback.payload == 'phone_file')
async def phone_guide(event: MessageCreated):
    print("инструкция к прикреплению файла пк")
    await event.message.answer(text="Чтобы прикрепить файл или видео нужно:\n1) Нажать на скрепку\n2) нажать на иконку 'фото' справа сверху в появившемся окне\nона должна измениться и выйдет уведомление об отправлении файлом\n3) Выбрать нужное видео\\файл\n4) Отправить сообщение ", attachments=[InputMedia("max_phone_instruction.jpg")])


@dp.message_callback(F.callback.payload == 'start_form')
async def description_stage(event: MessageCreated, context: MemoryContext):
    print(f"нажали на описание - {F.callback.payload}")
    await context.set_state(Form.description)
    await event.message.answer("опишите что произошло")

@dp.message_callback(F.callback.payload == 'time')
async def description_stage(event: MessageCreated, context: MemoryContext):
    print(f"нажали на время - {F.callback.payload}")

    await context.set_state(Form.time)
    await event.message.answer(__info["TIME_TEXT"])

@dp.message_callback(F.callback.payload == 'date')

async def description_stage(event: MessageCreated, context: MemoryContext):
    print(f"нажали на дату - {F.callback.payload}")

    await context.set_state(Form.date)
    await event.message.answer(__info["DATE_TEXT"])

@dp.message_callback(F.callback.payload == 'file')
async def description_stage(event: MessageCreated, context: MemoryContext):
    print(f"нажали на файл - {F.callback.payload}")

    await context.set_state(Form.file)
    await event.message.answer(__info["FILE_TEXT"])


@dp.message_callback(F.callback.payload == 'card')
async def description_stage(event: MessageCreated, context: MemoryContext):
    print(f"нажали на карту - {F.callback.payload}")

    await event.message.answer(__info["CARD_NUMBER_TEXT"])
    await context.set_state(Form.card)




@dp.message_created(Form.description)
async def description_stage(event: MessageCreated, context: MemoryContext):
    if(event.message.body.text == "" or event.message.body.text == None):
        print("here nothing")
        await event.message.answer("опишите что произошло текстом")
        return
    
    await context.update_data(description=event.message.body.text)
    await context.set_state(Form.time)
    await event.message.answer(__info["TIME_TEXT"])

@dp.message_created(Form.time)
async def age_handler(event: MessageCreated, context: MemoryContext):
    try:
        valid_time = datetime.strptime(event.message.body.text, "%H:%M")
        print("Время корректно:", valid_time.time())
        await context.update_data(time=event.message.body.text)
        await context.set_state(Form.date)
        await event.message.answer(__info['DATE_TEXT'])

    except ValueError:
        await event.message.answer("Неверный формат времени или введены несуществующие значения")

@dp.message_created(Form.date)
async def process_date(event: MessageCreated, context: MemoryContext):
    date = event.message.body.text
    if jsonPart.dateCheck(date):
        print(date)
        await context.update_data(date=date)
        await context.set_state(Form.file)

        builder = InlineKeyboardBuilder()
        builder.row(
            CallbackButton(text="Не прикреплять файл", payload="pass_button"),
        )
        builder.row(
            CallbackButton(text="инструкция 📱", payload="phone_file"),
            CallbackButton(text="инструкция 💻", payload="pc_file"),
        )
        await event.message.answer(
            text=__info['FILE_TEXT']+"\nКак прикрепить файл или видео можете узнать по нажав на кнопку 'инструкция'",
            attachments=[builder.as_markup()]
        )
    else:
        await event.message.answer("не корректная дата")

# @dp.message_created(Form.file)
# async def process_file(event: MessageCreated, context: MemoryContext):


@dp.message_created(Form.card)
async def process_card(event: MessageCreated, context:MemoryContext):
    card_number = event.message.body.text

    if not card_number or not jsonPart.cardcheck(card_number):
        await event.message.answer("Такого номера карты не существует или он введен неверно. Попробуйте еще раз:")
        return 
    await context.update_data(cardNumber=card_number)
    await event.message.answer("Номер карты успешно принят!")


    data = await context.get_data()
    await distribution(data)

    builder = InlineKeyboardBuilder()
    builder.row(CallbackButton(text="Настучать", payload="start_form"),)
    builder.row(CallbackButton(text="О сексот", payload="about_us"),LinkButton(text="Наш Сайт", url="https://secsot.online"))

    await event.message.answer(text="Выберите действие:",attachments=[builder.as_markup()])
    await context.set_state(None) 





@dp.message_created(Form.file)
async def handle_media_messages(event: MessageCreated, context:MemoryContext):
    attachments = getattr(event.message.body, 'attachments', None)
    if attachments:
        for attachment in attachments:
            file_url = None
            print("Доступные атрибуты в attachment:", attachment.__dict__)
            print("Доступные атрибуты в payload:", attachment.payload.__dict__)

            if attachment.type == "video":
                await event.message.answer("Отправьте фотографией, или видео файлом без сжатия")
                # макс говно, нужно отправлять файлом, можно вставить инструкцию
            else:
                payload = getattr(attachment, 'payload', None)
                file_url = getattr(payload, 'url', None) if payload else None

            # Если ссылку найти так и не удалось, пропускаем это вложение во избежание падения кода
            if not file_url:
                print(f"Не удалось найти URL для вложения: {getattr(attachment, 'name', 'Без имени')}")
                continue

            await handle_media(file_url=file_url)
            await context.update_data(file=file_url)
            await event.message.answer(f"Файл успешно сохранен")
            await event.message.answer(__info["CARD_NUMBER_TEXT"])
            await context.set_state(Form.card)
    else:
        text = getattr(event.message.body, 'text', '')
        if text:
            builder = InlineKeyboardBuilder()
            builder.row(CallbackButton(text="Не прикреплять файл", payload="pass_button"))
            await event.message.answer(text="Вы можете пропустить этот этап", attachments=[builder.as_markup()])
    

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


