import logging
import asyncio
import pyttsx3
import os
from pathlib import Path
import pdfminer.high_level
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot

import aspose.words as aw

from docx2pdf import convert
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
import requests
import speech_recognition as sr
import subprocess
import datetime

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import File
import soundfile as sf

import keyboard
from keyboard.dop import reply_keyboard

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('LogTag')

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor

from config.config import TOKEN
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot,storage=storage)
logfile = str(datetime.date.today()) + '.log' # формируем имя лог-файла
class Form(StatesGroup):
    trt = State()
    #trt1 = State()
    #trt2 = State()
    trt3 = State()

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привет!")

@dp.message_handler(commands="ttv")
async def cmd_ttv0(message: types.Message):
    await message.reply('Выберите нужную функцию на клавиатуре, в том случае если вы ошиблись при выборе, напишите: "Отмена" ', reply_markup=reply_keyboard)


@dp.message_handler(content_types=["text"], text='Сообщение в голос')
async def cmd_ttv(message: types.Message):
    await bot.send_message(message.from_user.id,'Для начала отправьте ваш текст')
    await Form.trt.set()

@dp.message_handler(content_types=["text"], text='Файл docx/pdf/txt в голос')
async def cmd_ttv3(message: types.Message):
    await bot.send_message(message.from_user.id,'Для начала отправьте ваш docx/pdf/txt файл')
    await Form.trt3.set()

@dp.message_handler(state='*', commands='Отмена')
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Функция отменена', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=Form.trt)
async def process_age(message: types.Message, state: FSMContext):
    data = message.text
    engine = pyttsx3.init()
    engine.save_to_file(data, 'test.mp3')
    engine.runAndWait()
    await message.reply_document(open('test.mp3', 'rb'))
    await state.finish()

@dp.message_handler(state=Form.trt3,content_types=types.ContentType.DOCUMENT)
async def process_age(message: types.Document, state: FSMContext):
    await message.reply(text='файл получен, конвертируем')
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "docx2txt.docx")
    doc = aw.Document("docx2txt.docx")
    doc.save("docx2txt.txt")
    with open('docx2txt.txt') as old, open('docx2txtnew.txt', 'w') as new:
        lines = old.readlines()
        new.writelines(lines[2:-1])
    file = open('docx2txtnew.txt', 'r', encoding="utf-8")
    text = file.read()
    engine = pyttsx3.init()
    engine.save_to_file(text, 'docx2txtnew.mp3')
    engine.runAndWait()
    await message.reply_document(open('docx2txtnew.mp3', 'rb'))
    file.close()
    await state.finish()


@dp.message_handler(commands=["help"])
async def cmd_start(message: types.Message):
    await message.answer("/start - Запускает бота в первый раз(не думаю что она вам ещё понадобиться) \n"+
                         "/help - Показывает список команд \n"+
                         "/ttv - Конвертирует файлы и текст в голосовые сообщения, в случае неправильного выбора пропишите: 'Отмена' ")

async def handle_file(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)
    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")

@dp.message_handler(content_types=['voice'])
async def voice_message_handler(message: types.Message):

    #Ниже пытаемся вычленить имя файла, да и вообще берем данные с мессаги
    #file_info = bot.get_file(message.voice.file_id)
    path = "/voices" # Вот тут-то и полный путь до файла (например: voice/file_2.oga)
    voice = await message.voice.get_file()
    name="one"
    await handle_file(file=voice, file_name=f"{name}.ogg", path=path)

    data, samplerate = sf.read('/voices/one.ogg')
    sf.write('two.wav', data, samplerate)
    sound = "two.wav"
    r = sr.Recognizer()
    with sr.AudioFile(sound) as source:
        r.adjust_for_ambient_noise(source)
        print('Convert.')
        audio = r.listen(source)
        query = r.recognize_google(audio, language='ru-RU')
        await bot.send_message(message.from_user.id,query)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

