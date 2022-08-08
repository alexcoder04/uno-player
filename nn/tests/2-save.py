#!/usr/bin/env python3

import tensorflow as tf

#detect = "numbers"
detect = "colors"
#detect = "colors_new"
#detect = "numbers_new"
base_folder = f"../../data/{detect}/"
save_folder = f"../saved/{detect}"

color_mode="rgb"
#color_mode="grayscale"

if detect.startswith("colors"):
    epochs = 3
if detect.startswith("numbers"):
    epochs = 6

epochs=2

print("--- Loading data ---")

train_ds = tf.keras.utils.image_dataset_from_directory(
    base_folder,
    color_mode=color_mode,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(32, 32),
    batch_size=10)

val_ds = tf.keras.utils.image_dataset_from_directory(
    base_folder,
    color_mode=color_mode,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(32, 32),
    batch_size=10)

class_names = train_ds.class_names

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

print("--- Creating model ---")

def get_input_shape(color_mode):
    if color_mode == "rgb":
        return (32, 32, 3)
    return (32, 32, 1)

model = tf.keras.models.Sequential([
    tf.keras.layers.Rescaling(1./255, input_shape=get_input_shape(color_mode)),
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

print("--- Training model ---")

history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

print("--- Saving model ---")

model.save(f"{save_folder}/model.h5")
model.save_weights(f"{save_folder}/model_weights")
print("Done")

