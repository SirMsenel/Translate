import fitz  # PyMuPDF
from deep_translator import GoogleTranslator
from fpdf import FPDF
import os

# Kullanıcıdan giriş dosyasının yolunu alma
input_pdf = input("Lütfen çevirmek istediğiniz PDF dosyasının tam yolunu girin: ")

# Çıktı klasörü ve dosya adını ayarlama
output_dir = "/Users/mehmetsenel/Desktop/translate/deneme-sonuç"
if not os.path.exists(output_dir):  # Çıktı klasörü yoksa oluştur
    os.makedirs(output_dir)

# Kullanıcıdan çıktı dosyasının ismini alma
output_filename = input("Lütfen çıktı PDF dosyasının ismini girin (örneğin: 'sonuc.pdf'): ")

# Çıktı dosyasının tam yolunu oluşturma
output_pdf = os.path.join(output_dir, output_filename)

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

        # Sayfa boyutunu artırma
        pdf.add_page(format='letter')  # Sayfa boyutunu letter (A4'den biraz büyük) yapar
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf')  # Fontu ekliyoruz
        pdf.set_font('DejaVu', size=8)  # Font boyutunu küçültme

        # Sayfa kenarlarını küçültme
        pdf.set_left_margin(2)
        pdf.set_right_margin(2)

        # Sayfa genişliğini almak
        page_width = pdf.w - 2 * pdf.l_margin  # Sayfa genişliği - sol ve sağ kenar boşluğu

        # Tüm sayfalardan metni çıkar ve çevir
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")  # Sayfadaki metni al
            translated_text = translate_text(text)  # Metni Türkçeye çevir

            # Metnin genişliğini kontrol et
            pdf.set_xy(pdf.l_margin, pdf.get_y())  # Başlangıç noktasına gel
            pdf.multi_cell(page_width, 10, translated_text)  # Sayfa genişliğine göre metni kırma

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
translate_pdf(input_pdf, output_pdf)
