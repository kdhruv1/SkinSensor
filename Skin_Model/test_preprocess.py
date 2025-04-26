import numpy as np
import matplotlib.pyplot as plt
import json


try:
    X_sample = np.load("X_train.npy")
    y_sample = np.load("y_train.npy")
    print(f" Loaded X_train.npy with shape {X_sample.shape}")
    print(f" Loaded y_train.npy with shape {y_sample.shape}")
except Exception as e:
    print(f" Error loading .npy files: {e}")
    exit()


try:
    with open("index_to_label.json", "r") as f:
        index_to_label = json.load(f)
    print(f" Loaded label mapping with {len(index_to_label)} classes")
except Exception as e:
    print(f" Error loading label mapping: {e}")
    exit()


indices = np.arange(len(X_sample))
np.random.shuffle(indices)
X_sample = X_sample[indices]
y_sample = y_sample[indices]

#checking to see if lableing is correct , gets random samples
plt.figure(figsize=(15, 4))
for i in range(5):
    label_index = int(y_sample[i])
    label = index_to_label.get(str(label_index), "Unknown")

    plt.subplot(1, 5, i + 1)
    img = np.clip(X_sample[i], 0, 1)
    plt.imshow(img)
    plt.title(label, fontsize=8)
    plt.axis("off")

plt.tight_layout()
plt.show()



