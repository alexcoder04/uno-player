#!/usr/bin/env python3

import sys
import os

colors = ["b", "r", "y", "g", "j"]
numbers = [str(i) for i in range(1, 9)] + ["n", "r", "+2", "+4", "j"]

def run_color():
    os.mkdir("./colors/raw")
    for c in colors:
        os.mkdir("./colors/raw/" + c)
        for i in os.listdir("./raw"):
            if i.startswith(c):
                os.system(f"cp -v ./raw/{i} ./colors/raw/{c}/{i[1:]}")

def run_number():
    for n in numbers:
        os.mkdir("./numbers/raw/" + n)
        for i in os.listdir("./raw"):
            if i[1:].startswith(n):
                os.system(f"cp -v ./raw/{i} ./numbers/raw/{n}/{i[0]}{i.split('-')[1]}")

try:
    os.mkdir("./colors")
    os.mkdir("./numbers")
except FileExistsError:
    print("./sorted already exists")

print(colors)
print(numbers)

if "color" in sys.argv:
    run_color()

if "number" in sys.argv:
    run_number()

