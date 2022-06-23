#!/usr/bin/env python3

import tensorflow as tf
import numpy as np

#base_folder = "../../data/colors/"
base_folder = "../../data/numbers/"

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

def test(filename):
    img = tf.keras.preprocessing.image.load_img(filename, target_size=(32,32))
    X = tf.keras.preprocessing.image.img_to_array(img)
    X = np.expand_dims(X, axis=0)
    images = np.vstack([X])

    val = model.predict(images)
    max_val = -1000
    res = 1000
    for i, v in enumerate(val[0]):
        if v >= max_val:
            max_val = v
            res = i

    print(f"{filename} => {class_names[res]}")

for i in ["./b/9-8.jpg", "./g/4-9.jpg", "./b/2-10.jpg", "./r/r-6.jpg", "./g/2-10.jpg", "./b/2-1.jpg", "./r/1-10.jpg", "./y/8-7.jpg", "./y/7-6.jpg", "./y/1-10.jpg"]:
#for i in ["./1/y4.jpg", "./6/b2.jpg", "./2/r6.jpg", "./n/g10.jpg", "./1/r1.jpg", "./7/y9.jpg", "./2/y7.jpg", "./r/y2.jpg", "./n/y9.jpg", "./4/g10.jpg"]:
    test(base_folder + i)

