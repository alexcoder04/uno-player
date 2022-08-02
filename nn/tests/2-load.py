#!/usr/bin/env python3

import tensorflow as tf
import test_default as test
#import test_raspi as test

#detect = "numbers"
detect = "colors"
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

print("--- Loading model ---")
model = tf.keras.models.load_model("../saved/model.h5")
print("--- Loading weights ---")
model.load_weights("../saved/model_weights")

print("--- Testing model ---")
test.run_test(model, class_names, base_folder, detect)

