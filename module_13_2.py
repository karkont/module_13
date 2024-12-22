from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio


api = '8147259899:AAFhZae2EoWgKu1isYS9NSs1NUYIKjSW1vM'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def urb_message(message):
    print('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')





if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)