import os
import json
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
from collections import Counter
from sklearn.model_selection import train_test_split


ISIC_IMAGE_DIR = "dataset/ISIC-images/"
ISIC_CSV_PATH = "dataset/train.csv"

SD198_IMAGE_DIR = "dataset/sd-198/images/"
SD198_CLASS_PATH = "dataset/sd-198/classes.txt"
SD198_LABELS_PATH = "dataset/sd-198/image_class_labels.txt"
SD198_IMAGES_LIST = "dataset/sd-198/images.txt"

CUSTOM_AUGMENT_DIR = "dataset/custom-augment/"

IMG_SIZE = (224, 224)

# lable grouping
isic_group_map = {
    "nevus": "Benign_Nevus",
    "melanoma": "Malignant_Melanoma",
    "seborrheic keratosis": "Benign_Keratosis",
    "solar lentigo": "Pigmentation_Disorder",
    "lentigo NOS": "Pigmentation_Disorder",
    "lichenoid keratosis": "Pre_Malignant_Lesion",
}

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
    "Sebaceous_Gland_Hyperplasia": "Benign_Tumor",
    "Basal_Cell_Carcinoma": "Malignant", "Bowen's_Disease": "Malignant",
    "Malignant_Melanoma": "Malignant", "Lentigo_Maligna_Melanoma": "Malignant",
    "Beau's_Lines": "Nail_Disorder", "Nail_Dystrophy": "Nail_Disorder",
    "Onycholysis": "Nail_Disorder", "Pincer_Nail_Syndrome": "Nail_Disorder",
    "Subungual_Hematoma": "Nail_Disorder",
    "Alopecia_Areata": "Alopecia", "Androgenetic_Alopecia": "Alopecia",
    "Scarring_Alopecia": "Alopecia",
    "Discoid_Lupus_Erythematosus": "Autoimmune", "Lichen_Planus": "Autoimmune",
    "Lichen_Simplex_Chronicus": "Autoimmune", "Morphea": "Autoimmune",
    "Angioma": "Vascular", "Strawberry_Hemangioma": "Vascular",
    "Xerosis": "Other", "Callus": "Other", "Ulcer": "Other", "Scar": "Other"
}

# ISIC dataset
isic_df = pd.read_csv(ISIC_CSV_PATH, dtype=str)
isic_df = isic_df[isic_df["diagnosis"].notna()]
isic_df["label_name"] = isic_df["diagnosis"].map(lambda x: isic_group_map.get(x.strip().lower(), None))
isic_df = isic_df[isic_df["label_name"].notna()]
isic_df["image_id"] = isic_df["isic_id"]
isic_df["dataset"] = "ISIC"

# SD-198 datset
with open(SD198_CLASS_PATH) as f:
    sd198_classes = [line.strip().split(" ", 1)[1] for line in f.readlines()]

labels_df = pd.read_csv(SD198_LABELS_PATH, sep=" ", names=["img_id", "class_id"])
images_df = pd.read_csv(SD198_IMAGES_LIST, sep=" ", names=["img_id", "img_path"])
sd198_df = pd.merge(labels_df, images_df, on="img_id")
sd198_df["label_name"] = sd198_df["class_id"].apply(lambda x: sd198_classes[x - 1])
sd198_df["label_name"] = sd198_df["label_name"].map(lambda x: sd198_group_map.get(x, None))
sd198_df = sd198_df[sd198_df["label_name"].notna()]
sd198_df["image_id"] = sd198_df["img_path"].apply(lambda x: os.path.splitext(x)[0])
sd198_df["dataset"] = "SD198"


custom_rows = []
for class_folder in os.listdir(CUSTOM_AUGMENT_DIR):
    class_path = os.path.join(CUSTOM_AUGMENT_DIR, class_folder)
    if os.path.isdir(class_path):
        for img_file in os.listdir(class_path):
            if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                custom_rows.append({
                    "image_id": img_file,
                    "label_name": class_folder,
                    "dataset": "CUSTOM"
                })
custom_df = pd.DataFrame(custom_rows)

# combing datasets
combined_df = pd.concat([
    isic_df[["image_id", "label_name", "dataset"]],
    sd198_df[["image_id", "label_name", "dataset"]],
    custom_df[["image_id", "label_name", "dataset"]]
])

# label index
label_counts = Counter(combined_df["label_name"])
valid_labels = {label for label, count in label_counts.items() if count >= 2}
combined_df = combined_df[combined_df["label_name"].isin(valid_labels)]

label_to_index = {label: i for i, label in enumerate(sorted(valid_labels))}
index_to_label = {i: label for label, i in label_to_index.items()}
combined_df["target"] = combined_df["label_name"].map(label_to_index)

# loading images
def load_image(row):
    if row["dataset"] == "ISIC":
        path = os.path.join(ISIC_IMAGE_DIR, row["image_id"] + ".jpg")
    elif row["dataset"] == "SD198":
        image_name = row["image_id"].replace("images/", "")
        path = os.path.join(SD198_IMAGE_DIR, image_name + ".jpg")
    else:  # CUSTOM
        for ext in (".jpg", ".jpeg", ".png"):
            try_path = os.path.join(CUSTOM_AUGMENT_DIR, row["label_name"], row["image_id"])
            if os.path.exists(try_path):
                path = try_path
                break
        else:
            print(f" Image missing: {row['image_id']}")
            return None

    try:
        img = Image.open(path).convert("RGB")
        img = img.resize(IMG_SIZE)
        return np.array(img) / 255.0
    except Exception as e:
        print(f" Error loading {path}: {e}")
        return None

X, y = [], []
print(" processing combined images...")
for _, row in tqdm(combined_df.iterrows(), total=len(combined_df)):
    img = load_image(row)
    if img is not None:
        X.append(img)
        y.append(row["target"])

X = np.array(X)
y = np.array(y)

# training split
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

# saving
np.save("X_train.npy", X_train)
np.save("X_val.npy", X_val)
np.save("y_train.npy", y_train)
np.save("y_val.npy", y_val)

with open("label_to_index.json", "w") as f:
    json.dump(label_to_index, f)
with open("index_to_label.json", "w") as f:
    json.dump(index_to_label, f)

# terminal outpu
print(f"\n all Done! saved cleaned and merged dataset.")
print(f" total final classes: {len(label_to_index)}")
print(f" train samples: {len(X_train)} | val samples: {len(X_val)}")
print("\n final sample counts per grouped class:")
print(pd.Series(y).map(index_to_label).value_counts())