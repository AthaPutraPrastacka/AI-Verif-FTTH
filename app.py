import streamlit as st
import pandas as pd
import os
from main import process_verification # Impor fungsi inti dari main.py

# Konfigurasi halaman
st.set_page_config(page_title="AI Verif Dokumen", layout="wide")

# Judul Aplikasi
st.title("🤖 AI Verifikasi Kelengkapan Dokumen")
st.write("Upload satu file PDF gabungan untuk diperiksa kelengkapannya secara otomatis.")

# 1. WIDGET UPLOAD FILE
uploaded_file = st.file_uploader("Pilih file PDF Anda...", type="pdf")

if uploaded_file is not None:
    # Simpan file yang di-upload sementara agar bisa dibaca
    temp_dir = "temp_uploads"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    temp_pdf_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Jalankan proses verifikasi saat tombol ditekan
    if st.button("Mulai Verifikasi Sekarang"):
        # Tampilkan indikator loading
        with st.spinner("AI sedang bekerja... Menganalisis halaman, memeriksa tanda tangan... Mohon tunggu..."):
            # Panggil fungsi inti dari main.py
            results = process_verification(temp_pdf_path)
        
        st.success("Verifikasi Selesai!")

        # 2. TAMPILKAN HASIL DALAM BENTUK TABEL
        st.subheader("Laporan Hasil Verifikasi")
        
        df_results = pd.DataFrame(results)
        # Ubah nama kolom agar lebih rapi
        df_display = df_results.rename(columns={'no': 'No.','kategori': 'Kategori','char': 'Sub','name': 'Item','status': 'Status','keterangan': 'Keterangan'})
        st.dataframe(df_display) # st.dataframe lebih interaktif dari st.table

        # 3. BUAT DATA UNTUK TOMBOL DOWNLOAD EXCEL
        # Siapkan file Excel dalam format bytes untuk di-download
        output_excel_filename = f"{os.path.splitext(uploaded_file.name)[0]}_Report.xlsx"
        df_excel = df_display[['No.', 'Kategori', 'Sub', 'Item', 'Status', 'Keterangan']]
        
        # Simpan ke memori (BytesIO buffer)
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_excel.to_excel(writer, index=False, sheet_name='Laporan Verifikasi')
        
        excel_data = output.getvalue()

        # WIDGET TOMBOL DOWNLOAD
        st.download_button(
            label="✅ Download Laporan sebagai Excel",
            data=excel_data,
            file_name=output_excel_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # Hapus file sementara setelah selesai
    # os.remove(temp_pdf_path) # Anda bisa aktifkan ini jika sudah production