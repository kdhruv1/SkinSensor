import numpy as np
import json


with open("label_to_index.json", "r") as f:
    label_to_index = json.load(f)

with open("index_to_label.json", "r") as f:
    index_to_label = json.load(f)

pigmentation_idx = label_to_index.get("Pigmentation_Disorder", None)

if pigmentation_idx is None:
    print(" No pigmentation disorder found. No patch needed.")
    exit()

X_train = np.load("X_train.npy")
y_train = np.load("y_train.npy")
X_val = np.load("X_val.npy")
y_val = np.load("y_val.npy")


train_filter = y_train != pigmentation_idx
val_filter = y_val != pigmentation_idx

X_train = X_train[train_filter]
y_train = y_train[train_filter]
X_val = X_val[val_filter]
y_val = y_val[val_filter]


unique_labels = sorted(set(y_train))
new_label_map = {old: new for new, old in enumerate(unique_labels)}
y_train = np.array([new_label_map[y] for y in y_train])
y_val = np.array([new_label_map[y] for y in y_val])


index_to_label = {str(new_idx): label for label, new_idx in
                  {label: new_label_map[idx] for label, idx in label_to_index.items() if label != "Pigmentation_Disorder"}.items()}
label_to_index = {label: int(idx) for idx, label in index_to_label.items()}


np.save("X_train.npy", X_train)
np.save("y_train.npy", y_train)
np.save("X_val.npy", X_val)
np.save("y_val.npy", y_val)

with open("label_to_index.json", "w") as f:
    json.dump(label_to_index, f)

with open("index_to_label.json", "w") as f:
    json.dump(index_to_label, f)
#
print(f" patch completed successfully!")
print(f" total final classes: {len(label_to_index)}")
print(f" train Samples: {len(X_train)} | val samples: {len(X_val)}")
