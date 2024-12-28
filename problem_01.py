import numpy as np
from helpers import load_text
import math

# FILE_PATH = "problem_01_example.txt"
FILE_PATH = "problem_01_data1.txt"


def main():
    def extract_numbers(line: str) -> tuple[int, int]:
        parts = line.split()
        assert len(parts) == 2
        return int(parts[0]), int(parts[-1])

    numbers = np.array(
        [extract_numbers(line.strip()) for line in load_text(FILE_PATH) if line != ""],
        dtype=np.int32,
    )

    assert numbers.shape[1] == 2

    left_numbers = np.sort(numbers[:, 0])
    right_numbers = np.sort(numbers[:, 1])

    sorted_numbers = np.vstack([left_numbers, right_numbers]).transpose()

    distances = np.abs(np.diff(sorted_numbers, axis=1))

    print(np.sum(distances))


main()
