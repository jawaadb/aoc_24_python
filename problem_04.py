import numpy as np
from helpers import load_text

# FILE_PATH = "problem_04_example2.txt"
FILE_PATH = "problem_04_data.txt"


def main():
    ch_array: np.ndarray = np.array(
        [[letter for letter in line.strip()] for line in load_text(FILE_PATH)],
        dtype="S1",
    )

    fwd_mask = np.isin(np.arange(9).reshape(3, 3), [0, 4, 8])
    back_mask = np.isin(np.arange(9).reshape(3, 3), [2, 4, 6])

    target_word = np.array("M A S".split(), dtype="S1")
    target_word_reversed = target_word[-1::-1]

    def check_sub_array(arr: np.ndarray) -> bool:
        str_fwd = arr[fwd_mask]
        str_back = arr[back_mask]
        fwd_found = np.all(str_fwd == target_word) | np.all(
            str_fwd == target_word_reversed
        )
        back_found = np.all(str_back == target_word) | np.all(
            str_back == target_word_reversed
        )
        return fwd_found & back_found

    found_count = 0
    nrows, ncols = ch_array.shape
    for irow in range(1, nrows - 1):
        for icol in range(1, ncols - 1):
            sub_array = ch_array[(irow - 1) : (irow + 2), (icol - 1) : (icol + 2)]
            if check_sub_array(sub_array):
                found_count += 1

    print(f"{found_count=}")  # Answer: 1921


main()
