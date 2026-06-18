import os
import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model

# ==================================================
# PATH PROJECT
# ==================================================
BASE_DIR = os.getcwd()

train_dir = os.path.join(BASE_DIR, "model", "dataset", "train")
test_dir = os.path.join(BASE_DIR, "model", "dataset", "test")

save_path = os.path.join(
    BASE_DIR,
    "model",
    "saved_model",
    "freshscan.h5"
)

# ==================================================
# CEK PATH
# ==================================================
print("\n===== PATH CHECK =====")
print("Train Path :", train_dir)
print("Test Path  :", test_dir)

print("Train Exists :", os.path.exists(train_dir))
print("Test Exists  :", os.path.exists(test_dir))

# ==================================================
# INFO DATASET
# ==================================================
train_fresh = len(os.listdir(os.path.join(train_dir, "fresh")))
train_rotten = len(os.listdir(os.path.join(train_dir, "rotten")))

test_fresh = len(os.listdir(os.path.join(test_dir, "fresh")))
test_rotten = len(os.listdir(os.path.join(test_dir, "rotten")))

print("\n===== DATASET INFO =====")
print(f"Train Fresh  : {train_fresh}")
print(f"Train Rotten : {train_rotten}")
print(f"Total Train  : {train_fresh + train_rotten}")

print()

print(f"Test Fresh   : {test_fresh}")
print(f"Test Rotten  : {test_rotten}")
print(f"Total Test   : {test_fresh + test_rotten}")

print("========================\n")

# ==================================================
# PARAMETER
# ==================================================
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5

# ==================================================
# DATA GENERATOR
# ==================================================
print("Membuat Data Generator...")

train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

test_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=True
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

# ==================================================
# CLASS INFO
# ==================================================
print("\n===== CLASS INFO =====")
print("Class Mapping :", train_generator.class_indices)
print("Train Samples :", train_generator.samples)
print("Test Samples  :", test_generator.samples)
print("======================\n")

# ==================================================
# LOAD MOBILENETV2
# ==================================================
print("Loading MobileNetV2...")

base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

base_model.trainable = False

# ==================================================
# CLASSIFICATION HEAD
# ==================================================
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)

predictions = Dense(
    1,
    activation='sigmoid'
)(x)

model = Model(
    inputs=base_model.input,
    outputs=predictions
)

# ==================================================
# COMPILE MODEL
# ==================================================
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("\n===== MODEL SIAP =====")
print("Loss Function :", model.loss)
print("======================\n")

# ==================================================
# TRAINING
# ==================================================
print("Mulai Training...\n")

history = model.fit(
    train_generator,
    validation_data=test_generator,
    epochs=EPOCHS
)

# ==================================================
# EVALUASI
# ==================================================
print("\nEvaluasi Model...")

loss, accuracy = model.evaluate(
    test_generator,
    verbose=1
)

print("\n===== HASIL AKHIR =====")
print(f"Loss     : {loss:.4f}")
print(f"Accuracy : {accuracy * 100:.2f}%")
print("=======================\n")

# ==================================================
# SAVE MODEL
# ==================================================
print("Menyimpan Model...")

model.save(save_path)

print("\n✅ MODEL BERHASIL DISIMPAN")
print("📁 Lokasi :", save_path)