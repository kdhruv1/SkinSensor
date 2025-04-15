import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow.keras.backend as K

# ==== Custom Focal Loss ====
def sparse_categorical_focal_loss(gamma=2.0, alpha=0.25):
    def loss_fn(y_true, y_pred):
        y_true = tf.cast(y_true, tf.int32)
        y_true = tf.one_hot(y_true, depth=tf.shape(y_pred)[-1])
        y_pred = K.clip(y_pred, K.epsilon(), 1.0 - K.epsilon())
        cross_entropy = -y_true * K.log(y_pred)
        loss = alpha * K.pow(1 - y_pred, gamma) * cross_entropy
        return K.sum(loss, axis=1)
    return loss_fn

# ==== Load Preprocessed Data ====
X_train = np.load("X_train.npy")
X_val = np.load("X_val.npy")
y_train = np.load("y_train.npy")
y_val = np.load("y_val.npy")
index_to_label = np.load("index_to_label.npy", allow_pickle=True).item()

# ==== Label Remapping ====
unique_labels = np.unique(y_train)
label_remap = {old: new for new, old in enumerate(unique_labels)}
y_train = np.array([label_remap[label] for label in y_train])
y_val = np.array([label_remap[label] for label in y_val])
index_to_label = {new: index_to_label[old] for old, new in label_remap.items()}

print(f"Train Samples: {X_train.shape[0]} | Val Samples: {X_val.shape[0]}")
print(f"Number of Classes: {len(np.unique(y_train))}")
print(f"Class Distribution: {Counter(y_train)}")

# ==== Class Weights ====
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(y_train),
    y=y_train
)
class_weights = dict(enumerate(class_weights))

# ==== Data Augmentation ====
datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)

# ==== Model Definition ====
base_model = MobileNetV2(include_top=False, input_shape=(224, 224, 3), weights='imagenet')
base_model.trainable = True
for layer in base_model.layers[:100]:
    layer.trainable = False  # Freeze base layers

model = Sequential([
    base_model,
    Flatten(),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dense(len(np.unique(y_train)), activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=5e-5),
    loss=sparse_categorical_focal_loss(gamma=2.0, alpha=0.25),
    metrics=['accuracy']
)

# ==== Training ====
history = model.fit(
    datagen.flow(X_train, y_train, batch_size=32),
    validation_data=(X_val, y_val),
    epochs=30,
    class_weight=class_weights,
    callbacks=[
        EarlyStopping(patience=5, restore_best_weights=True),
        ReduceLROnPlateau(patience=2, factor=0.5, verbose=1)
    ]
)

# ==== Accuracy & Loss Plot ====
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

# ==== Predictions ====
val_preds = model.predict(X_val)
val_labels = np.argmax(val_preds, axis=1)

# ==== Sample Output ====
plt.figure(figsize=(15, 4))
for i in range(10):
    plt.subplot(1, 5, i + 1)
    plt.imshow(X_val[i])
    pred_label = index_to_label.get(val_labels[i], "Unknown")
    true_label = index_to_label.get(int(y_val[i]), "Unknown")
    plt.title(f"P: {pred_label}\nT: {true_label}", fontsize=8)
    plt.axis("off")
plt.tight_layout()
plt.show()
