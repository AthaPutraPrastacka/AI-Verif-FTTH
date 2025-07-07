# modules/dl_classifier.py
import tensorflow as tf
import numpy as np
import os
import json

MODEL_PATH = 'document_classifier_model.keras'
CLASS_NAMES_FILENAME = 'class_names.json'
IMAGE_SIZE = (160, 160)
model, class_names = None, []

try:
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
        if os.path.exists(CLASS_NAMES_FILENAME):
            with open(CLASS_NAMES_FILENAME, 'r') as f:
                class_names = json.load(f)
        else:
            print(f"KRITIS: File '{CLASS_NAMES_FILENAME}' tidak ditemukan. Model tidak bisa digunakan.")
            model = None
    else:
        print(f"KRITIS: File model tidak ditemukan di '{MODEL_PATH}'. Jalankan train_model.py terlebih dahulu.")
except Exception as e:
    print(f"Error saat memuat model atau nama kelas: {e}")
    model = None

def predict_page_class(page_image_path: str) -> str:
    if model is None or not class_names: return "ERROR_MODEL_NOT_LOADED"
    try:
        img = tf.keras.utils.load_img(page_image_path, target_size=IMAGE_SIZE)
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        preprocessed_img = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        predictions = model.predict(preprocessed_img, verbose=0)
        score = tf.nn.softmax(predictions[0])
        class_name = class_names[np.argmax(score)]
        return class_name
    except Exception as e:
        print(f"  -> Error saat prediksi DL: {e}")
        return "ERROR_PREDICTION"