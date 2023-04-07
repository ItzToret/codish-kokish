import logging
import asyncio
import pyttsx3
import os
from pathlib import Path

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot

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
    trt1 = State()
    trt2 = State()
    trt3 = State()

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

@dp.message_handler(commands="ttv")
async def cmd_ttv0(message: types.Message):
    await message.reply('Выберите нужную функцию на клавиатуре', reply_markup=reply_keyboard)


@dp.message_handler(content_types=["text"], text='Сообщение в голос')
async def cmd_ttv(message: types.Message):
    await bot.send_message(message.from_user.id,'Для начала отправьте ваш текст')
    await Form.trt.set()
@dp.message_handler(content_types=["text"], text='Файл txt в голос')
async def cmd_ttv1(message: types.Message):
    await bot.send_message(message.from_user.id,'Для начала отправьте ваш txt файл')
    await Form.trt1.set()
@dp.message_handler(content_types=["text"], text='Файл pdf в голос')
async def cmd_ttv2(message: types.Message):
    await bot.send_message(message.from_user.id,'Для начала отправьте ваш pdf файл')
    await Form.trt2.set()
@dp.message_handler(content_types=["text"], text='Файл docx в голос')
async def cmd_ttv3(message: types.Message):
    await bot.send_message(message.from_user.id,'Для начала отправьте ваш docx файл')
    await Form.trt3.set()

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
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
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=Form.trt)
async def process_age(message: types.Message, state: FSMContext):
    data = message.text
    engine = pyttsx3.init()
    engine.save_to_file(data, 'test.mp3')
    engine.runAndWait()
    await message.reply_document(open('test.mp3', 'rb'))
    await state.finish()

@dp.message_handler(state=Form.trt1,content_types=types.ContentType.DOCUMENT)
async def process_age(message: types.Document, state: FSMContext):
    await message.reply(text='файл получен, начинаю поиск ошибок...')
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "txt.rtf")
    file = open('txt.rtf', 'r', encoding="utf-8")
    text = file.read()
    file.close()
    engine = pyttsx3.init()
    engine.save_to_file(text, 'txtmp3.mp3')
    engine.runAndWait()
    await message.reply_document(open('txtmp3.mp3', 'rb'))
    await state.finish()
@dp.message_handler(state=Form.trt2,content_types=types.ContentType.DOCUMENT)
async def process_age(message: types.Document, state: FSMContext):
    await message.reply(text='файл получен, начинаю поиск ошибок...')
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "pdf2txt.pdf")
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open('pdf2txt.pdf', 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    file = open('pdf2txt.txt', 'r', encoding="utf-8")
    text = file.read()
    file.close()
    engine = pyttsx3.init()
    engine.save_to_file(text, 'pdf2txt.mp3')
    engine.runAndWait()
    await message.reply_document(open('pdf2txt.mp3', 'rb'))
    await state.finish()
@dp.message_handler(state=Form.trt3,content_types=types.ContentType.DOCUMENT)
async def process_age(message: types.Document, state: FSMContext):
    await message.reply(text='файл получен, начинаю поиск ошибок...')
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "docx2txt.docx")
    convert("docx2txt.docx")
    convert("docx2txt.docx", "docx2txt.pdf")
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open('docx2txt.pdf', 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    file = open('docx2txt.txt', 'r', encoding="utf-8")
    text = file.read()
    file.close()
    engine = pyttsx3.init()
    engine.save_to_file(text, 'docx2txt.mp3')
    engine.runAndWait()
    await message.reply_document(open('docx2txt.mp3', 'rb'))
    await state.finish()

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def fileHandle(message: types.Document):
    await message.reply(text='файл получен, начинаю поиск ошибок...')
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "opdf.pdf")

    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open('docx2txt.pdf', 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    file = open('opdf.txt', 'r', encoding="utf-8")
    text = file.read()
    file.close()
    engine = pyttsx3.init()
    engine.save_to_file(text, 'testpdf.mp3')
    engine.runAndWait()
    await message.reply_document(open('testpdf.mp3', 'rb'))


@dp.message_handler(commands=["help"])
async def cmd_start(message: types.Message):
    await message.answer("Список команд")

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

