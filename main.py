# main.py
import os
import fitz
from collections import defaultdict
from modules.signature_detector import detect_signature
from modules.page_classifier import classify_page_by_keywords
from modules.dl_classifier import predict_page_class

# Fungsi helper tidak berubah
def convert_pdf_page_to_image(doc, page_num, output_folder="output"):
    try:
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        image_path = os.path.join(output_folder, f"temp_page_{page_num+1}.png")
        pix.save(image_path)
        return image_path
    except Exception as e:
        print(f"ERROR: Gagal convert page {page_num+1}: {e}")
        return None

# --- FUNGSI INTI DENGAN LOGIKA FINAL YANG DISEMPURNAKAN ---
def process_verification(pdf_path: str, selected_checklist: list) -> tuple:
    print("\n" + "="*50 + "\n   MEMULAI ANALISIS PDF (MODE HYBRID V3)  \n" + "="*50)
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        return ([], 0.0, "ERROR")

    document_map = defaultdict(list)
    print("\n--- TAHAP 1: KLASIFIKASI HALAMAN ---\n")
    for i in range(len(doc)):
        page_num = i + 1
        page = doc.load_page(i)
        text = page.get_text("text")

        # Prioritas 1: Coba klasifikasi dengan kata kunci yang pasti
        keyword_result = classify_page_by_keywords(text)
        
        # Prioritas 2: Selalu jalankan prediksi visual untuk perbandingan
        image_path = convert_pdf_page_to_image(doc, i)
        if not image_path:
            print(f"Halaman {page_num:<3} -> Gagal diubah menjadi gambar, dilewati.")
            continue
        
        visual_result_raw = predict_page_class(image_path)
        visual_result = visual_result_raw.split('_', 1)[-1]

        # --- LOGIKA KEPUTUSAN FINAL ---
        final_doc_type = ""
        # Jika hasil visual sangat jelas (bukan dokumen teks), kita lebih percaya padanya.
        if visual_result in ["REDLINE_DRAWING", "HASIL_CAPTURE", "EVIDENCE_PHOTO"]:
            final_doc_type = visual_result
        # Jika tidak, kita percaya pada hasil kata kunci
        elif keyword_result != "UNKNOWN":
            final_doc_type = keyword_result
        # Jika keduanya tidak yakin, baru kita gunakan tebakan visual sebagai pilihan terakhir
        else:
            final_doc_type = visual_result

        if final_doc_type not in ['UNKNOWN', 'ERROR']:
             document_map[final_doc_type].append(page_num)
        
        print(f"Halaman {page_num:<3} -> Keyword: {keyword_result} | Visual: {visual_result} -> Dipilih: {final_doc_type}")
        
    print("\n--- Klasifikasi halaman selesai. ---\n")

    # Sisa fungsi ini tidak berubah sama sekali
    final_results = []
    print("\n--- TAHAP 2: VERIFIKASI CHECKLIST ---\n")
    for kategori_item in selected_checklist:
        for sub_item in kategori_item['sub_items']:
            status, keterangan = ("TIDAK OK", "TIDAK ADA")
            if sub_item['id'] in document_map:
                if sub_item.get('requires_signature', False):
                    page_to_check_num = document_map[sub_item['id']][-1] - 1
                    image_path_for_signature = convert_pdf_page_to_image(doc, page_to_check_num)
                    if image_path_for_signature and detect_signature(image_path_for_signature):
                        status, keterangan = ("OK", "ADA, LENGKAP TANDA TANGAN")
                    else:
                        status, keterangan = ("TIDAK OK", "ADA, TANDA TANGAN TIDAK LENGKAP")
                else:
                    status, keterangan = ("OK", "ADA")
            final_results.append({'no': kategori_item['no'], 'kategori': kategori_item['kategori'], 'char': sub_item['char'], 'name': sub_item['name'], 'status': status, 'keterangan': keterangan, 'id': sub_item['id']})
    
    total_items = len(final_results)
    items_found = sum(1 for item in final_results if "TIDAK ADA" not in item['keterangan'])
    signatures_required = sum(1 for item in selected_checklist for sub_item in item['sub_items'] if sub_item.get('requires_signature'))
    signatures_found = sum(1 for item in final_results if "LENGKAP TANDA TANGAN" in item['keterangan'])
    
    score_kelengkapan = (items_found / total_items) * 60 if total_items > 0 else 0
    score_ttd = (signatures_found / signatures_required) * 40 if signatures_required > 0 else 40
    total_score = score_kelengkapan + score_ttd

    if total_score >= 95: integrity_level = "SANGAT BAIK"
    elif total_score >= 80: integrity_level = "BAIK"
    elif total_score >= 60: integrity_level = "CUKUP (PERLU REVIEW)"
    else: integrity_level = "KURANG (WAJIB REVIEW)"
    
    doc.close()
    return (final_results, total_score, integrity_level)