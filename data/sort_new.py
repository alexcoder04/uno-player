#!/usr/bin/env python3

import os

os.mkdir("colors_new")
os.mkdir("numbers_new")

def run_color():
    for f in os.listdir("raw_new"):
        [color, number, take] = f.replace(".jpeg", "").split("-")
        if not os.path.isdir(f"colors_new/{color}"):
            os.mkdir(f"colors_new/{color}")
        os.system(f"cp -iv raw_new/{f} colors_new/{color}/{number}-{take}.jpeg")

def run_number():
    for f in os.listdir("raw_new"):
        [color, number, take] = f.replace(".jpeg", "").split("-")
        if not os.path.isdir(f"numbers_new/{number}"):
            os.mkdir(f"numbers_new/{number}")
        os.system(f"cp -iv raw_new/{f} numbers_new/{number}/{color}-{take}.jpeg")

run_color()
run_number()

