import re
import numpy as np
from helpers import load_text


FILE_PATH = "problem_03_data.txt"
# FILE_PATH = "problem_03_example.txt"


def main():
    txt = "\n".join(load_text(FILE_PATH))

    re_pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

    sum = 0
    for m in re_pattern.finditer(txt):
        numA, numB = int(m.group(1)), int(m.group(2))
        sum += numA * numB

    print(f"{sum=}")  # Answer: 174960292


main()
