from docx2pdf import convert
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io

convert("12345.docx")
convert("12345.docx", "12345.pdf")

resource_manager = PDFResourceManager()
fake_file_handle = io.StringIO()
converter = TextConverter(resource_manager, fake_file_handle)
page_interpreter = PDFPageInterpreter(resource_manager, converter)

with open('12345.pdf', 'rb') as fh:

    for page in PDFPage.get_pages(fh,
                                  caching=True,
                                  check_extractable=True):
        page_interpreter.process_page(page)

    text = fake_file_handle.getvalue()

# close open handles
converter.close()
fake_file_handle.close()

print(text, file=open("12345.txt","a"))

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
