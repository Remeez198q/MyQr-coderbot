import logging
import asyncio
import qrcode
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = 'TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def generate_qr_code(text):
    # Создаем QR-код
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Создаем изображение QR-кода
    img = qr.make_image(fill_color="black", back_color="white")

    # Сохраняем изображение
    img.save("qrcode.png")

async def on_start(message: types.Message):
    # Приветствие при старте бота
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    keyboard_markup.add(
        types.InlineKeyboardButton("Сгенерировать QR-код", callback_data="generate_qr_code"),
        types.InlineKeyboardButton("Помощь", callback_data="help"),
    )
    await message.answer("Здаров, я бот QR-кодер для создания qr.", reply_markup=keyboard_markup)

dp.register_message_handler(on_start, commands=['start'])

@dp.callback_query_handler(lambda c: c.data == 'generate_qr_code')
async def process_generate_qr_code(callback_query: types.CallbackQuery):
    # Отправляем сообщение с инструкциями и генерируем QR-код
    await bot.send_message(callback_query.from_user.id, "Отправь текст или ссылку.")

@dp.callback_query_handler(lambda c: c.data == 'help')
async def process_help(callback_query: types.CallbackQuery):
    help_text = " Имба бот а для дополнительной инфы перейди по ссылке на статью http://surl.li/pbydu"
    await bot.send_message(callback_query.from_user.id, help_text)
    
@dp.message_handler(lambda message: message.text)
async def process_text(message: types.Message):
    # Генерируем QR-код и отправляем его пользователю
    await generate_qr_code(message.text)
    with open("qrcode.png", "rb") as qr_file:
        await bot.send_photo(message.from_user.id, qr_file, caption="Вот ваш QR-код!")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
