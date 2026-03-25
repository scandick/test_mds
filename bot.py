import os
import asyncio
# import logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# # Логирование
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

load_dotenv()  # Загрузка переменных из .env файла

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не установлен в переменных окружения")

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я эхобот. Отправь мне любое сообщение, и я его повторю.")


# Обработчик команды /help
@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Я просто повторяю твои сообщения. Отправь мне текст!")


# Обработчик всех остальных сообщений (эхо)
@dp.message()
async def echo_handler(message: Message):
    await message.answer(f"Ты написал: {message.text}")


async def main():    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


