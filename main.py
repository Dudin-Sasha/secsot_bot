from emailMessage import sendTo
from locale import str
import io
import asyncio
import logging
from jsonPart import *
# from aiogram import *
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandObject,CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

INFO = loadInfo()

router = Router()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=INFO['TG_TOKEN'])
dp = Dispatcher()

admins = load_admin_profile()


async def distribution(user_data, res):
    for admin_id in admins:
        print(admin_id)
        try:
            f_id = user_data.get('file')
            f_type = user_data.get('file_type')
            if f_type == "photo":
                await bot.send_photo(chat_id=admin_id['id'], photo=f_id, caption=res,parse_mode="Markdown")
            elif f_type == "document":
                await bot.send_document(chat_id=admin_id['id'], document=f_id, caption=res,parse_mode="Markdown")
            elif f_type == "video":
                await bot.send_video(chat_id=admin_id['id'], video=f_id, caption=res,parse_mode="Markdown")
            else:
                await bot.send_message(chat_id=admin_id['id'], text=res, parse_mode="Markdown")

        except Exception as e:
            logging.error(f"Не удалось отправить сообщение админу {admin_id}: {e}")


def get_start_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text = "Сообщить о воровстве"))
    builder.add(KeyboardButton(text = "О Нас" ))
    builder.add(KeyboardButton(text = "🌐 Перейти на сайт"))
    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True)

@router.message(CommandStart() if hasattr(types, 'CommandStart') else Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(INFO["START_TEXT"], reply_markup=get_start_keyboard())


@router.message(F.text == "О Нас")
async def about_us(message: types.Message):
    await message.answer(INFO['ABOUT_US_TEXT'])




@router.message(F.text == "🌐 Перейти на сайт")
async def site(message: types.Message):
    await message.answer(text=INFO[LINK_TEXT],parse_mode="Markdown")

class Form(StatesGroup):
    description = State()  
    time = State()       
    date = State()   
    file = State()
    cardNumber = State()

@dp.message(F.text == "Сообщить о воровстве")
async def cmd_start_anketa(message: types.Message, state: FSMContext):
    await state.set_state(Form.description)
    await message.answer(INFO['DESCRIPTION_TEXT'], reply_markup=ReplyKeyboardRemove())    

@dp.message(Form.description)
async def procces_description(message: types.Message, state: FSMContext):
    print("") #я просто порядок в консоли чутка навожу
    if message.text:
        await state.update_data(description=message.text)
        await state.set_state(Form.time)
        await message.answer(INFO['TIME_TEXT'], parse_mode="Markdown")
    else:
        await message.answer("Опишите ситуацию текстом", parse_mode="Markdown")

@dp.message(Form.time)
async def process_time(message: types.Message, state: FSMContext):
    print("")
    try:
        valid_time = datetime.strptime(message.text, "%H:%M")
        print("Время корректно:", valid_time.time())
        await state.update_data(time=message.text)
        await state.set_state(Form.date)
        await message.answer(INFO['DATE_TEXT'], parse_mode="Markdown")
    except ValueError:
        await message.answer("Неверный формат времени или введены несуществующие значения")
    
@dp.message(Form.date)
async def process_date(message: types.Message, state: FSMContext):
    print("")
    if dateCheck(message.text):
        print("Формат верный")
        await state.update_data(date=message.text)
        await state.set_state(Form.file)
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="⏭️ Пропустить этот шаг", callback_data="skip_file" ))
    
        await message.answer(INFO['FILE_TEXT'], 
        reply_markup=builder.as_markup())
        # await message.answer("Можете отправить один файл\фото, или пропустить этот этап", reply_markup=get_inline_start_keyboard())
    else:
        await message.answer("неверная дата")


@dp.callback_query(Form.file, F.data == "skip_file")
async def skip_file_handler(callback: types.CallbackQuery, state: FSMContext):
    print("")

    await callback.answer("Фото пропущен")
    await state.update_data(file=None, file_type="text")
    await state.set_state(Form.cardNumber)
    await callback.message.answer(INFO['CARD_NUMBER_TEXT'])
    await callback.message.edit_reply_markup(reply_markup=None)

@dp.message(Form.file, F.photo | F.document | F.video | F.text)
async def proccess_file(message: types.Message, state: FSMContext):
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
    await message.answer(INFO['CARD_NUMBER_TEXT'])


@dp.message(Form.cardNumber)
async def card_handler(message: types.Message, state: FSMContext):
    print("")
    card_number = message.text
    if not card_number or not cardcheck(card_number):
        await message.answer("Такого номера карты не существует или он введен неверно. Попробуйте еще раз:")
        return 

    await state.update_data(cardNumber=card_number)
    await message.answer("Номер карты успешно принят!")

    user_data = await state.get_data()
    result =(f"📝 Описание: {user_data.get('description')}\n🕒 Время: {user_data.get('time')}\n📅 Дата: {user_data.get('date')}\n💳 Номер карты: {user_data.get('cardNumber')}")
    file_type = user_data.get('file_type')

    await message.answer(f" \n\n{result}",parse_mode="Markdown", reply_markup=get_start_keyboard())
    
    # рассылка
    if len(admins) >0:
        try:
            path = await bot.get_file(user_data.get('file'))
        except:
            path = None

        if path:
            path = path.file_path
            last_dot_index = path.rfind('.')
            if last_dot_index != -1: 
                afd = path[last_dot_index + 1:]
                file_buffer = io.BytesIO()
                await bot.download_file(path, destination=file_buffer)
                await sendTo(file_buffer=file_buffer, header="Новая заявка", content=result, filename=f'{file_type}.{afd}',admins = admins)
                file_buffer.seek(0)
        else:
            await sendTo(header="Новая заявка", content=result, admins = admins)

        await distribution(user_data, result)

    await state.clear()


@router.message(Command("regadmin"))
async def register_admin(message: types.Message, command: CommandObject):
    tmp = reg_new_admin(cmdArg=command.args, id = message.from_user.id, admins=admins)
    await message.answer(tmp)
    print(tmp)

async def main():
    dp.include_router(router)
    print("Бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
