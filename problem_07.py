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
        qty_combinations = 3 ** (qty_numbers - 1)

        for iops in [
            [i // (3**n) % 3 for n in range(qty_numbers - 1)]
            for i in range(qty_combinations)
        ]:
            this_result = numbers[0]
            for iop, num in zip(iops, numbers[1:]):
                match iop:
                    case 0:
                        this_result = this_result + num
                    case 1:
                        this_result = this_result * num
                    case 2:
                        this_result = int(f"{this_result}{num}")

            if this_result == result:
                return True

        return False

    sum = 0
    for idx, line in enumerate(lines):
        print(f"{idx}/{len(lines)}", end="\r")
        result, numbers = parse_line(line)
        is_valid = check_equation(result, numbers)
        if is_valid:
            sum += result

    print("")
    print(f"{sum=}")  # Answer: 159490400628354


main()
