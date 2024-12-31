import numpy as np
from helpers import load_text
from itertools import permutations

# FILE_PATH = "problem_07_example.txt"
FILE_PATH = "problem_07_data.txt"


def main():
    lines = [line.strip() for line in load_text(FILE_PATH)]

    def parse_line(line: str):
        parts = line.split(":")
        result = int(parts[0])
        numbers = [int(s) for s in parts[1].strip().split(" ")]
        return result, numbers

    def check_equation(result: int, numbers: list[int]) -> bool:
        qty_numbers = len(numbers)
        qty_combinations = 2 ** (qty_numbers - 1)

        for iops in [
            [i // (2**n) % 2 for n in range(qty_numbers - 1)]
            for i in range(qty_combinations)
        ]:
            this_result = numbers[0]
            for iop, num in zip(iops, numbers[1:]):
                this_result = this_result + num if iop == 0 else this_result * num

            if this_result == result:
                return True

        return False

    sum = 0
    for line in lines:
        result, numbers = parse_line(line)
        is_valid = check_equation(result, numbers)
        if is_valid:
            sum += result

    print(f"{sum=}")  # Answer: 20281182715321


main()
