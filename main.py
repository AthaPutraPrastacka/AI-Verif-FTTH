# main.py
import os
import fitz
import pandas as pd
from collections import defaultdict
from modules.signature_detector import detect_signature
from modules.page_classifier import classify_page_by_keywords
from modules.dl_classifier import predict_page_class

def convert_pdf_page_to_image(doc: fitz.Document, page_num: int, output_folder: str = "output"):
    try:
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        image_path = os.path.join(output_folder, f"temp_page_{page_num+1}_for_check.png")
        pix.save(image_path)
        return image_path
    except Exception as e:
        print(f"ERROR: Gagal convert page {page_num+1}: {e}")
        return None

def process_verification(pdf_path: str) -> list:
    print("\n" + "="*50 + "\n   MEMULAI ANALISIS PDF (MODE HYBRID FINAL)  \n" + "="*50)
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"FATAL ERROR: Gagal membuka file PDF: {e}")
        return []

    document_map = defaultdict(list)
    print("\n--- TAHAP 1: KLASIFIKASI HALAMAN ---\n")
    for i in range(len(doc)):
        page_num = i + 1
        page = doc.load_page(i)
        text = page.get_text("text")

        # Prioritas 1: Coba klasifikasi dengan kata kunci yang pasti
        doc_type_id = classify_page_by_keywords(text)
        
        # Prioritas 2: Jika tidak ada kata kunci, baru gunakan model Deep Learning
        if doc_type_id == "UNKNOWN":
            print(f"Halaman {page_num:<3} -> Keyword tidak cocok, menggunakan Deep Learning...")
            image_path = convert_pdf_page_to_image(doc, i)
            if image_path:
                prediction_result = predict_page_class(image_path)
                doc_type_id = prediction_result.split('_', 1)[-1]
            else:
                doc_type_id = "ERROR"
        
        if doc_type_id not in ['UNKNOWN', 'ERROR']:
            document_map[doc_type_id].append(page_num)
        
        print(f"Halaman {page_num:<3} -> Dikenali sebagai: {doc_type_id}")
    print("\n--- Klasifikasi halaman selesai. ---\n")

    main_checklist = [
        {'no': '1', 'kategori': 'BA Uji Terima dan Laporan Uji Terima', 'sub_items': [{'id': 'BAUT', 'char': 'A', 'name': 'BAUT', 'requires_signature': True}, {'id': 'LAPORAN_UT', 'char': 'B', 'name': 'Laporan UT', 'requires_signature': True}]},
        {'no': '2', 'kategori': 'Permintaan Uji Terima Mitra', 'sub_items': [{'id': 'SURAT_PERMINTAAN', 'char': 'A', 'name': 'Surat Permintaan Uji Terima dari Mitra', 'requires_signature': True}, {'id': 'BA_TESTCOMM', 'char': 'B', 'name': 'BA Test Commissioning dan Lampirannya', 'requires_signature': True}]},
        {'no': '3', 'kategori': 'Pelaksanaan Uji Terima', 'sub_items': [{'id': 'SK_TEAM', 'char': 'A', 'name': 'SK/Penunjukan Team Uji Terima', 'requires_signature': False}, {'id': 'NOTA_DINAS', 'char': 'B', 'name': 'Nota Dinas Pelaksanaan Uji Terima', 'requires_signature': False}]},
        {'no': '4', 'kategori': 'Lampiran Uji Terima', 'sub_items': [{'id': 'REDLINE_DRAWING', 'char': 'A', 'name': 'Red line drawing', 'requires_signature': False}, {'id': 'BOQ_AKHIR', 'char': 'B', 'name': 'BoQ akhir', 'requires_signature': False}, {'id': 'HASIL_CAPTURE', 'char': 'C', 'name': 'Hasil Capture', 'requires_signature': False}, {'id': 'EVIDENCE_PHOTO', 'char': 'D', 'name': 'Evidence Photo', 'requires_signature': False}]}
    ]
    
    final_results = []
    print("\n--- TAHAP 2: VERIFIKASI CHECKLIST ---\n")
    for kategori_item in main_checklist:
        for sub_item in kategori_item['sub_items']:
            status, keterangan = ("TIDAK OK", "TIDAK ADA")
            if sub_item['id'] in document_map:
                if sub_item['requires_signature']:
                    page_to_check_num = document_map[sub_item['id']][-1] - 1
                    image_path_for_signature = convert_pdf_page_to_image(doc, page_to_check_num)
                    if image_path_for_signature and detect_signature(image_path_for_signature):
                        status, keterangan = ("OK", "ADA, LENGKAP TANDA TANGAN")
                    else:
                        status, keterangan = ("TIDAK OK", "ADA, TANDA TANGAN TIDAK LENGKAP")
                else:
                    status, keterangan = ("OK", "ADA")
            final_results.append({'no': kategori_item['no'], 'kategori': kategori_item['kategori'], 'char': sub_item['char'], 'name': sub_item['name'], 'status': status, 'keterangan': keterangan})
    doc.close()
    print("\n--- Proses verifikasi selesai. ---")
    return final_results