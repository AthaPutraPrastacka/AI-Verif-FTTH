# app.py
import streamlit as st
import pandas as pd
import os
import io
from main import process_verification
from modules.checklist_templates import ALL_TEMPLATES # Impor template

st.set_page_config(layout="wide", page_title="AI Document Verifier", page_icon="🤖")

with st.sidebar:
    st.title("🤖 AI Document Verifier")
    st.info("Aplikasi ini dibuat untuk tugas PKL dengan menggunakan Streamlit, OpenCV, dan TensorFlow.")
    st.divider()

st.header("Unggah dan Verifikasi Dokumen Proyek")

# --- PEMILIHAN TEMPLATE CHECKLIST (BARU) ---
st.subheader("1. Pilih Jenis Verifikasi")
template_choice = st.selectbox(
    "Pilih jenis checklist yang akan digunakan:",
    options=list(ALL_TEMPLATES.keys())
)

# --- File Uploader ---
st.subheader("2. Unggah Dokumen PDF")
uploaded_file = st.file_uploader(
    "Pilih file PDF proyek Anda di sini:",
    type="pdf",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    if st.button("🚀 Mulai Verifikasi Sekarang!", type="primary", use_container_width=True):
        temp_dir = "temp_uploads"
        if not os.path.exists(temp_dir): os.makedirs(temp_dir)
        temp_pdf_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_pdf_path, "wb") as f: f.write(uploaded_file.getbuffer())

        with st.spinner('⏳ AI sedang bekerja... Menganalisis dokumen...'):
            chosen_checklist = ALL_TEMPLATES[template_choice] # Ambil checklist yang dipilih
            results, score, level = process_verification(temp_pdf_path, chosen_checklist) # Kirim ke backend

        st.success("✅ Verifikasi Selesai!")
        st.divider()

        st.subheader("Ringkasan Hasil Analisis")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Skor Kepatuhan Dokumen", value=f"{score:.2f}%", delta=level)
        with col2:
            st.progress(int(score))
            if level == "SANGAT BAIK": st.success("Dokumen sangat lengkap dan sesuai standar.")
            elif level == "BAIK": st.info("Dokumen sudah baik, ada beberapa item minor yang bisa diperiksa.")
            else: st.warning("Dokumen kurang lengkap atau ditemukan masalah. Perlu review manual.")
        
        st.subheader("Laporan Detail Kelengkapan")
        if results:
            df_results = pd.DataFrame(results)
            df_display = df_results.rename(columns={'no': 'No.', 'kategori': 'Kategori', 'char': 'Sub', 'name': 'Item', 'status': 'Status', 'keterangan': 'Keterangan'})
            st.dataframe(df_display.drop(columns=['id']), use_container_width=True)

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_display.drop(columns=['id']).to_excel(writer, index=False, sheet_name='LaporanVerifikasi')
            
            st.download_button(
                label="📥 Download Laporan Lengkap sebagai Excel",
                data=output.getvalue(),
                file_name=f"Laporan_{os.path.splitext(uploaded_file.name)[0]}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        os.remove(temp_pdf_path)