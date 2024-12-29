import re
import numpy as np
from helpers import load_text


FILE_PATH = "problem_03_data.txt"
# FILE_PATH = "problem_03_example2.txt"


def main():
    txt = "\n".join(load_text(FILE_PATH))

    do_pattern = r"(do)\(\)"
    dont_pattern = r"(don't)\(\)"
    mul_pattern = r"(mul)\((\d{1,3}),(\d{1,3})\)"
    re_pattern = re.compile(f"(({mul_pattern})|({do_pattern})|({dont_pattern}))")

    mul_enabled = True
    sum = 0
    for m in re_pattern.finditer(txt):
        is_do = m.group(7) == "do"
        is_dont = m.group(9) == "don't"
        is_mul = m.group(3) == "mul"

        if is_do:
            mul_enabled = True
            continue
        elif is_dont:
            mul_enabled = False
            continue

        assert is_mul

        if mul_enabled == False:
            continue

        numA, numB = int(m.group(4)), int(m.group(5))
        sum += numA * numB

    print(f"{sum=}")  # Answer: 56275602


main()
