import os
import json
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, Callback
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from tensorflow.keras.preprocessing.image import ImageDataGenerator


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


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


class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(y_train),
    y=y_train
)
class_weights = dict(enumerate(class_weights))

datagen = ImageDataGenerator(
    rotation_range=20,
    zoom_range=0.15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    horizontal_flip=True,
    fill_mode="nearest"
)

train_gen = datagen.flow(
    X_train, to_categorical(y_train, NUM_CLASSES), batch_size=32
)
val_data = (X_val, to_categorical(y_val, NUM_CLASSES))


base_model = EfficientNetB0(
    include_top=False,
    weights="imagenet",
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(NUM_CLASSES, activation="softmax")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-4),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

class UnfreezeCallback(Callback):
    def __init__(self, unfreeze_at_epoch, base_model):
        super().__init__()
        self.unfreeze_at_epoch = unfreeze_at_epoch
        self.base_model = base_model

    def on_epoch_begin(self, epoch, logs=None):
        if epoch == self.unfreeze_at_epoch:
            print("\n unfreezing last 30 layers of EfficientNetB0...")
            for layer in self.base_model.layers[-30:]:
                layer.trainable = True
            self.model.compile(
                optimizer=tf.keras.optimizers.Adam(1e-5),
                loss="categorical_crossentropy",
                metrics=["accuracy"]
            )


callbacks = [
    EarlyStopping(monitor="val_accuracy", patience=5, restore_best_weights=True),
    ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, verbose=1),
    ModelCheckpoint("best_efficientnet_model.h5", monitor="val_accuracy", save_best_only=True),
    UnfreezeCallback(unfreeze_at_epoch=10, base_model=base_model)
]


history = model.fit(
    train_gen,
    validation_data=val_data,
    epochs=40,
    class_weight=class_weights,
    callbacks=callbacks
)


val_preds = model.predict(X_val)
y_pred = np.argmax(val_preds, axis=1)

print("\n classification report:")
print(classification_report(y_val, y_pred, target_names=[index_to_label[str(i)] for i in range(NUM_CLASSES)]))


cm = confusion_matrix(y_val, y_pred, normalize="true")
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=list(index_to_label.values()))
fig, ax = plt.subplots(figsize=(12, 8))
disp.plot(cmap="blues", ax=ax, xticks_rotation=45)
plt.title(" normalized confusion matrix")
plt.tight_layout()
plt.show()


plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"], label="Train Accuracy")
plt.plot(history.history["val_accuracy"], label="Val Accuracy")
plt.legend()
plt.title("accuracy Over epochs")

plt.subplot(1, 2, 2)
plt.plot(history.history["loss"], label="Train Loss")
plt.plot(history.history["val_loss"], label="Val Loss")
plt.legend()
plt.title("loss Over epochs")

plt.tight_layout()
plt.show()


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
    plt.axis("off")
    plt.title(f"True: {true_label}\nPredicted: {pred_label} ({confidence:.1f}%)")
    plt.show()


print(" training complete. best weights saved to 'best_efficientnet_model.h5'")

