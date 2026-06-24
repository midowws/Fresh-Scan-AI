import os
import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

# ==================================================
# PATH PROJECT
# ==================================================
BASE_DIR = os.getcwd()

train_dir = os.path.join(BASE_DIR, "model", "dataset", "train")
test_dir = os.path.join(BASE_DIR, "model", "dataset", "test")

save_path = os.path.join(BASE_DIR, "model", "saved_model", "freshscan.h5")

# Pastikan folder saved_model ada
os.makedirs(os.path.dirname(save_path), exist_ok=True)

# ==================================================
# INFO DATASET (DINAMIS 12 KELAS)
# ==================================================
print("\n===== DATASET INFO =====")
try:
    train_classes = os.listdir(train_dir)
    print(f"Ditemukan {len(train_classes)} Kelas di Folder Train:")
    for cls in sorted(train_classes):
        jml = len(os.listdir(os.path.join(train_dir, cls)))
        print(f" - {cls}: {jml} gambar")
except FileNotFoundError:
    print("⚠️ Folder dataset belum ditemukan!")

# ==================================================
# PARAMETER TUNING
# ==================================================
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 25 # Dinaikkan karena ada Early Stopping

# ==================================================
# DATA GENERATOR (AUGMENTASI)
# ==================================================
print("\nMembuat Data Generator...")

train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    shear_range=0.15,
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

# PERUBAHAN KRUSIAL: class_mode menjadi 'categorical'
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

num_classes = train_generator.num_classes

print("\n===== CLASS INFO =====")
print("Class Mapping :", train_generator.class_indices)
print(f"Total Kelas   : {num_classes}")
print("======================\n")

# ==================================================
# LOAD MOBILENETV2 & FINE-TUNING
# ==================================================
print("Loading MobileNetV2 dan Setup Fine-Tuning...")

base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# Membuka gembok seluruh base_model
base_model.trainable = True

# Mengunci kembali layer-layer awal, menyisakan 30 layer terakhir untuk dilatih ulang (Fine-tuning)
for layer in base_model.layers[:-30]:
    layer.trainable = False

# ==================================================
# CLASSIFICATION HEAD (MULTICLASS)
# ==================================================
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.4)(x) # Dinaikkan sedikit untuk mencegah overfitting

# PERUBAHAN KRUSIAL: Dense sejumlah kelas, aktivasi Softmax
predictions = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# ==================================================
# COMPILE MODEL (LEARNING RATE KECIL)
# ==================================================
# Menggunakan loss categorical_crossentropy untuk > 2 kelas
model.compile(
    optimizer=Adam(learning_rate=0.0001), 
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ==================================================
# CALLBACKS (ASISTEN TRAINING)
# ==================================================
# 1. Simpan model HANYA saat akurasi meningkat
checkpoint = ModelCheckpoint(
    save_path, 
    monitor='val_accuracy', 
    save_best_only=True, 
    mode='max', 
    verbose=1
)

# 2. Hentikan training jika tidak ada peningkatan selama 5 epoch
early_stop = EarlyStopping(
    monitor='val_accuracy', 
    patience=5, 
    restore_best_weights=True,
    verbose=1
)

# 3. Turunkan kecepatan belajar jika model mentok
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss', 
    factor=0.2, 
    patience=3, 
    min_lr=1e-6,
    verbose=1
)

# ==================================================
# TRAINING
# ==================================================
print("\nMulai Training dengan Asisten Otomatis...\n")

history = model.fit(
    train_generator,
    validation_data=test_generator,
    epochs=EPOCHS,
    callbacks=[checkpoint, early_stop, reduce_lr]
)

# ==================================================
# EVALUASI
# ==================================================
print("\nEvaluasi Model Terbaik...")

loss, accuracy = model.evaluate(test_generator, verbose=1)

print("\n===== HASIL AKHIR =====")
print(f"Loss     : {loss:.4f}")
print(f"Accuracy : {accuracy * 100:.2f}%")
print("✅ MODEL TERBAIK TELAH DISIMPAN OTOMATIS")
print("=======================\n")
