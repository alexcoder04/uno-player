
"""
Default Camera Interface for entering the cards and other data
"""

import numpy as np
import requests
import tensorflow as tf


RASPI_IP = "192.168.178.39"
BASE_PATH = "../nn/saved"
COLORS_PATH = f"{BASE_PATH}/colors"
NUMBERS_PATH = f"{BASE_PATH}/numbers"


c_ds = tf.keras.utils.image_dataset_from_directory(
    f"../data/colors",
    color_mode="rgb",
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(32, 32),
    batch_size=10)
n_ds = tf.keras.utils.image_dataset_from_directory(
    f"../data/numbers",
    color_mode="rgb",
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(32, 32),
    batch_size=10)

c_class_names = c_ds.class_names
n_class_names = n_ds.class_names

def get_max(val):
    max_val = -1000
    res = 1000
    for i, v in enumerate(val[0]):
        if v >= max_val:
            max_val = v
            res = i
    return res


class CameraDataloader:
    def __init__(self) -> None:
        self.c_model = tf.keras.models.load_model(f"{COLORS_PATH}/model.h5")
        self.c_model.load_weights(f"{COLORS_PATH}/model_weights")
        self.n_model = tf.keras.models.load_model(f"{NUMBERS_PATH}/model.h5")
        self.n_model.load_weights(f"{NUMBERS_PATH}/model_weights")

    def get_players_number(self) -> int:
        while True:
            try:
                return int(input("Players number: "))
            except ValueError:
                print("Sorry, this is not a number")
                continue
    
    def download_image(self):
        resp = requests.get("http://"+RASPI_IP+":8000/image.jpeg")
        with open("/tmp/image.jpeg", "wb") as f:
            f.write(resp.content)


    def read_card(self, prompt: str) -> (str, str, bool):
        # TODO load image from raspberry
        # TODO process
        print(prompt)
        input("Hold the card in front of camera and press enter...")
        self.download_image()
        img = tf.keras.preprocessing.image.load_img("/tmp/image.jpeg", target_size=(32,32))
        X = tf.keras.preprocessing.image.img_to_array(img)
        X = np.expand_dims(X, axis=0)
        images = np.vstack([X])
        c_val = self.c_model.predict(images)
        n_val = self.n_model.predict(images)
        c_res = get_max(c_val)
        n_res = get_max(n_val)
        print(f"=> {c_class_names[c_res]}")
        for i, v in enumerate(c_val[0]):
            print(f"{c_class_names[i]} = {v}")
        inp = input("correct: ")
        if inp == "":
            color = c_class_names[c_res]
        else:
            color = inp
        print(f"=> {n_class_names[n_res]}")
        for i, v in enumerate(n_val[0]):
            print(f"{n_class_names[i]} = {v}")
        inp = input("correct: ")
        if inp == "":
            number = n_class_names[n_res]
        else:
            number = inp
        special = True if color == "s" else False
        return color, number, special
        #while True:
        #    try:
        #        [color, number] = input(prompt).split(",")
        #    except ValueError:
        #        print("Sorry, cannot read your input")
        #        continue
        #    color, number = color.strip(), number.strip()
        #    if color not in ("r", "g", "b", "y", "s"):
        #        print("Sorry, invalid color, use (r,g,b,y,s)")
        #        continue
        #    if color != "s" and number not in ("0","1","2","3","4","5","6","7","8","9","r","n","+2","j"):
        #        print("Sorry, invalid number, use (0,1,2,3,4,5,6,7,8,9,r,n,+2,j)")
        #        continue
        #    if color == "s" and number not in ("j","+4"):
        #        print("Sorry, invalid number, use (j,+4)")
        #        continue
        #    special = True if color == "s" else False
        #    return color, number, special

    def get_how_many_to_pull(self) -> int:
        inp = input("Do I have to pull? If so, how much: ")
        try:
            return int(inp)
        except ValueError:
            return 0

    def clear(self) -> None:
        return
        #input("Press <enter> to clear the screen and continue")
        #os.system("clear")

