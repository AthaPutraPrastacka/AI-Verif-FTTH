# modules/table_extractor.py

import cv2
import pytesseract
from PIL import Image
import fitz  # Ini adalah PyMuPDF
import os
import re

# PENTING: Jika Tesseract tidak ada di 'path' sistem Anda, Anda harus
# menunjukkan lokasinya secara manual. Contoh untuk Windows:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_image(image_path: str) -> str:
    """Fungsi pembantu untuk melakukan OCR pada sebuah file gambar."""
    img = cv2.imread(image_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Nilai threshold (150) mungkin perlu disesuaikan tergantung kualitas gambar
    _, binary_img = cv2.threshold(gray_img, 150, 255, cv2.THRESH_BINARY)
    raw_text = pytesseract.image_to_string(binary_img, lang='ind')
    return raw_text

def extract_data_from_document(doc_path: str) -> dict:
    """
    Mengekstrak data dari dokumen (bisa gambar atau PDF), lalu mem-parsingnya
    menjadi data terstruktur menggunakan Regex.
    """
    print(f"[INFO] Memulai ekstraksi dari dokumen: {doc_path}")
    raw_text = ""
    
    try:
        # Cek tipe file berdasarkan ekstensinya
        if doc_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print("[INFO] Dokumen terdeteksi sebagai gambar. Menggunakan OCR...")
            raw_text = ocr_image(doc_path)
            
        elif doc_path.lower().endswith('.pdf'):
            print("[INFO] Dokumen terdeteksi sebagai PDF.")
            # Buka file PDF
            doc = fitz.open(doc_path)
            full_text_from_pdf = ""
            
            # Proses setiap halaman
            for i, page in enumerate(doc):
                print(f"[INFO] Memproses halaman PDF ke-{i+1}...")
                # 1. Coba ekstrak teks digital langsung (untuk PDF berbasis teks)
                text_from_page = page.get_text("text")
                
                # 2. Jika teks digital kosong, anggap sebagai gambar dan gunakan OCR
                if not text_from_page.strip():
                    print(f"[INFO] Halaman {i+1} tidak memiliki teks digital, melakukan OCR...")
                    # Ubah halaman PDF menjadi gambar
                    pix = page.get_pixmap()
                    temp_image_path = f"output/temp_page_{i+1}.png"
                    pix.save(temp_image_path)
                    
                    # Lakukan OCR pada gambar halaman
                    text_from_page = ocr_image(temp_image_path)
                    os.remove(temp_image_path) # Hapus gambar sementara setelah selesai
                else:
                    print(f"[INFO] Halaman {i+1} berhasil diekstrak sebagai teks digital.")

                full_text_from_pdf += text_from_page + "\n"
            
            raw_text = full_text_from_pdf
            doc.close()

        else:
            print(f"[ERROR] Format file tidak didukung: {doc_path}")
            return None

        # --- Bagian Parsing (Versi Baru dengan Regex) ---
        print("\n[INFO] Memulai parsing cerdas menggunakan Regex...")
        
        # Alih-alih list, kita akan simpan dalam dictionary agar lebih terstruktur
        extracted_data = {}

        # Pola Regex 1: Mencari jumlah pembayaran
        # r"" -> Tanda bahwa ini adalah string Regex
        # Jumlah: -> Mencari teks "Jumlah: "
        # ( ... ) -> Ini adalah "capturing group", bagian yang ingin kita ambil nilainya
        # Rp ? -> Mencari "Rp" diikuti spasi opsional (?)
        # [\d.,]+ -> Mencari satu atau lebih karakter (\d)igit, titik, atau koma
        pola_jumlah = re.search(r"Jumlah: (Rp ?[\d.,]+)", raw_text, re.IGNORECASE)
        if pola_jumlah:
            # pola_jumlah.group(1) hanya berisi capturing group -> "Rp 500.000"
            extracted_data['jumlah_pembayaran'] = pola_jumlah.group(1)

        # Pola Regex 2: Mencari tanggal
        pola_tanggal = re.search(r"Tanggal: (.*)", raw_text, re.IGNORECASE)
        if pola_tanggal:
            # (.*) -> Pola sederhana: ambil semua karakter ( . ) sebanyak-banyaknya ( * )
            # .strip() untuk menghapus spasi yang tidak perlu
            extracted_data['tanggal_dokumen'] = pola_tanggal.group(1).strip()
            
        # Pola Regex 3: Mencari nama dari daftar hadir
        pola_nama = re.search(r"Nama: (.*)", raw_text, re.IGNORECASE)
        if pola_nama:
            # Kita bisa gunakan pola yang sama untuk nama
            nama_ditemukan = pola_nama.group(1).strip()
            # Cek jika namanya hanya garis bawah, kita anggap kosong
            if "___" in nama_ditemukan:
                extracted_data['nama_peserta'] = "KOSONG"
            else:
                extracted_data['nama_peserta'] = nama_ditemukan

        print("\n--- Hasil Ekstraksi Terstruktur ---")
        print(extracted_data)
        print("----------------------------------\n")
        
        print(f"[INFO] Ekstraksi dokumen selesai.")
        # Kita kembalikan dictionary yang sudah terstruktur
        return extracted_data

    except Exception as e:
        print(f"[ERROR] Gagal memproses dokumen: {e}")
        return None