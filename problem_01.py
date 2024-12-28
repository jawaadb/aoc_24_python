import numpy as np
from helpers import load_text
import math

# FILE_PATH = "problem_01_example2.txt"
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

    occurrences = np.array(
        [np.sum(num == numbers[:, 1]) for num in numbers[:, 0]], dtype=np.int32
    )

    print(np.sum(numbers[:, 0] * occurrences))


main()
