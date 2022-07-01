#!/usr/bin/env python3

# this test script takes images on a raspberry pi and tries them

import numpy as np
import os
import subprocess
import sys
import tensorflow as tf

if "RASPI_IP" not in os.environ:
    print("RASPI_IP not found")
    sys.exit()

RASPI_IP = os.environ["RASPI_IP"]

def test(model, class_names, filename):
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

def run_test(model, class_names, base_folder):
    while input("press enter...").strip() == "":
        print("requesting image on raspberry...")
        subprocess.run(["ssh", f"pi@{RASPI_IP}", "sudo", "raspistill", "-o", "/tmp/image.jpg"])
        print("loading image from raspberry...")
        subprocess.run(["rsync", f"pi@{RASPI_IP}:/tmp/image.jpg", "/tmp/image.jpg"])
        test(model, class_names, "/tmp/image.jpg")

