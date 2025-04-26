import os

# ==== CONFIG ====
CUSTOM_AUGMENT_DIR = r"C:/Users/Kdhru/SkinSensor-Copy/Skin_Model/dataset/custom-augment/"

# ==== SCRIPT ====
print("\n📊 Custom-Augment Class Sample Counts:")
total = 0
for class_folder in sorted(os.listdir(CUSTOM_AUGMENT_DIR)):
    class_path = os.path.join(CUSTOM_AUGMENT_DIR, class_folder)
    if os.path.isdir(class_path):
        count = len([f for f in os.listdir(class_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))])
        print(f" - {class_folder}: {count} samples")
        total += count

print(f"\n✅ Total Samples in Custom-Augment: {total}")
