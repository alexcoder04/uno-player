#!/usr/bin/env python3

import os
import random
import math
import sys

def run(folder):
    os.mkdir(f"{folder}/train")
    os.mkdir(f"{folder}/test")

    for label in os.listdir(f"{folder}/raw"):
        files = os.listdir(f"{folder}/raw/{label}")
        random.shuffle(files)
        edge = math.floor(len(files) / 10)
        test_files = files[:edge]
        train_files = files[edge:]

        os.mkdir(f"{folder}/train/{label}")
        for f in train_files:
            os.system(f"cp -v {folder}/raw/{label}/{f} {folder}/train/{label}/{f}")

        os.mkdir(f"{folder}/test/{label}")
        for f in test_files:
            os.system(f"cp -v {folder}/raw/{label}/{f} {folder}/test/{label}/{f}")

if len(sys.argv) <= 1:
    print("you need to pass a folder")
    sys.exit(1)

print("running on " + sys.argv[1])
input("press <enter> to continue")

run(sys.argv[1])

