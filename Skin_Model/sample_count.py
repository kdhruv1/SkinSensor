import os
import pandas as pd
from collections import Counter

ISIC_IMAGE_DIR = "dataset/ISIC-images/"
ISIC_CSV_PATH = "dataset/train.csv"

SD198_IMAGE_DIR = "dataset/sd-198/images/"
SD198_CLASS_PATH = "dataset/sd-198/classes.txt"
SD198_LABELS_PATH = "dataset/sd-198/image_class_labels.txt"
SD198_IMAGES_LIST = "dataset/sd-198/images.txt"

CUSTOM_AUGMENT_DIR = "dataset/custom-augment/"

# ISIC Dataset
isic_df = pd.read_csv(ISIC_CSV_PATH, dtype=str)
isic_df = isic_df[isic_df["diagnosis"].notna()]
print(f" ISIC Dataset: {len(isic_df)} samples found.")

# SD-198 Dataset
with open(SD198_CLASS_PATH) as f:
    sd198_classes = [line.strip().split(" ", 1)[1] for line in f.readlines()]

labels_df = pd.read_csv(SD198_LABELS_PATH, sep=" ", names=["img_id", "class_id"])
images_df = pd.read_csv(SD198_IMAGES_LIST, sep=" ", names=["img_id", "img_path"])
sd198_df = pd.merge(labels_df, images_df, on="img_id")
print(f" SD-198 Dataset: {len(sd198_df)} samples found.")

# custom-augment dataset
custom_augment_counter = Counter()
for class_folder in os.listdir(CUSTOM_AUGMENT_DIR):
    class_path = os.path.join(CUSTOM_AUGMENT_DIR, class_folder)
    if os.path.isdir(class_path):
        num_images = len(os.listdir(class_path))
        custom_augment_counter[class_folder] = num_images

print("\n custom-augment samples per Class:")
for class_name, num_samples in custom_augment_counter.items():
    print(f"  - {class_name}: {num_samples} samples")

print(f"\n total custom-augment samples: {sum(custom_augment_counter.values())}")
#a