#!/usr/bin/env python3

import tensorflow as tf
import os
import numpy as np

detect = "numbers"
#detect = "colors"
#detect = "numbers_new"
#detect = "colors_new"
base_folder = f"../../data/{detect}/"
saved_folder = f"../saved/{detect}"
#color_mode = "grayscale"
color_mode = "rgb"

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

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

print("--- Loading model ---")
model = tf.keras.models.load_model(f"{saved_folder}/model.h5")
print("--- Loading weights ---")
model.load_weights(f"{saved_folder}/model_weights")

all_counter = 0
right_counter = 0
for c in os.listdir("/home/alex/_/Uno/TEST_IMG"):
    for i in os.listdir(f"/home/alex/_/Uno/TEST_IMG/{c}"):
        img = tf.keras.preprocessing.image.load_img(f"/home/alex/_/Uno/TEST_IMG/{c}/{i}", target_size=(32,32))
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
    
        if detect == "numbers":
            if class_names[res] == c[1:]:
                print(f"{c}/{i} => OK")
                right_counter += 1
            else:
                print(f"{c}/{i} => WRONG")
        else:
            if class_names[res] == c[1]:
                print(f"{c}/{i} => OK")
                right_counter += 1
            else:
                print(f"{c}/{i} => WRONG")
        all_counter += 1


print(f"{right_counter}/{all_counter} ({right_counter/all_counter*100}%)")

