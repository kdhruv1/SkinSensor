import numpy as np
import matplotlib.pyplot as plt

# Load sample data
X_sample = np.load("X_sample.npy")
y_sample = np.load("y_sample.npy")
index_to_label = np.load("index_to_label.npy", allow_pickle=True).item()


indices = np.arange(len(X_sample))
np.random.shuffle(indices)
X_sample = X_sample[indices]
y_sample = y_sample[indices]

# Plot 5 random samples
plt.figure(figsize=(10, 5))
for i in range(5):
    label = index_to_label.get(int(y_sample[i]), "Unknown")
    plt.subplot(1, 5, i + 1)
    plt.imshow(X_sample[i])
    plt.title(label)
    plt.axis("off")
plt.tight_layout()
plt.show()

