import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Укажи свой токен бота
TOKEN = "YOUR_BOT_TOKEN"

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я твой бот. Используй команды для взаимодействия.")


# Обработчик команды /help
@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Доступные команды:\n/start - Запустить бота\n/help - Получить помощь")


async def main():
    # Удаляем прошлые обновления
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускаем поллинг
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
