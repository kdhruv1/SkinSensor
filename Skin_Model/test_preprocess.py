import numpy as np
import matplotlib.pyplot as plt

# ✅ Load the Sample Data
X_sample = np.load("X_sample.npy")
y_sample = np.load("y_sample.npy")

# ✅ Display 5 Sample Images with Labels
plt.figure(figsize=(10, 5))

for i in range(5):
    plt.subplot(1, 5, i + 1)
    plt.imshow(X_sample[i])  # Show image
    plt.title(f"Label: {y_sample[i]}")
    plt.axis("off")

plt.show()
