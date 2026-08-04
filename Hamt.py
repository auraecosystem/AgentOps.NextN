import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

class HAMTNode:
    def __init__(self, bitmap=0, children=None, value=None):
        self.bitmap = bitmap
        self.children = children or []
        self.value = value

class HAMT:
    BITS = 5
    MASK = (1 << BITS) - 1

    def __init__(self):
        self.root = HAMTNode()

    def _index(self, h, shift):
        return (h >> shift) & self.MASK

    def _popcount(self, x):
        return bin(x).count("1")

    def insert(self, key, value):
        h = hash(key)
        self.root = self._insert(self.root, key, value, h, 0)

    def _insert(self, node, key, value, h, shift):
        idx = self._index(h, shift)
        bit = 1 << idx

        if node.bitmap & bit == 0:
            node.bitmap |= bit
            node.children.insert(self._popcount(node.bitmap & (bit - 1)), HAMTNode(value=(key, value)))
            return node

        pos = self._popcount(node.bitmap & (bit - 1))
        child = node.children[pos]

        if child.value and child.value[0] == key:
            child.value = (key, value)
        else:
            node.children[pos] = self._insert(child, key, value, h, shift + self.BITS)
        return node

    def lookup(self, key):
        h = hash(key)
        return self._lookup(self.root, key, h, 0)

    def _lookup(self, node, key, h, shift):
        idx = self._index(h, shift)
        bit = 1 << idx
        if node.bitmap & bit == 0:
            return None
        pos = self._popcount(node.bitmap & (bit - 1))
        child = node.children[pos]
        if child.value:
            return child.value[1] if child.value[0] == key else None
        return self._lookup(child, key, h, shift + self.BITS)


# Example: store MNIST samples and model checkpoints
(x_train, y_train), _ = mnist.load_data()

hamt = HAMT()

# Store a few samples
for i in range(10):
    hamt.insert(f"digit_{i}", {"image": x_train[i], "label": y_train[i]})

# Build and train a simple model
model = Sequential([
    Flatten(input_shape=(28, 28)),
    Dense(128, activation="relu"),
    Dense(10, activation="softmax")
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(x_train[:1000], y_train[:1000], epochs=1, verbose=0)

# Save checkpoint (weights + config)
checkpoint = {
    "weights": model.get_weights(),
    "config": model.get_config(),
    "epoch": 1,
    "accuracy": model.evaluate(x_train[:200], y_train[:200], verbose=0)[1]
}
hamt.insert("checkpoint_v1", checkpoint)

# Retrieve checkpoint
ckpt = hamt.lookup("checkpoint_v1")
print("Checkpoint accuracy:", ckpt["accuracy"])
