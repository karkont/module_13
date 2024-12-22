from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


api = '8147259899:AAFhZae2EoWgKu1isYS9NSs1NUYIKjSW1vM'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def urb_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler(text=['Calories'])
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваше количество калорий для поддержания веса: {calories}')
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)