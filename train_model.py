# train_model.py
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import os
import json # Tambahkan import json

# --- PENGATURAN & PARAMETER ---
DATASET_PATH = "dataset_visual/"
IMAGE_SIZE = (160, 160)
BATCH_SIZE = 16
EPOCHS = 20
MODEL_FILENAME = 'document_classifier_model.keras'
CLASS_NAMES_FILENAME = 'class_names.json' # Nama file untuk menyimpan kelas

# --- MEMUAT & MEMPERSIAPKAN DATASET ---
print("Memuat dataset dari folder...")
try:
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        os.path.join(DATASET_PATH, 'train'), shuffle=True, batch_size=BATCH_SIZE, image_size=IMAGE_SIZE
    )
    validation_dataset = tf.keras.utils.image_dataset_from_directory(
        os.path.join(DATASET_PATH, 'validation'), shuffle=True, batch_size=BATCH_SIZE, image_size=IMAGE_SIZE
    )
except Exception as e:
    print(f"Error saat memuat dataset: {e}")
    exit()

class_names = train_dataset.class_names
print("Kelas yang ditemukan:", class_names)

# ---> PEMBARUAN: Simpan nama kelas ke file JSON
with open(CLASS_NAMES_FILENAME, 'w') as f:
    json.dump(class_names, f)
print(f"Nama kelas berhasil disimpan di '{CLASS_NAMES_FILENAME}'")

AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)

# --- MEMBANGUN ARSITEKTUR MODEL ---
print("Membangun arsitektur model...")
base_model = tf.keras.applications.MobileNetV2(input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3), include_top=False, weights='imagenet')
base_model.trainable = False
inputs = keras.Input(shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3))
x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(len(class_names), activation='softmax')(x)
model = keras.Model(inputs, outputs)

# --- KOMPILASI MODEL ---
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])
model.summary()

# --- MELATIH MODEL ---
print("\nMemulai proses training AI...")
history = model.fit(train_dataset, epochs=EPOCHS, validation_data=validation_dataset)
print("Training selesai!")

# --- MENYIMPAN MODEL ---
model.save(MODEL_FILENAME)
print(f"Model berhasil disimpan sebagai '{MODEL_FILENAME}'")

# --- VISUALISASI HASIL ---
acc, val_acc = history.history['accuracy'], history.history['val_accuracy']
loss, val_loss = history.history['loss'], history.history['val_loss']
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(acc, label='Akurasi Training'); plt.plot(val_acc, label='Akurasi Validasi')
plt.legend(loc='lower right'); plt.title('Grafik Akurasi'); plt.xlabel('Epoch')
plt.subplot(1, 2, 2)
plt.plot(loss, label='Loss Training'); plt.plot(val_loss, label='Loss Validasi')
plt.legend(loc='upper right'); plt.title('Grafik Loss'); plt.xlabel('Epoch')
plt.suptitle('Hasil Training Model'); plt.show()