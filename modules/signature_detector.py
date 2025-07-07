# modules/signature_detector.py
import cv2
import numpy as np
import os

def detect_signature(image_path: str) -> bool:
    if not os.path.exists(image_path):
        print(f"[ERROR] Signature check: Gambar tidak ditemukan di {image_path}")
        return False
        
    try:
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if img is None: return False
        height, _, _ = img.shape
        roi_start_y = int(height * 0.60)
        roi = img[roi_start_y:height, :]
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blurred_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)
        binary_roi = cv2.adaptiveThreshold(blurred_roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        contours, _ = cv2.findContours(binary_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        signature_like_contours = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0: continue
            complexity = (perimeter * perimeter) / area
            if (50 < area < 80000) and (complexity > 25):
                signature_like_contours += 1
        return signature_like_contours >= 1
    except Exception as e:
        print(f"[ERROR] Gagal deteksi tanda tangan: {e}")
        return False