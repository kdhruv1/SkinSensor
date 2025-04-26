import os
import shutil
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# ==== CONFIG ====
HAM_METADATA_PATH = "C:/Users/Kdhru/Downloads/archive/HAM10000_metadata.csv"
HAM_IMAGES_PART1 = "C:/Users/Kdhru/Downloads/archive/HAM10000_images_part_1/"
HAM_IMAGES_PART2 = "C:/Users/Kdhru/Downloads/archive/HAM10000_images_part_2/"
CUSTOM_AUGMENT_DIR = "custom-augment/"


# Mapping HAM labels to your grouped class folders
ham_to_custom_map = {
    "akiec": "Pre_Malignant_Lesion",
    "vasc": "Vascular",
    "df": "Benign_Tumor"
}

# Limit samples added per class
LIMIT_SAMPLES = {
    "Pre_Malignant_Lesion": 150,
    "Vascular": 100,
    "Benign_Tumor": 100
}

# ==== LOAD HAM METADATA ====
ham_df = pd.read_csv(HAM_METADATA_PATH)

# ==== PREPARE OUTPUT FOLDERS ====
for target_label in ham_to_custom_map.values():
    target_dir = os.path.join(CUSTOM_AUGMENT_DIR, target_label)
    os.makedirs(target_dir, exist_ok=True)

# ==== COPY IMAGES ====
added_counter = Counter()

for ham_label, target_folder in ham_to_custom_map.items():
    subset = ham_df[ham_df["dx"] == ham_label]
    print(f"🔎 Found {len(subset)} samples for '{ham_label}' -> '{target_folder}'.")

    # Shuffle and limit
    subset = subset.sample(frac=1, random_state=42)
    subset = subset.head(LIMIT_SAMPLES[target_folder])

    for _, row in subset.iterrows():
        img_filename = row["image_id"] + ".jpg"
        src_path1 = os.path.join(HAM_IMAGES_PART1, img_filename)
        src_path2 = os.path.join(HAM_IMAGES_PART2, img_filename)

        if os.path.exists(src_path1):
            shutil.copy(src_path1, os.path.join(CUSTOM_AUGMENT_DIR, target_folder, img_filename))
            added_counter[target_folder] += 1
        elif os.path.exists(src_path2):
            shutil.copy(src_path2, os.path.join(CUSTOM_AUGMENT_DIR, target_folder, img_filename))
            added_counter[target_folder] += 1
        else:
            print(f"⚠️ Missing image in both parts: {img_filename}")

# ==== SUMMARY REPORT ====
print("\n✅ Limited Extraction Completed!")
for label, count in added_counter.items():
    print(f"📦 {count} samples added to '{label}'.")

# ==== OPTIONAL: PLOT DISTRIBUTION ====
def plot_distribution(counter_dict, title):
    labels = list(counter_dict.keys())
    values = list(counter_dict.values())

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.title(title)
    plt.ylabel('Number of Samples')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

plot_distribution(added_counter, "📊 Samples Added to Each Minority Class (HAM10000)")
