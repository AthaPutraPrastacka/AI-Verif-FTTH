import streamlit as st
import pandas as pd
import os
import io
from main import process_verification # Impor fungsi inti dari main.py

# Konfigurasi halaman
st.set_page_config(page_title="AI Verif Dokumen", layout="wide")

# Judul Aplikasi
st.title("AI Verifikasi Kelengkapan Dokumen")
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
    # Di dalam file app.py

if st.button("Mulai Verifikasi Sekarang", type="primary"):
    with st.spinner('AI sedang bekerja... Menganalisis dokumen...'):
        # Panggil fungsi inti yang sekarang mengembalikan 3 nilai
        results, score, level = process_verification(temp_pdf_path)

    st.success("Verifikasi Selesai!")

    # --- Tampilkan Skor (Bagian Baru) ---
    st.header(f" Skor Integritas Dokumen: {score:.2f}%")
    
    # Beri warna berdasarkan level
    if level == "SANGAT TINGGI":
        st.info(f"**Level Kepatuhan: {level}**")
    elif level == "BAIK":
        st.success(f"**Level Kepatuhan: {level}**")
    elif level == "PERLU PERHATIAN":
        st.warning(f"**Level Kepatuhan: {level}**")
    else:
        st.error(f"**Level Kepatuhan: {level}**")

    st.progress(int(score))

    # --- Tampilkan Laporan Detail (tidak berubah) ---
    st.header("Laporan Hasil Verifikasi Detail")
    if results:
        df_results = pd.DataFrame(results)
        df_display = df_results.rename(columns={'no': 'No.', 'kategori': 'Kategori', 'char': 'Sub', 'name': 'Item', 'status': 'Status', 'keterangan': 'Keterangan'})
        st.dataframe(df_display.drop(columns=['id']), use_container_width=True) # Sembunyikan kolom 'id'

        # Tombol Download Excel (tidak berubah)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_display.to_excel(writer, index=False, sheet_name='LaporanVerifikasi')
        
        st.download_button(
            label="Download Laporan sebagai Excel",
            data=output.getvalue(),
            file_name=f"Laporan_{os.path.splitext(uploaded_file.name)[0]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("Tidak ada hasil yang dapat ditampilkan.")
    
    os.remove(temp_pdf_path)