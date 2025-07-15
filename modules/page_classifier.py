# modules/page_classifier.py
def classify_page_by_keywords(page_text: str) -> str:
    text_upper = page_text.upper()
    if "BERITA ACARA UJI TERIMA" in text_upper and "BAUT" in text_upper: return "BAUT"
    if "CHECKLIST VERIFIKASI BA UJI TERIMA" in text_upper: return "BAUT"
    if "DAFTAR HADIR UJI TERIMA" in text_upper: return "DAFTAR_HADIR"
    if "SURAT PERMINTAAN UJI TERIMA" in text_upper or "PERMOHONAN UJI TERIMA" in text_upper: return "SURAT_PERMINTAAN"
    if "BERITA ACARA" in text_upper and "TEST COMMISSIONING" in text_upper: return "BA_TESTCOMM"
    if "LAPORAN UJI TERIMA" in text_upper: return "LAPORAN_UT"
    if "SK/PENUNJUKAN TEAM UJI TERIMA" in text_upper or "PENUNJUKAN PERSONIL" in text_upper: return "SK_TEAM"
    if "NOTA DINAS PELAKSANAAN UJI TERIMA" in text_upper: return "NOTA_DINAS"
    if "BILL OF QUANTITY" in text_upper or "BOQ UJI TERIMA" in text_upper: return "BOQ_AKHIR"
    if "AS BUILD DRAWING" in text_upper or "SKEMA KABEL" in text_upper or "PETA LOKASI" in text_upper: return "REDLINE_DRAWING"
    if "OTDR REPORT" in text_upper or "DATA PENGUKURAN OPM" in text_upper or "FOTO PENGUKURAN OPM" in text_upper: return "HASIL_CAPTURE"
    if "EVIDENCE PHOTO" in text_upper or "DOKUMENTASI UJI TERIMA" in text_upper or "FOTO KEGIATAN" in text_upper: return "EVIDENCE_PHOTO"
    return "UNKNOWN"