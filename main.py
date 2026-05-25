# from toServer import url
from aiogram.utils.markdown import text
from typing import Text
from locale import str
import os
import re
import json
import asyncio
import logging
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandObject,CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, MessageAutoDeleteTimerChanged
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


API_TOKEN = '' 
ADMIN_PASSWORD = "my_admin_pass_123"
ADMINS_FILE = "admins.json"  


router = Router()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def distribution(user_data, res):
    
    for admin_id in admins:
        print("\n\nid администратора = ")
        print(admin_id)
        try:
            f_id = user_data.get('file')
            f_type = user_data.get('file_type')
            print(f_id)
            if f_id:
                if f_type == "photo":
                    await bot.send_photo(chat_id=admin_id, photo=f_id, caption=res, parse_mode="Markdown")
                elif f_type == "document":
                    await bot.send_document(chat_id=admin_id, document=f_id, caption=res, parse_mode="Markdown")
                elif f_type == "video":
                    await bot.send_video(chat_id=admin_id, video=f_id, caption=res, parse_mode="Markdown")
                else:
                    await bot.send_message(chat_id=admin_id, text=res, parse_mode="Markdown")
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение админу {admin_id}: {e}")


def dateCheck(date_str):
    if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", date_str):
        return False
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def cardcheck(card_number: str) -> bool:
    card_number = re.sub(r'\D', '', card_number)
    if not (13 <= len(card_number) <= 19):
        return False

    total = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1
    
    for count in range(num_digits):
        digit = int(card_number[count])
        if not ((count & 1) ^ oddeven):
            digit = digit * 2
            if digit > 9:
                digit = digit - 9
        total += digit
    return (total % 10) == 0



def get_start_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Сообщить о воровстве"))
    builder.add(KeyboardButton(text = "О Нас" ))
    builder.add(KeyboardButton(text="🌐 Перейти на сайт"))
    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True)

@dp.message(CommandStart() if hasattr(types, 'CommandStart') else Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Нажми на кнопку начать, чтобы сообщить о злодеянии.",
        reply_markup=get_start_keyboard()
    )

def load_admins() -> set:
    if not os.path.exists(ADMINS_FILE):
        return set()
    try:
        with open(ADMINS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # JSON сохраняет ключи как строки, переводим их обратно в int
            return set(int(admin_id) for admin_id in data)
    except Exception as e:
        logging.error(f"Ошибка при загрузке админов: {e}")
        return set()

def save_admins(admins_set: set):
    try:
        with open(ADMINS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(admins_set), f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Ошибка при сохранении админов: {e}")



@dp.message(F.text == "О Нас")
async def about_us(message: types.Message):
    await message.answer("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur consectetur facilisis pulvinar. Morbi varius gravida magna, in vulputate diam cursus nec. Etiam sit amet hendrerit turpis. Pellentesque convallis eros eget.")



@dp.message(F.text == "🌐 Перейти на сайт")
async def site(message: types.Message):
    await message.answer(text="https://secsot.online",parse_mode="Markdown")


admins = load_admins()
class Form(StatesGroup):
    description = State()  
    time = State()       
    date = State()   
    file = State()
    cardNumber = State()


@dp.message(F.text == "Сообщить о воровстве")
async def cmd_start_anketa(message: types.Message, state: FSMContext):
    await state.set_state(Form.description)
    # print(f"Старт анкеты для пользователя {message.from_user.id}")
    await message.answer('Привет! Это анкета для заполнения. Опишите, что произошло', reply_markup=ReplyKeyboardRemove())    

@dp.message(Form.description)
async def procces_description(message: types.Message, state: FSMContext):
    if message.text:
        await state.update_data(description=message.text)
        await state.set_state(Form.time)
        await message.answer("В какое примерно время это произошло?\n*Пример: 15:48*", parse_mode="Markdown")
    else:
        await message.answer("Опишите ситуацию текстом", parse_mode="Markdown")


@dp.message(Form.time)
async def process_time(message: types.Message, state: FSMContext):

    try:
        valid_time = datetime.strptime(message.text, "%H:%M")
        print("Время корректно:", valid_time.time())
        await state.update_data(time=message.text)
        await state.set_state(Form.date)
        await message.answer("Какого числа это произошло? *(В формате ДД.ММ.ГГГГ)*", parse_mode="Markdown")
    except ValueError:
        await message.answer("Неверный формат времени или введены несуществующие значения")
    

@dp.message(Form.date)
async def process_date(message: types.Message, state: FSMContext):
    if dateCheck(message.text):
        print("Формат верный")
        await state.update_data(date=message.text)
        await state.set_state(Form.file)
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="⏭️ Пропустить этот шаг", callback_data="skip_file" ))
    
        await message.answer("Отправьте фото или файл (или нажмите кнопку ниже, если файла нет):", 
        reply_markup=builder.as_markup())
        # await message.answer("Можете отправить один файл\фото, или пропустить этот этап", reply_markup=get_inline_start_keyboard())
    else:
        await message.answer("неверная дата")



@dp.callback_query(Form.file, F.data == "skip_file")
async def skip_file_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Фото пропущен")
    await state.update_data(file=None, file_type="text")
    await state.set_state(Form.cardNumber)
    await callback.message.answer("Укажите номер карты для вознаграждения:")
    await callback.message.edit_reply_markup(reply_markup=None)


@dp.message(Form.file, F.photo | F.document | F.video | F.text)
async def proccess_file(message: types.Message, state: FSMContext):
    print("\n я почти работаю! \n")
    if message.photo and len(message.photo) > 0:
        file_id = message.photo[-1].file_id
        file_type = "photo"
    elif message.document:
        file_id = message.document.file_id
        file_type = "document"
    elif message.video:
        file_id = message.video.file_id
        file_type = "video"
    else:
        file_id = None
        file_type = "text"
    await state.update_data(file=file_id, file_type=file_type)
    
    await state.set_state(Form.cardNumber)
    await message.answer("Укажите номер карты для вознаграждения:")


@dp.message(Form.cardNumber)
async def card_handler(message: types.Message, state: FSMContext):
    card_number = message.text
    if not card_number or not cardcheck(card_number):
        await message.answer("Такого номера карты не существует или он введен неверно. Попробуйте еще раз:")
        return 

    await state.update_data(cardNumber=card_number)
    await message.answer("Номер карты успешно принят!")

    # Получаем все собранные данные
    user_data = await state.get_data()
    result = (
        f"📝 **Описание:** {user_data.get('description')}\n"
        f"🕒 **Время:** {user_data.get('time')}\n"
        f"📅 **Дата:** {user_data.get('date')}\n"
        f"💳 **Номер карты:** {user_data.get('cardNumber')}"
    )
    file_type = user_data.get('file_type')

    await message.answer(f"**Данные собраны** \n\n{result}",parse_mode="Markdown", reply_markup=get_start_keyboard())
    # await bot.send_photo(chat_id=message.chat.id, photo=user_data.get('file'), caption=result,parse_mode="Markdown")
    
    await distribution(user_data, result)
    
    await state.clear()
    await state.clear()



@dp.message(Command("regadmin"))
async def register_admin(message: types.Message, command: CommandObject):
    if not command.args:
        await message.answer("Введите команду вместе с секретным паролем.\nПример: `/regadmin ваш_пароль`")
        return

    if command.args.strip() == ADMIN_PASSWORD:
        user_id = message.from_user.id
        
        if user_id in admins:
            await message.answer("Вы уже являетесь администратором данного бота.")
            return

        # Добавляем в локальный сет и сохраняем в файл
        admins.add(user_id)
        save_admins(admins)
        
        await message.answer("Вы успешно зарегистрированы как администратор! Сюда будут приходить анкеты.")
        print(f"Новый админ сохранен в JSON: {user_id}. Всего админов: {len(admins)}")
    else:
        await message.answer("Неверный пароль. Доступ заблокирован.")


async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())