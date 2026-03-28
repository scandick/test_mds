import os
import asyncio

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message

load_dotenv()  # Загрузка переменных из .env файла

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не установлен в переменных окружения")
print(TOKEN) 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик всех остальных сообщений (эхо)
@dp.message()
async def echo_handler(message: Message):
    await message.answer(message.text)


async def main():  
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


