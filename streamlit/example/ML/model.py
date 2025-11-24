import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

import tensorflow as tf
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import (
    Conv2D,
    MaxPooling2D,
    Activation,
    Dropout,
    Flatten,
    Dense,
    Input,
)
from keras.utils import to_categorical

(X_train, y_train), (X_val, y_val) = cifar10.load_data()
X_train = X_train / 255.0
X_val = X_val / 255.0

y_train = to_categorical(y_train, 10)
y_val = to_categorical(y_val, 10)

print(X_train.shape)

model = Sequential(
    [
        Conv2D(32, (3, 3), padding="same", input_shape=X_train.shape[1:]),
        Activation("relu"),
        Conv2D(32, (3, 3)),
        Activation("relu"),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        Flatten(),
        Dense(512),
        Activation("relu"),
        Dropout(0.5),
        Dense(10),
        Activation("softmax"),
    ]
)

# model = Sequential(
#     [
#         Input(shape=(32, 32, 3)),
#         Flatten(),
#         Dense(20000, activation="relu"),
#         Dense(10, activation="softmax"),
#     ]
# )

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

model.fit(X_train, y_train, batch_size=64, epochs=10, validation_data=(X_val, y_val))

score = model.evaluate(X_val, y_val, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

model.save("cifar10_model_2.h5")
