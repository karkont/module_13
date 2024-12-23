from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher import FSMContext
import asyncio

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb1 = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
button = KeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button1 = KeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb1.row(button, button1)

kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
button = KeyboardButton(text='Рассчитать')
button1 = KeyboardButton(text='Информация')
kb.row(button, button1)

@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb1)

@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call):
    await call.message.answer('10 * weight + 6.25 * growth - 5 * age + 5')
    await call.answer()


@dp.message_handler(commands=['start'])
async def urb_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
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