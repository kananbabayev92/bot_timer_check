# Focus Timer Bot - Documentation

## Overview

Focus Timer Bot is a Telegram bot designed to help users improve productivity by managing work and rest periods effectively. The bot provides inline buttons for starting, stopping, and checking the current time.

## Features

- Start a focused work session.
- Stop the work session at any time.
- Show the current time.
- Inline buttons for easy interaction.
- Uses an asynchronous system for smooth operation.

---

## Installation & Setup

### Prerequisites

Before running the bot, ensure you have:

- Python 3.8 or higher installed.
- `aiogram` library installed (`pip install aiogram`).
- A Telegram Bot Token (obtained from @BotFather).

### Clone the Repository

```bash
$ git clone https://github.com/kananbabayev92/focus-timer-bot.git
$ cd focus-timer-bot
```

### Install Dependencies

```bash
$ pip install -r requirements.txt
```

### Configure Environment

Create a `telegram_token.py` file and define your bot token:

```python
BOT_TOKEN = "your_telegram_bot_token"
FIRST_MESSAGE = "Welcome to Focus Timer Bot! Use the buttons below to start."
```

### Run the Bot

```bash
$ python main.py
```

---

## Usage

### Start Command

Users can start the bot by sending:

```bash
/start
```

This command displays a message along with inline buttons:

- **Start Work**: Begins a focus session.
- **Stop Work**: Stops the ongoing session.
- **Show Time**: Displays the current time.

### Button Actions

- **Start Work** (`start_work`): Initiates a work session where reminders are sent.
- **Stop Work** (`stop_work`): Stops the session and prevents further messages.
- **Show Time** (`show_time`): Displays the current system time.

---

## Code Explanation

### Importing Libraries

```python
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from telegram_token import BOT_TOKEN, FIRST_MESSAGE
from datetime import datetime
```

- `aiogram`: Handles Telegram bot functionality.
- `asyncio`: Manages asynchronous operations.
- `datetime`: Retrieves current time.

### Initializing the Bot

```python
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()
is_working = False
```

- `bot`: Connects to Telegram using the provided token.
- `dp`: Dispatcher for handling events.
- `is_working`: A global variable to track if the bot is running a session.
- `parse_mode="HTML"`: Allows formatting messages with HTML tags.

### Inline Keyboard

```python
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Start Work", callback_data="start_work")],
        [InlineKeyboardButton(text="Stop Work", callback_data="stop_work")],
        [InlineKeyboardButton(text="Show Time", callback_data="show_time")]
    ])
    return keyboard
```

Creates inline buttons for interaction.

### Work Session Logic

```python
async def start_work(callback: types.CallbackQuery):
    global is_working
    is_working = True
    await callback.message.answer("Work session started!")
    while is_working:
        await asyncio.sleep(10)
        await callback.message.answer("Take a break!")
        await asyncio.sleep(5)
        await callback.message.answer("Back to work!")
```

- Runs an asynchronous work session cycle.
- Sends periodic reminders for work and rest.

### Stop Work Command

```python
@dp.callback_query(lambda c: c.data == "stop_work")
async def stop_work_callback(callback: types.CallbackQuery):
    global is_working
    is_working = False
    await callback.message.answer("Work session stopped.")
```

- Stops the ongoing work session.

### Show Current Time

```python
@dp.callback_query(lambda c: c.data == "show_time")
async def show_time_callback(callback: types.CallbackQuery):
    now_time = datetime.now().strftime("%H:%M:%S")
    await callback.message.answer(f"Current time: {now_time}")
```

- Retrieves and displays the current time.

### Start Command Handler

```python
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(FIRST_MESSAGE, reply_markup=get_main_keyboard())
```

- Sends a welcome message with inline buttons.

### Bot Startup

```python
async def main():
    await dp.start_polling(bot)
```

Runs the bot and starts listening for events.

---

## Error Handling

```python
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
```

Handles manual termination (`CTRL+C`).

---

## Conclusion

This bot helps users manage their work time effectively by sending reminders. Future improvements may include:

- Customizable work/rest durations.
- User-specific session tracking.
- Data storage for analytics.

For support or suggestions, contact kananbabayev92 on GitHub.

