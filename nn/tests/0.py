#!/usr/bin/env python3

import tensorflow as tf
#import test_default as test
import test_raspi as test

detect = "numbers"
base_folder = f"../../data/{detect}/"

train_ds = tf.keras.utils.image_dataset_from_directory(
    base_folder,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(32, 32),
    batch_size=10)

val_ds = tf.keras.utils.image_dataset_from_directory(
    base_folder,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(32, 32),
    batch_size=10)

class_names = train_ds.class_names

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

model = tf.keras.models.Sequential([
    tf.keras.layers.Rescaling(1./255, input_shape=(32, 32, 3)),
    tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(len(class_names))
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

epochs=5
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

test.run_test(model, class_names, base_folder, detect)

