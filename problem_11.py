from helpers import load_text
from functools import cache
import time


FILE_PATH = "problem_11_data.txt"
NUM_BLINKS = 75


def main():
    stones = list(map(int, load_text(FILE_PATH)[0].strip().split()))

    @cache
    def stone_value(stone, nblinks) -> int:
        if stone == 0:
            next_stones = [1]
        elif len(digits := str(stone)) % 2 == 0:
            left = int(digits[0 : len(digits) // 2])
            right = int(digits[len(digits) // 2 :])
            next_stones = [left, right]
        else:
            next_stones = [2024 * stone]

        if nblinks == 1:
            return len(next_stones)
        else:
            return sum(stone_value(s, nblinks - 1) for s in next_stones)

    t0 = time.time()
    answer = sum(stone_value(s, NUM_BLINKS) for s in stones)
    print(f"{answer=}")
    print(f"dt: {time.time()- t0:.3f} seconds")


main()
