from googletrans import Translator
import PyPDF2

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''

        for page_num in range(pdf_reader.pages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
    return text

def translate_text(text, target_language='tr'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def save_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

# Kullanım örneği
pdf_path = 'ingilizce-yeterlilik-sinav-ornegi.pdf'  # PDF dosyanızın adını ve yolunu belirtin
translated_text = translate_text(pdf_to_text(pdf_path))
save_to_file(translated_text, 'translated_text.txt')
