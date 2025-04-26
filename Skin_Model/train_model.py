import os
import json
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

#  forcing the cpu as gpu runs out of ram
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# loading data
X_train = np.load("X_train.npy")
X_val = np.load("X_val.npy")
y_train = np.load("y_train.npy")
y_val = np.load("y_val.npy")

with open("index_to_label.json") as f:
    index_to_label = json.load(f)

NUM_CLASSES = len(np.unique(y_train))
IMG_SIZE = 224


if X_train.shape[1] != IMG_SIZE:
    from tensorflow.image import resize
    X_train = np.array([resize(img, (IMG_SIZE, IMG_SIZE)).numpy() for img in X_train])
    X_val = np.array([resize(img, (IMG_SIZE, IMG_SIZE)).numpy() for img in X_val])

# weights for classes
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train),
    y=y_train
)
class_weights = dict(enumerate(class_weights))

# mixup and cutmix
def sample_beta_distribution(size, concentration=0.3):
    return np.random.beta(concentration, concentration, size)

def mixup_cutmix(x, y, alpha=0.2):
    lam = sample_beta_distribution(1, alpha)[0]
    batch_size = x.shape[0]
    idx = np.random.permutation(batch_size)
    x1, y1 = np.array(x), np.array(y)
    x2, y2 = x1[idx], y1[idx]

    if np.random.rand() > 0.5:
        mixed_x = lam * x1 + (1 - lam) * x2
    else:
        cut_w = int(IMG_SIZE * np.sqrt(1 - lam))
        cut_h = int(IMG_SIZE * np.sqrt(1 - lam))
        cx = np.random.randint(IMG_SIZE)
        cy = np.random.randint(IMG_SIZE)

        x1_copy = x1.copy()
        x1_copy[:, max(0, cy - cut_h // 2):min(IMG_SIZE, cy + cut_h // 2),
        max(0, cx - cut_w // 2):min(IMG_SIZE, cx + cut_w // 2), :] = \
            x2[:, max(0, cy - cut_h // 2):min(IMG_SIZE, cy + cut_h // 2),
            max(0, cx - cut_w // 2):min(IMG_SIZE, cx + cut_w // 2), :]
        mixed_x = x1_copy

    return mixed_x, lam * y1 + (1 - lam) * y2

def mixed_generator(X, y, batch_size):
    while True:
        idx = np.random.choice(len(X), batch_size)
        x_batch = np.array(X[idx])  # ✅ Force numpy
        y_batch = to_categorical(y[idx], NUM_CLASSES)
        mixed_x, mixed_y = mixup_cutmix(x_batch, y_batch)
        yield mixed_x, mixed_y

# model
base_model = MobileNetV2(input_shape=(IMG_SIZE, IMG_SIZE, 3), include_top=False, weights='imagenet')
base_model.trainable = True
for layer in base_model.layers[:50]:  # Freeze first few layers
    layer.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(NUM_CLASSES, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# configuration for training (use this to try and get better accacury )
EPOCHS = 30
BATCH_SIZE = 32
y_val_cat = to_categorical(y_val, NUM_CLASSES)

callbacks = [
    EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3),
    ModelCheckpoint("best_model.h5", monitor='val_accuracy', save_best_only=True)
]

# trainingn
history = model.fit(
    mixed_generator(X_train, y_train, BATCH_SIZE),
    steps_per_epoch=len(X_train) // BATCH_SIZE,
    validation_data=(X_val, y_val_cat),
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=callbacks
)

# evaluation
val_preds = model.predict(X_val)
y_pred = np.argmax(val_preds, axis=1)

print("\n Classification Report:")
print(classification_report(y_val, y_pred, target_names=[index_to_label[str(i)] for i in range(NUM_CLASSES)]))

# confusion matrix
cm = confusion_matrix(y_val, y_pred, normalize='true')
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=list(index_to_label.values()))
fig, ax = plt.subplots(figsize=(12, 8))
disp.plot(cmap='Blues', ax=ax, xticks_rotation=45)
plt.title(" Normalized Confusion Matrix")
plt.tight_layout()
plt.show()

# accuracy and plots
plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.title("Accuracy")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title("Loss")
plt.legend()
plt.tight_layout()
plt.show()

#  prediction
import random
sample_indices = random.sample(range(len(X_val)), 6)
for idx in sample_indices:
    image = X_val[idx]
    true_label = index_to_label[str(y_val[idx])]
    pred_probs = model.predict(np.expand_dims(image, axis=0), verbose=0)[0]
    pred_idx = np.argmax(pred_probs)
    pred_label = index_to_label[str(pred_idx)]
    confidence = pred_probs[pred_idx] * 100

    plt.figure()
    plt.imshow(image)
    plt.axis('off')
    plt.title(f"True: {true_label}\nPredicted: {pred_label} ({confidence:.1f}%)")
    plt.show()

# saving
print(" Model saved as best_model.h5")