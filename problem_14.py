from helpers import load_text
import numpy as np
import re

EXAMPLE_FILE_PATH = "problem_14_example.txt"
DATA_FILE_PATH = "problem_14_data.txt"


def main():
    def load(fp) -> np.ndarray:
        lines = [l.strip() for l in load_text(fp)]
        pattern = re.compile(r"^p=(\d+),(\d+) v=(\-?\d+),(\-?\d+)$")
        return np.int64([list(map(int, pattern.match(l).groups())) for l in lines])

    rs = load(DATA_FILE_PATH)
    ncols, nrows = 101, 103

    poss, vels = rs[:, :2], rs[:, 2:]

    dt = 100
    poss += vels * dt

    poss[:, 0] %= ncols
    poss[:, 1] %= nrows

    mid_col, mid_row = (ncols - 1) // 2, (nrows - 1) // 2

    q1 = np.sum((poss[:, 0] < mid_col) & (poss[:, 1] < mid_row))
    q2 = np.sum((poss[:, 0] > mid_col) & (poss[:, 1] < mid_row))
    q3 = np.sum((poss[:, 0] < mid_col) & (poss[:, 1] > mid_row))
    q4 = np.sum((poss[:, 0] > mid_col) & (poss[:, 1] > mid_row))

    ans = q1 * q2 * q3 * q4
    print(f"{ans=}")  # Answer: 225648864


main()
