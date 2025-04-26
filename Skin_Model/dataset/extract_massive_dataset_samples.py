import os
import shutil
import random
from collections import Counter

# ==== CONFIG ====
SOURCE_DIR = r"C:/Users/Kdhru/Downloads/archive (1)/balanced_dataset/balanced_dataset/"
CUSTOM_AUGMENT_DIR = r"C:/Users/Kdhru/SkinSensor-Copy/Skin_Model/dataset/custom-augment/"

# Classes to copy: (source_folder) -> (target_folder) -> (limit)
copy_plan = [
    ("Light Diseases And Disorders Of Pigmentation", "Pigmentation", 100),
    ("Warts Molluscum And Other Viral Infections", "Viral", 100),
    ("Herpes Hpv And Other Stds Photos", "Viral", 50),
    ("Cellulitis Impetigo And Other Bacterial Infections", "Bacterial", 80),
    ("Ba Impetigo", "Bacterial", 30),
    ("Ba Cellulitis", "Bacterial", 30),
    ("Lupus And Other Connective Tissue Diseases", "Autoimmune", 100),
    ("Psoriasis Pictures Lichen Planus And Related", "Autoimmune", 50),
    ("Hair Loss Photos Alopecia And Other Hair Diseases", "Alopecia", 100),
    ("Acne And Rosacea Photos", "Acneiform", 100),
]

# ==== SCRIPT ====

# Create target folders if missing
for _, target_folder, _ in copy_plan:
    target_path = os.path.join(CUSTOM_AUGMENT_DIR, target_folder)
    os.makedirs(target_path, exist_ok=True)

# Copy samples
copied_counter = Counter()

for source_folder, target_folder, limit in copy_plan:
    source_path = os.path.join(SOURCE_DIR, source_folder)
    target_path = os.path.join(CUSTOM_AUGMENT_DIR, target_folder)

    if not os.path.exists(source_path):
        print(f"⚠️ Warning: Source folder '{source_folder}' not found. Skipping...")
        continue

    images = [img for img in os.listdir(source_path) if img.lower().endswith((".jpg", ".jpeg", ".png"))]
    random.shuffle(images)  # Shuffle to get a random selection
    selected_images = images[:limit]

    for img_file in selected_images:
        src_file = os.path.join(source_path, img_file)
        dst_file = os.path.join(target_path, img_file)
        shutil.copy(src_file, dst_file)
        copied_counter[target_folder] += 1

    print(f"✅ Copied {len(selected_images)} images from '{source_folder}' to '{target_folder}'.")

# ==== SUMMARY ====
print("\n📦 Copy Summary:")
for target_class, num_copied in copied_counter.items():
    print(f"  - {target_class}: {num_copied} samples added")

print("\n✅ Extraction completed successfully!")
