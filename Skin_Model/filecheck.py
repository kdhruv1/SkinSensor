import pandas as pd
import os
from collections import Counter

#  Checking csv and images
df = pd.read_csv("dataset/train.csv")
print(f"CSV rows: {len(df)}")

image_folder = "dataset/ISIC-images/"
image_files = [f for f in os.listdir(image_folder) if f.endswith(".jpg")]
print(f"Image files in folder: {len(image_files)}")


ISIC_CSV_PATH = "dataset/train.csv"
SD198_CLASS_PATH = "dataset/sd-198/classes.txt"
SD198_LABELS_PATH = "dataset/sd-198/image_class_labels.txt"
SD198_IMAGES_LIST = "dataset/sd-198/images.txt"
CUSTOM_AUGMENT_DIR = "dataset/custom-augment/"

# loading isic metadata
isic_df = pd.read_csv(ISIC_CSV_PATH, dtype=str)
isic_df = isic_df[isic_df["diagnosis"].notna()]
isic_df["label_name"] = isic_df["diagnosis"]
isic_df["dataset"] = "ISIC"

# gropuing isic labels
isic_group_map = {
    "nevus": "Benign_Nevus",
    "melanoma": "Malignant_Melanoma",
    "seborrheic keratosis": "Benign_Keratosis",
    "lentigo NOS": "Pigmentation_Disorder",
    "solar lentigo": "Pigmentation_Disorder",
    "lichenoid keratosis": "Pre_Malignant_Lesion"
}
isic_df["grouped_label"] = isic_df["label_name"].map(isic_group_map)
isic_df = isic_df[isic_df["grouped_label"].notna()]

# filtering samples less than 30
isic_group_counts = Counter(isic_df["grouped_label"])
valid_isic_labels = {label for label, count in isic_group_counts.items() if count >= 30}
isic_df = isic_df[isic_df["grouped_label"].isin(valid_isic_labels)]

# print results
print("\n cleaned ISIC grouped class counts (≥30 samples):")
for label, count in Counter(isic_df["grouped_label"]).most_common():
    print(f"{label:<25} {count}")

# loading SD-198 meta data
with open(SD198_CLASS_PATH) as f:
    sd198_classes = [line.strip().split(" ", 1)[1] for line in f.readlines()]

labels_df = pd.read_csv(SD198_LABELS_PATH, sep=" ", names=["img_id", "class_id"])
images_df = pd.read_csv(SD198_IMAGES_LIST, sep=" ", names=["img_id", "img_path"])
sd198_df = pd.merge(labels_df, images_df, on="img_id")
sd198_df["label_name"] = sd198_df["class_id"].apply(lambda x: sd198_classes[x - 1])
sd198_df["dataset"] = "SD198"

# sd-198 label mapping
sd198_group_map = {
    "Acne_Vulgaris": "Acneiform", "Acne_Keloidalis_Nuchae": "Acneiform",
    "Pomade_Acne": "Acneiform", "Pseudofolliculitis_Barbae": "Acneiform",
    "Nevus_Comedonicus": "Acneiform",
    "Atopic_Dermatitis": "Eczema", "Nummular_Eczema": "Eczema",
    "Seborrheic_Dermatitis": "Eczema", "Dyshidrosiform_Eczema": "Eczema",
    "Allergic_Contact_Dermatitis": "Eczema", "Stasis_Dermatitis": "Eczema",
    "Neurodermatitis": "Eczema", "Frictional_Lichenoid_Dermatitis": "Eczema",
    "Perioral_Dermatitis": "Eczema",
    "Psoriasis": "Psoriasis", "Guttate_Psoriasis": "Psoriasis",
    "Scalp_Psoriasis": "Psoriasis", "Pustular_Psoriasis": "Psoriasis",
    "Nail_Psoriasis": "Psoriasis", "Mucous_Membrane_Psoriasis": "Psoriasis",
    "Tinea_Corporis": "Fungal", "Tinea_Cruris": "Fungal",
    "Tinea_Faciale": "Fungal", "Tinea_Manus": "Fungal",
    "Tinea_Pedis": "Fungal", "Tinea_Versicolor": "Fungal",
    "Onychomycosis": "Fungal",
    "Herpes_Simplex_Virus": "Viral", "Herpes_Zoster": "Viral",
    "Molluscum_Contagiosum": "Viral", "Verruca_Vulgaris": "Viral",
    "Impetigo": "Bacterial", "Cellulitis": "Bacterial", "Folliculitis": "Bacterial",
    "Melasma": "Pigmentation", "Vitiligo": "Pigmentation",
    "Cafe_Au_Lait_Macule": "Pigmentation", "Hyperpigmentation": "Pigmentation",
    "Actinic_solar_Damage(Pigmentation)": "Pigmentation",
    "Seborrheic_Keratosis": "Benign_Tumor", "Dermatofibroma": "Benign_Tumor",
    "Syringoma": "Benign_Tumor", "Lipoma": "Benign_Tumor",
    "Nevus_Comedonicus": "Benign_Tumor", "Sebaceous_Gland_Hyperplasia": "Benign_Tumor",
    "Basal_Cell_Carcinoma": "Malignant", "Bowen's_Disease": "Malignant",
    "Malignant_Melanoma": "Malignant", "Lentigo_Maligna_Melanoma": "Malignant",
    "Beau's_Lines": "Nail_Disorder", "Nail_Dystrophy": "Nail_Disorder",
    "Onycholysis": "Nail_Disorder", "Onychomycosis": "Nail_Disorder",
    "Pincer_Nail_Syndrome": "Nail_Disorder", "Subungual_Hematoma": "Nail_Disorder",
    "Alopecia_Areata": "Alopecia", "Androgenetic_Alopecia": "Alopecia",
    "Scarring_Alopecia": "Alopecia",
    "Discoid_Lupus_Erythematosus": "Autoimmune", "Lichen_Planus": "Autoimmune",
    "Lichen_Simplex_Chronicus": "Autoimmune", "Morphea": "Autoimmune",
    "Angioma": "Vascular", "Strawberry_Hemangioma": "Vascular",
    "Xerosis": "Other", "Callus": "Other", "Ulcer": "Other", "Scar": "Other"
}

sd198_df["grouped_label"] = sd198_df["label_name"].map(lambda x: sd198_group_map.get(x, None))
sd198_df = sd198_df[sd198_df["grouped_label"].notna()]

# print results
print("\n SD-198 grouped  class counts:")
for label, count in Counter(sd198_df["grouped_label"]).most_common():
    print(f"{label:<20} {count}")

# load custom-augmnet
print("\ custom-augment class sample counts:")
custom_augment_counter = Counter()

for class_folder in sorted(os.listdir(CUSTOM_AUGMENT_DIR)):
    class_path = os.path.join(CUSTOM_AUGMENT_DIR, class_folder)
    if os.path.isdir(class_path):
        count = len([f for f in os.listdir(class_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))])
        custom_augment_counter[class_folder] = count

for label, count in custom_augment_counter.items():
    print(f"{label:<20} {count}")

print(f"\n total custom-augment samples: {sum(custom_augment_counter.values())}")

from collections import Counter


custom_augment_counts = {
    'Acneiform': 100,
    'Alopecia': 100,
    'Autoimmune': 100,
    'Bacterial': 110,
    'Benign_Tumor': 100,
    'Eczema': 0,
    'Fungal': 0,
    'Malignant': 0,
    'Nail_Disorder': 0,
    'Pigmentation': 100,
    'Pre_Malignant_Lesion': 150,
    'Psoriasis': 0,
    'Vascular': 100,
    'Viral': 150,
    'other': 0
}

sd198_grouped_counts = {
    'Eczema': 377,
    'Fungal': 330,
    'Benign_Tumor': 259,
    'Psoriasis': 239,
    'Malignant': 232,
    'Nail_Disorder': 215,
    'Other': 142,
    'Acneiform': 140,
    'Autoimmune': 115,
    'Alopecia': 114,
    'Pigmentation': 97,
    'Viral': 90,
    'Vascular': 66,
    'Bacterial': 51
}


merged_counts = Counter()

for label, count in sd198_grouped_counts.items():
    merged_counts[label] += count

# Then add Custom-Augment counts
for label, count in custom_augment_counts.items():
    merged_counts[label] += count


print("\n merged class sample counts (custom-Augment + SD-198):")
for label, count in merged_counts.most_common():
    print(f"{label:<20} {count}")

print(f"\n total samples {sum(merged_counts.values())}")
