import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebhookInfo
from fastapi import FastAPI
import uvicorn

TOKEN = os.getenv("7517028969:AAHs6cWqDnzK8xYkIUcE3peGxSNAiwjqkHw")  # Используй переменные окружения
WEBHOOK_URL = os.getenv("https://larisaguz.onrender.com")  # Например, твой Render-домен

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook установлен на {WEBHOOK_URL}")

@app.post("/")
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.process_update(telegram_update)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
