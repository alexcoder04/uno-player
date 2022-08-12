#!/usr/bin/env python3

# default test, just trying out some images from training dataset

import numpy as np
import tensorflow as tf

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

def run_test(model, class_names, base_folder, detect):
    if detect == "colors":
        for i in ["./b/9-8.jpg", "./g/4-9.jpg", "./b/2-10.jpg", "./r/r-6.jpg", "./g/2-10.jpg", "./b/2-1.jpg", "./r/1-10.jpg", "./y/8-7.jpg", "./y/7-6.jpg", "./y/1-10.jpg"]:
            test(model, class_names, base_folder + i)
        return
    if detect == "numbers":
        for i in ["./1/y4.jpg", "./6/b2.jpg", "./2/r6.jpg", "./n/g10.jpg", "./1/r1.jpg", "./7/y9.jpg", "./2/y7.jpg", "./r/y2.jpg", "./n/y9.jpg", "./4/g10.jpg"]:
            test(model, class_names, base_folder + i)
        return
    print("unknown arg")

