import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#  Load Saved Preprocessed Data
X_train = np.load("X_train.npy")
X_val = np.load("X_val.npy")
y_train = np.load("y_train.npy")
y_val = np.load("y_val.npy")
index_to_label = np.load("index_to_label.npy", allow_pickle=True).item()

unique_labels = np.unique(y_train)
label_remap = {old: new for new, old in enumerate(unique_labels)}

y_train = np.array([label_remap[label] for label in y_train])
y_val = np.array([label_remap[label] for label in y_val])

index_to_label = {new: index_to_label[old] for old, new in label_remap.items()}

print(f"Train Samples: {X_train.shape[0]} | Val Samples: {X_val.shape[0]}")
print(f"Number of Classes: {len(np.unique(y_train))}")
print(f"Class Distribution: {Counter(y_train)}")

#  Compute Class Weights for Imbalance
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(y_train),
    y=y_train
)
class_weights = dict(enumerate(class_weights))

#  Data Augmentation
datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)

#  Model Definition
base_model = MobileNetV2(include_top=False, input_shape=(224, 224, 3), weights='imagenet')
base_model.trainable = True
for layer in base_model.layers[:100]:
    layer.trainable = False  # freeze base layers

model = Sequential([
    base_model,
    Flatten(),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dense(len(np.unique(y_train)), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

#  Train Model
history = model.fit(
    datagen.flow(X_train, y_train, batch_size=32),
    validation_data=(X_val, y_val),
    epochs=10,
    class_weight=class_weights,
    callbacks=[EarlyStopping(patience=3, restore_best_weights=True)]
)

#  Plot Accuracy & Loss
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.legend()
plt.title("Accuracy")

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.legend()
plt.title("Loss")
plt.tight_layout()
plt.show()

#  Predict and Compare
val_preds = model.predict(X_val)
val_labels = np.argmax(val_preds, axis=1)

#Show Sample Predictions
plt.figure(figsize=(15, 4))
for i in range(5):
    plt.subplot(1, 5, i + 1)
    plt.imshow(X_val[i])
    pred_label = index_to_label.get(val_labels[i], "Unknown")
    true_label = index_to_label.get(int(y_val[i]), "Unknown")
    plt.title(f"P: {pred_label}\nT: {true_label}", fontsize=8)
    plt.axis("off")
plt.tight_layout()
plt.show()
