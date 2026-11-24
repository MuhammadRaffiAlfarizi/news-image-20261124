#!/usr/bin/env python3
"""Entry program: copy this repository's entry.png to /output/entry.png.

Standard library only. The image is already rendered; this program just
places it where the grader expects it.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
