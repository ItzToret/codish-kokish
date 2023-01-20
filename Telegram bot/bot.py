import logging
import asyncio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('LogTag')

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
from stickers import stickers

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

@dp.message_handler(commands=["help"])
async def cmd_start(message: types.Message):
    await message.answer("Список команд")

@dp.message_handler()
async def hello_response(msg:types.Message):
    if 'привет' in msg.text.lower():
        await bot.send_message(msg.from_user.id,f'Здравствуй,{msg.from_user.first_name}!')
    elif 'пока' in msg.text.lower():
            await bot.send_message(msg.from_user.id, f'ну и вали отсюда,{msg.from_user.first_name}!')

@dp.message_handler(content_types=["sticker"])
async def st(msg:types.Message):
    print(msg.sticker)
    await msg.reply("Круть!")
    await bot.send_sticker(msg.from_user.id, sticker=stickers['Like'])


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

