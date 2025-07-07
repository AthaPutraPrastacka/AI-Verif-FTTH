def classify_page_by_keywords(page_text: str) -> str:
    """
    Mengklasifikasikan halaman HANYA berdasarkan kata kunci teks.
    Versi ini telah diperkaya dengan kata kunci dari berbagai dokumen.
    """
    text_upper = page_text.upper()

    # Urutan ini sangat penting untuk menghindari salah klasifikasi
    
    # Kategori dengan keyword paling unik dan pasti
    if "BERITA ACARA" in text_upper and "TEST COMMISSIONING" in text_upper:
        return "BA_TESTCOMM"
    if "BERITA ACARA PERIZINAN PEMBANGUNAN" in text_upper:
        return "BA_PERIZINAN" # Dari dokumen BA-PRELIM
    if "BERITA ACARA KESEPAKATAN NEGOSIASI" in text_upper:
        return "BA_NEGOSIASI" # Dari dokumen BA-PRELIM
    if "BERITA ACARA PERSETUJUAN PRELIMINARY" in text_upper:
        return "BA_PRELIMINARY" # Dari dokumen BA-PRELIM
    if "SURAT PERMINTAAN UJI TERIMA" in text_upper or "PERMOHONAN UJI TERIMA" in text_upper:
        return "SURAT_PERMINTAAN"
    if "BERITA ACARA UJI TERIMA" in text_upper and "BAUT" in text_upper:
        return "BAUT"
    if "SK/PENUNJUKAN TEAM UJI TERIMA" in text_upper or "PENUNJUKAN PERSONIL TIM UJI TERIMA" in text_upper:
        return "SK_TEAM"
    if "NOTA DINAS" in text_upper and "PEDOMAN KELENGKAPAN" in text_upper: # Dari Pedoman.pdf
        return "NOTA_DINAS"
    if "BILL OF QUANTITY" in text_upper or "BOQ UJI TERIMA" in text_upper:
        return "BOQ_AKHIR"

    # Kategori yang lebih umum atau bisa jadi bagian dari dokumen lain
    if "LAPORAN UJI TERIMA" in text_upper:
        return "LAPORAN_UT"
    if "OTDR REPORT" in text_upper:
        return "HASIL_CAPTURE" # Laporan OTDR kita klasifikasikan sebagai Hasil Capture
    if "DATA PENGUKURAN OPM" in text_upper:
        return "HASIL_CAPTURE" # Form OPM juga kita anggap sebagai Hasil Capture
        
    # Kategori gambar yang mungkin punya judul teks
    if "AS BUILD DRAWING" in text_upper or "SINGLE LINE DIAGRAM" in text_upper or "SKEMA KABEL" in text_upper:
        return "REDLINE_DRAWING"
    if "EVIDENCE PHOTO" in text_upper or "EVIDENT HASIL UKUR" in text_upper or "DOKUMENTASI UJI TERIMA" in text_upper:
        return "EVIDENCE_PHOTO"
        
    return "UNKNOWN"