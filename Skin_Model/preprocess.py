import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
from sklearn.model_selection import train_test_split


IMAGE_DIR = "dataset/ISIC-images/"  
IMG_SIZE = 224  # Required for MobileNetV2 , this is the pretrained CNN i will use to ensure high accuracy

# Load Metadata CSV
df = pd.read_csv("dataset/train.csv", low_memory=False, dtype=str)


image_column = "isic_id" if "isic_id" in df.columns else "image_name"


disease_mapping = {disease: idx for idx, disease in enumerate(df["diagnosis"].unique())}
df["target"] = df["diagnosis"].map(disease_mapping)


print("Disease Label Mapping:", disease_mapping)

#  Function to Remove Metadata
def remove_exif(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")  # Removes EXIF metadata
        return img
    except Exception as e:
        print(f" Error loading {image_path}: {e}")
        return None

#  Preprocess Images (Resize, Normalize)
def load_and_preprocess_image(image_id):
    img_path = os.path.join(IMAGE_DIR, image_id + ".jpg")

    # Remove metadata
    img = remove_exif(img_path)
    if img is None:
        return None  # Skip missing files

    # Convert to OpenCV format
    img = np.array(img)

    # Resize to 224x224
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

    # Normalize pixel values (0-1)
    img = img / 255.0

    return img


df_sample = df.head(50)  # Take the first 50 rows for testing

#  Apply Preprocessing to  Images
X_sample, y_sample = [], []
missing_files = []

for i, row in tqdm(df_sample.iterrows(), total=len(df_sample)):
    img = load_and_preprocess_image(row[image_column])  
    if img is not None:
        X_sample.append(img)
        y_sample.append(row["target"])  
    else:
        missing_files.append(row[image_column])

print(f" Sample Test: {len(X_sample)} images processed.")
print(f" Missing Images: {len(missing_files)}")

#   Sample Data saved Separately for testing
np.save("X_sample.npy", np.array(X_sample))
np.save("y_sample.npy", np.array(y_sample))

print(" Preprocessing Test Complete! Saved as `X_sample.npy` and `y_sample.npy`.")
