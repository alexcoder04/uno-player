#!/usr/bin/env python3

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np

base_folder = "../../data/colors/"

train = ImageDataGenerator(rescale= 1/255)
validation = ImageDataGenerator(rescale= 1/255)

train_dataset = train.flow_from_directory(base_folder + "train/", target_size=(32,32),batch_size=10, class_mode="categorical")
test_dataset = validation.flow_from_directory(base_folder + "test/", target_size=(32,32),batch_size=10, class_mode="categorical")

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3,3), activation="relu", input_shape=(32,32,3)),
    tf.keras.layers.MaxPool2D(2, 2),

    tf.keras.layers.Conv2D(32, (3,3), activation="relu"),
    tf.keras.layers.MaxPool2D(2, 2),

    tf.keras.layers.Conv2D(64, (3,3), activation="relu"),
    tf.keras.layers.MaxPool2D(2, 2),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
    ])

model.compile(loss="binary_crossentropy", optimizer="adam" ,metrics=["accuracy"])

model_fit = model.fit(train_dataset, steps_per_epoch=3, epochs=5, validation_data=test_dataset)

img = image.load_img("./colors/test/g/1-2.jpg", target_size=(32,32))
X = image.img_to_array(img)
X = np.expand_dims(X, axis=0)
images = np.vstack([X])

val = model.predict(images)

print(val)
print(train_dataset.class_indices)


