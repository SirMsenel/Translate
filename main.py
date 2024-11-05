import fitz  # PyMuPDF
from deep_translator import GoogleTranslator
from fpdf import FPDF
import os

# Kullanıcıdan giriş dosyasının yolunu ve çıktı dosyasının ismini alma
input_pdf = input("Lütfen çevirmek istediğiniz PDF dosyasının tam yolunu girin (örneğin: /Users/mehmetsenel/Downloads/ingilizce_yeterlilik.pdf): ")
output_filename = input("Lütfen çıktı PDF dosyasının ismini girin (örneğin: cevrilmis_dosya.pdf): ")

def translate_text(text):
    """ İngilizce metni Türkçeye çevirir """
    try:
        return GoogleTranslator(source='en', target='tr').translate(text)
    except Exception as e:
        print(f"Çeviri sırasında bir hata oluştu: {e}")
        return text  # Hata olursa orijinal metni döndür

# PDF'deki metni al ve çevir
def translate_pdf(input_pdf, output_pdf):
    if not os.path.exists(input_pdf):
        print(f"Hata: '{input_pdf}' dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")
        return
    
    try:
        # Orijinal PDF'i aç
        doc = fitz.open(input_pdf)
        pdf = FPDF()
        
        # Tüm sayfalardan metni çıkar ve çevir
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")  # Sayfadaki metni al
            translated_text = translate_text(text)  # Metni Türkçeye çevir

            # Yeni sayfa ekle ve çeviriyi yaz
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            # UTF-8 karakter setini desteklemek için
            pdf.multi_cell(0, 10, translated_text.encode('latin-1', 'replace').decode('latin-1'))
            
            # Orijinal grafikleri eklemek için PyMuPDF'i kullanın
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                img_name = f"temp_image_{page_num}_{img_index}.png"
                
                # Geçici olarak resmi kaydedin
                with open(img_name, "wb") as img_file:
                    img_file.write(image_bytes)
                
                # Görüntüyü PDF sayfasına ekleyin
                pdf.image(img_name, x=10, y=None, w=100)
                
                # Geçici dosyayı silin
                os.remove(img_name)

        # Çıktıyı kaydet
        pdf.output(output_pdf)
        print(f"Çeviri işlemi tamamlandı. Yeni dosya '{output_pdf}' olarak kaydedildi.")
    
    except Exception as e:
        print(f"PDF işleme sırasında bir hata oluştu: {e}")

# Fonksiyonu çağırarak işlemi başlat
translate_pdf(input_pdf, output_filename)
