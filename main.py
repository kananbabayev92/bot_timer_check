import asyncio
import os
from aiogram import Bot, Dispatcher, types
from keyboard import get_main_keyboard
from message import FIRST_MESSAGE
from datetime import datetime
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message

# Initialize bot and dispatcher
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()  # ✅ Aiogram 3 requires passing the bot instance

is_working = False

# State for Notes
class NoteState(StatesGroup):
    waiting_for_note = State()

# User notes storage
user_notes = {}

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")


# Work function
async def start_work(message: Message):
    global is_working
    is_working = True
    current_time = get_current_time()
    await message.answer(f"Işə fokuslanmaq üçün 30 dəqiqə {current_time}")

    while is_working:
        await asyncio.sleep(1800)  # 30 minutes working
        if not is_working:
            break

        await message.answer("Get dincəl")
        await asyncio.sleep(300)
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

# ✅ Handling "Save Note" button
@dp.callback_query(lambda query: query.data == "save_note")
async def save_note_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Please send your note:")
    await state.set_state(NoteState.waiting_for_note)

# ✅ Save the note when user sends a message
@dp.message(NoteState.waiting_for_note)
async def save_user_note(message: Message, state: FSMContext):
    user_id = message.from_user.id
    note_text = message.text

    # Save note
    if user_id not in user_notes:
        user_notes[user_id] = []
    user_notes[user_id].append(note_text)

    await message.answer("✅ Your note has been saved!")
    await state.clear()  # Clear state after saving

# ✅ Handle "Show Note" button (Fixing callback query usage)
@dp.callback_query(lambda c: c.data == "show_note")
async def show_notes_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id in user_notes and user_notes[user_id]:
        show_note = "\n".join(f"📌 {note}" for note in user_notes[user_id])
        await callback.message.answer(f"📝 Your Notes:\n\n{show_note}")
    else:
        await callback.message.answer("You have no saved notes.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
