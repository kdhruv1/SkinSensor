import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
from collections import Counter
from sklearn.model_selection import train_test_split

# ==== CONFIG ====
IMAGE_DIR = "dataset/ISIC-images/"  # folder with all your images
CSV_PATH = "dataset/train.csv"       # your metadata file
IMG_SIZE = 224                       # input size for MobileNetV2

# ==== LOAD METADATA ====
df = pd.read_csv(CSV_PATH, low_memory=False, dtype=str)
print(f"CSV rows: {len(df)}")

image_column = "isic_id" if "isic_id" in df.columns else "image_name"

# Remove missing diagnosis rows
df = df[df["diagnosis"].notna()]

# Create label mappings
disease_mapping = {disease: idx for idx, disease in enumerate(df["diagnosis"].unique())}
index_mapping = {v: k for k, v in disease_mapping.items()}
df["target"] = df["diagnosis"].map(disease_mapping)

print("📌 Label Mapping:", disease_mapping)

# ==== REMOVE METADATA (EXIF) ====
def remove_exif(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")  # remove exif and force RGB
        return img
    except Exception as e:
        print(f"⚠️ Error loading {image_path}: {e}")
        return None

# ==== PREPROCESS IMAGES ====
def preprocess_image(image_id):
    path = os.path.join(IMAGE_DIR, image_id + ".jpg")
    img = remove_exif(path)
    if img is None:
        return None
    img = np.array(img)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    return img / 255.0  # normalize between 0-1

# ==== PROCESS ALL IMAGES ====
X, y, failed = [], [], []

print("📦 Loading images...")
for i, row in tqdm(df.iterrows(), total=len(df)):
    img = preprocess_image(row[image_column])
    if img is not None:
        X.append(img)
        y.append(int(row["target"]))
    else:
        failed.append(row[image_column])

print(f"✅ Processed: {len(X)} images | ❌ Failed: {len(failed)}")

X = np.array(X)
y = np.array(y)

# ==== FILTER CLASSES (at least 2 samples required) ====
label_counts = Counter(y)
valid_indices = [i for i, label in enumerate(y) if label_counts[label] >= 2]

X = X[valid_indices]
y = y[valid_indices]

# ==== SPLIT (70% train / 30% validation) ====
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

print(f"🧠 Train size: {len(X_train)} | 🧪 Val size: {len(X_val)}")

# ==== SAVE DATA ====
np.save("X_train.npy", X_train)
np.save("X_val.npy", X_val)
np.save("y_train.npy", y_train)
np.save("y_val.npy", y_val)

np.save("label_to_index.npy", disease_mapping)
np.save("index_to_label.npy", index_mapping)

print("\n✅ Done! Saved:")
print(" - X_train.npy")
print(" - X_val.npy")
print(" - y_train.npy")
print(" - y_val.npy")
print(" - label_to_index.npy")
print(" - index_to_label.npy")
