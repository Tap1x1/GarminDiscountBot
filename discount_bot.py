import json
from asyncio import exceptions

from aiogram import Bot,Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import get_data

bot = Bot(token="2058601887:AAHzfLaApPLTmMjBn3X6G82-leQBZMSu8QE", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Часы"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Garmin", reply_markup=keyboard)


@dp.message_handler(Text(equals="Часы"))
async def get_discount_watch(message: types.Message):
    await message.answer("Пожалуйста подождите...")
    get_data()

    with open("result_data.json", encoding="utf-8") as file:
        data =json.load(file)
    for item in data:
        card = f"{hlink(item.get('title'), (item.get('link')))}\n" \
            f"{hbold('Цена: ')} {item.get('price')}\n" \
            f"{hbold('Скидка: ')} {item.get('discount')}\n" \

        await message.answer(card)

@dp.errors_handler(exception=exceptions.TimeoutError)
async def exception_handler(update: types.Update, exception: exceptions.TimeoutError):
    # Do something
    return True


def main():
    executor.start_polling(dp)



if __name__ =="__main__":
    main()