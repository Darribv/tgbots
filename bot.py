import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openrouter/auto"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key=OPENROUTER_API_KEY,
)


dialog_history = {}

@dp.message(Command("start"))
async def start(message: Message):
await message.answer("Привет! Я твой AI-ассистент. Напиши мне любой вопрос.")

@dp.message(Command("help"))
async def help_command(message: Message):
await message.answer("Я могу отвечать на вопросы, используя нейросеть. Просто напиши текст!")

@dp.message()
async def ai_answer(message: Message):
user_id = message.from_user.id
user_text = message.text

if user_id not in dialog_history:
dialog_history[user_id] = [
{"role": "system", "content": "Ты полезный и вежливый помощник."}
]


dialog_history[user_id].append({"role": "user", "content": user_text})

try:

response = client.chat.completions.create(
model=MODEL,
messages=dialog_history[user_id],
)

answer = response.choices[0].message.content


dialog_history[user_id].append({"role": "assistant", "content": answer})

await message.answer(answer)

except Exception as e:
await message.answer(f"Ошибка при обращении к AI: {e}")

async def main():
print("Бот запущен...")
await dp.start_polling(bot)

if __name__ == "__main__":
try:
asyncio.run(main())
except KeyboardInterrupt:
print("Бот выключен")
