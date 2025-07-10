    # extract_pages.py

import fitz  # Ini adalah PyMuPDF, library untuk bekerja dengan file PDF
import os    # Ini adalah library standar untuk fungsi sistem operasi, seperti membuat folder

# --- PENGATURAN SCRIPT ---
# Anda bisa dengan mudah mengganti path file PDF atau nama folder output di sini.
PDF_FILE_PATH = "input_documents/BAUT TBN028 Rev_SIGNED.pdf"  # Ganti dengan path file PDF Anda
OUTPUT_FOLDER = "all_pages_output" # Nama folder untuk menyimpan semua hasil gambar
# -------------------------

# 1. PERSIAPAN FOLDER
# Cek apakah folder output sudah ada atau belum
if not os.path.exists(OUTPUT_FOLDER):
    # Jika belum ada, buat folder baru
    os.makedirs(OUTPUT_FOLDER)
    print(f"Folder '{OUTPUT_FOLDER}' berhasil dibuat.")
else:
    print(f"Folder '{OUTPUT_FOLDER}' sudah ada, siap digunakan.")

# 2. PROSES EKSTRAKSI
try:
    # Buka dokumen PDF menggunakan library fitz
    doc = fitz.open(PDF_FILE_PATH)

    print(f"\nMemulai proses ekstraksi {len(doc)} halaman dari file '{os.path.basename(PDF_FILE_PATH)}'...")

    # Loop atau ulangi proses untuk setiap halaman di dalam dokumen
    # `range(len(doc))` akan membuat urutan angka dari 0 hingga (jumlah halaman - 1)
    for i in range(len(doc)):
        # Ambil satu halaman berdasarkan nomor urutnya
        page = doc.load_page(i)
        
        # Ubah halaman menjadi gambar. 
        # DPI (Dots Per Inch) menentukan resolusi/kualitas gambar. 200 adalah nilai yang bagus untuk training.
        pix = page.get_pixmap(dpi=200) 
        
        # Buat nama file yang unik untuk setiap halaman.
        # Contoh: page_001.png, page_002.png, dst.
        output_filename = os.path.join(OUTPUT_FOLDER, f"page_{i+1:03d}.png")
        
        # Simpan gambar ke dalam folder output
        pix.save(output_filename)

    # Setelah selesai, tutup dokumen untuk melepaskan memori
    doc.close()

    print(f"\n✅ Proses Selesai! Semua {len(doc)} halaman telah berhasil disimpan di dalam folder '{OUTPUT_FOLDER}'.")

except Exception as e:
    print(f"\n❌ Terjadi Error: {e}")
    print("Pastikan path file PDF sudah benar dan file tersebut tidak rusak.")