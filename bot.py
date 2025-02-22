import logging
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

TOKEN = "7517028969:AAHs6cWqDnzK8xYkIUcE3peGxSNAiwjqkHw"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

game_data = {}

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я бот для игры 'Жених и 17 невест'. Используйте /reg для регистрации.")

@dp.message_handler(commands=["reg"])
async def register(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in game_data:
        game_data[chat_id] = {"players": [], "bachelor": None, "started": False}
    
    if message.from_user.id not in game_data[chat_id]["players"]:
        game_data[chat_id]["players"].append(message.from_user.id)
        await message.answer(f"{message.from_user.first_name} присоединился к игре! ({len(game_data[chat_id]['players'])}/18)")
    
    if len(game_data[chat_id]["players"]) == 18:
        await start_game(chat_id)

async def start_game(chat_id):
    game_data[chat_id]["started"] = True
    players = game_data[chat_id]["players"]
    bachelor = random.choice(players)
    brides = [p for p in players if p != bachelor]
    random.shuffle(brides)
    
    game_data[chat_id]["bachelor"] = bachelor
    game_data[chat_id]["brides"] = {brides[i]: i+1 for i in range(len(brides))}
    
    await bot.send_message(bachelor, "🤵Ты - Жених! Задай вопрос для невест.")
    for bride, number in game_data[chat_id]["brides"].items():
        await bot.send_message(bride, f"👰‍♀️Ты - Невеста №{number}! Жди вопрос от жениха.")
    
    await bot.send_message(chat_id, "Игра началась! Жених получил инструкцию.")

@dp.message_handler(lambda message: message.chat.type == "private")
async def handle_private_message(message: types.Message):
    chat_id = list(game_data.keys())[0]
    if game_data[chat_id]["bachelor"] == message.from_user.id:
        game_data[chat_id]["question"] = message.text
        await bot.send_message(chat_id, f"Жених задал вопрос! {message.text}")
        for bride in game_data[chat_id]["brides"]:
            await bot.send_message(bride, f"{message.text} Ваш ответ?")
    elif message.from_user.id in game_data[chat_id]["brides"]:
        bride_number = game_data[chat_id]["brides"][message.from_user.id]
        await bot.send_message(game_data[chat_id]["bachelor"], f"Ответ невесты №{bride_number}: {message.text}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
