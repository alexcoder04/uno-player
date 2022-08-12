#!/usr/bin/env python3

import tensorflow as tf
#import test_default as test
import test_raspi as test
#import test_raspi_eval as test

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

print("--- Testing model ---")
test.run_test(model, class_names, base_folder, detect)

