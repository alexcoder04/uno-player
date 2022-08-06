#!/usr/bin/env python3

import sys
import os
import random

if "colors" in sys.argv:
    for c in os.listdir("./colors"):
        for f in os.listdir(f"./colors/{c}"):
            if random.randint(0, 1) == 0:
                print(f"{c}/{f}")
                os.system(f"mogrify -rotate 180 ./colors/{c}/{f}")

if "numbers" in sys.argv:
    for c in os.listdir("./numbers"):
        for f in os.listdir(f"./numbers/{c}"):
            if random.randint(0, 1) == 0:
                print(f"{c}/{f}")
                os.system(f"mogrify -rotate 180 ./numbers/{c}/{f}")

