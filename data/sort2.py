#!/usr/bin/env python3

import sys
import os

colors = ["b", "r", "y", "g", "j"]
numbers = [str(i) for i in range(0, 10)] + ["n", "r", "+2", "+4", "j"]

def run_color():
    os.mkdir("./trash/colors_1")
    os.mkdir("./trash/colors_2")
    for c in colors:
        os.mkdir("./trash/colors_1/" + c)
        os.mkdir("./trash/colors_2/" + c)
        for i in os.listdir("./raw"):
            if i.startswith(c):
                if int(i.split(".")[0].split("-")[1]) % 10 == 0:
                    os.system(f"cp -v ./raw/{i} ./trash/colors_1/{c}/{i[1:]}")
                else:
                    os.system(f"cp -v ./raw/{i} ./trash/colors_2/{c}/{i[1:]}")

def run_number():
    os.mkdir("./trash/numbers_1")
    os.mkdir("./trash/numbers_2")
    for n in numbers:
        os.mkdir("./trash/numbers_1/" + n)
        os.mkdir("./trash/numbers_2/" + n)
        for i in os.listdir("./raw"):
            if i[1:].startswith(n):
                if int(i.split(".")[0].split("-")[1]) % 10 == 0:
                    os.system(f"cp -v ./raw/{i} ./trash/numbers_1/{n}/{i[0]}{i.split('-')[1]}")
                else:
                    os.system(f"cp -v ./raw/{i} ./trash/numbers_2/{n}/{i[0]}{i.split('-')[1]}")

print(colors)
print(numbers)

if "colors" in sys.argv:
    run_color()

if "numbers" in sys.argv:
    run_number()

