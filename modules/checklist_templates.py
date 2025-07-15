# modules/checklist_templates.py

# --- TEMPLATE 1: UNTUK BAUT FTTH ---
TEMPLATE_BAUT = [
    {'no': '1', 'kategori': 'BA Uji Terima dan Laporan Uji Terima', 'sub_items': [
        {'id': 'BAUT', 'char': 'A', 'name': 'BAUT', 'requires_signature': True},
        {'id': 'LAPORAN_UT', 'char': 'B', 'name': 'Laporan UT', 'requires_signature': True}
    ]},
    {'no': '2', 'kategori': 'Permintaan Uji Terima Mitra', 'sub_items': [
        {'id': 'SURAT_PERMINTAAN', 'char': 'A', 'name': 'Surat Permintaan Uji Terima dari Mitra', 'requires_signature': True},
        {'id': 'BA_TESTCOMM', 'char': 'B', 'name': 'BA Test Commissioning dan Lampirannya', 'requires_signature': True}
    ]},
    {'no': '3', 'kategori': 'Pelaksanaan Uji Terima', 'sub_items': [
        {'id': 'SK_TEAM', 'char': 'A', 'name': 'SK/Penunjukan Team Uji Terima', 'requires_signature': False},
        {'id': 'NOTA_DINAS', 'char': 'B', 'name': 'Nota Dinas Pelaksanaan Uji Terima', 'requires_signature': False}
    ]},
    {'no': '4', 'kategori': 'Lampiran Uji Terima', 'sub_items': [
        {'id': 'REDLINE_DRAWING', 'char': 'A', 'name': 'Red line drawing', 'requires_signature': False},
        {'id': 'BOQ_AKHIR', 'char': 'B', 'name': 'BoQ akhir', 'requires_signature': False},
        {'id': 'HASIL_CAPTURE', 'char': 'C', 'name': 'Hasil Capture', 'requires_signature': False},
        {'id': 'EVIDENCE_PHOTO', 'char': 'D', 'name': 'Evidence Photo', 'requires_signature': False}
    ]}
]

# --- TEMPLATE 2: UNTUK CHECKLIST BARU (SESUAI GAMBAR) ---
TEMPLATE_CHECKLIST_BARU = [
    {'no': '1', 'kategori': 'BA Uji Terima dan Laporan Uji Terima', 'sub_items': [
        {'id': 'JUDUL_BAUT', 'char': 'A', 'name': 'Judul BAUT', 'requires_signature': False},
        {'id': 'DAFTAR_HADIR', 'char': 'B', 'name': 'Daftar Hadir', 'requires_signature': True}
    ]},
    {'no': '2', 'kategori': 'Permintaan Uji Terima Mitra', 'sub_items': [
        {'id': 'SURAT_PERMINTAAN_BARU', 'char': 'A', 'name': 'Surat Permintaan Uji Terima dari Mitra', 'requires_signature': True}
    ]},
    {'no': '3', 'kategori': 'Pelaksanaan Uji Terima', 'sub_items': [
        {'id': 'SK_PENUNJUKAN', 'char': 'A', 'name': 'SK/Penunjukan Pelaksanaan Uji Terima', 'requires_signature': False},
        {'id': 'NOTA_DINAS_PELAKSANAAN', 'char': 'B', 'name': 'Nota Dinas Pelaksanaan Uji Terima', 'requires_signature': False}
    ]},
    {'no': '4', 'kategori': 'Lampiran Uji Terima', 'sub_items': [
        {'id': 'BOQ_UT', 'char': 'A', 'name': 'BOQ Uji Terima', 'requires_signature': False},
        {'id': 'FOTO_KEGIATAN', 'char': 'B', 'name': 'Foto Kegiatan Uji Terima', 'requires_signature': False},
        {'id': 'FOTO_MATERIAL', 'char': 'C', 'name': 'Foto Material terpasang sesuai BOQ', 'requires_signature': False},
        {'id': 'FOTO_ROLLMETER', 'char': 'D', 'name': 'Foto Roll Meter / Fault Locator', 'requires_signature': False},
        {'id': 'FOTO_OPM', 'char': 'E', 'name': 'Foto Pengukuran OPM', 'requires_signature': False},
        {'id': 'FORM_OPM', 'char': 'F', 'name': 'Form OPM', 'requires_signature': True},
        {'id': 'FILE_OTDR', 'char': 'G', 'name': 'File PDF OTDR', 'requires_signature': False},
        {'id': 'BA_LAPANGAN', 'char': 'H', 'name': 'BA Lapangan', 'requires_signature': True},
    ]}
]

# --- DICTIONARY UTAMA YANG DIIMPOR OLEH app.py ---
# Kunci di sini adalah teks yang akan muncul di dropdown aplikasi.
ALL_TEMPLATES = {
    "Verifikasi BAUT FTTH": TEMPLATE_BAUT,
    "Checklist Dokumen Baru": TEMPLATE_CHECKLIST_BARU
}