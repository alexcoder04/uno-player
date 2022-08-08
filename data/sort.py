#!/usr/bin/env python3

import sys
import os

colors = ["b", "r", "y", "g", "j"]
numbers = [str(i) for i in range(0, 10)] + ["n", "r", "+2", "+4", "j"]

def run_color():
    os.mkdir("./colors")
    for c in colors:
        os.mkdir("./colors/" + c)
        for i in os.listdir("./raw"):
            if i.startswith(c):
                os.system(f"cp -v ./raw/{i} ./colors/{c}/{i[1:]}")

def run_number():
    os.mkdir("./numbers")
    for n in numbers:
        os.mkdir("./numbers/" + n)
        for i in os.listdir("./raw"):
            if i[1:].startswith(n):
                os.system(f"cp -v ./raw/{i} ./numbers/{n}/{i[0]}{i.split('-')[1]}")

print(colors)
print(numbers)

if "colors" in sys.argv:
    run_color()

if "numbers" in sys.argv:
    run_number()

