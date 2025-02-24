import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from telegram_token import BOT_TOKEN, FIRST_MESSAGE
from datetime import datetime

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

is_working = False


def get_current_time():
    return datetime.now().strftime("%H:%M:%S")


# Buttons
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Start Work", callback_data="start_work")],
        [InlineKeyboardButton(text="Stop Work", callback_data="stop_work")],
        [InlineKeyboardButton(text="Show Time", callback_data="show_time")]
    ])
    return keyboard


# Work function
async def start_work(message: Message):
    global is_working

    is_working = True
    current_time = get_current_time()
    await message.answer(f"Işə fokuslanmaq üçün 30 dəqiqə {current_time}")

    while is_working:
        await asyncio.sleep(10)  # 30 minutes working
        if not is_working:
            break

        await message.answer("Get dincəl")
        await asyncio.sleep(5)
        if not is_working:
            break
        await message.answer("İşə qayıtmaq vaxtıdır")

    await message.answer("Proqram dayandırıldı.")


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(FIRST_MESSAGE, reply_markup=get_main_keyboard())


@dp.callback_query(lambda c: c.data == "start_work")
async def start_work_callback(callback: types.CallbackQuery):
    await start_work(callback.message)


@dp.callback_query(lambda c: c.data == "stop_work")
async def stop_work_callback(callback: types.CallbackQuery):
    global is_working
    if is_working:
        is_working = False
        await callback.message.answer("İş prosesi dayandırıldı.")
    else:
        await callback.message.answer("Heç bir iş prosesi aktiv deyil.")


@dp.callback_query(lambda c: c.data == "show_time")
async def show_time_callback(callback: types.CallbackQuery):
    now_time = get_current_time()
    await callback.message.answer(f"Current time: {now_time}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program dayandırıldı")
