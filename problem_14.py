from helpers import load_text
import numpy as np
import re

DATA_FILE_PATH = "problem_14_data.txt"


def main():
    def load(fp) -> np.ndarray:
        lines = [l.strip() for l in load_text(fp)]
        pattern = re.compile(r"^p=(\d+),(\d+) v=(\-?\d+),(\-?\d+)$")
        return np.int64([list(map(int, pattern.match(l).groups())) for l in lines])

    rs = load(DATA_FILE_PATH)
    ncols, nrows = 101, 103

    def step():
        rs[:, :2] += rs[:, 2:]
        rs[:, 0] %= ncols
        rs[:, 1] %= nrows

    def map_robots(poss: np.ndarray):
        grid = np.zeros((nrows, ncols), dtype=np.int64)
        for ip in range(poss.shape[0]):
            grid[poss[ip, 1], poss[ip, 0]] += 1
        return grid

    def disp(grid: np.ndarray):
        row_str = lambda rvec: "".join([" " if v == 0 else str(v)[-1] for v in rvec])
        print("\n".join(row_str(grid[irow, :]) for irow in range(grid.shape[0])))

    nsteps = 0
    while True:
        step()
        nsteps += 1
        print(f"{nsteps=}", end="\r")
        grid = map_robots(rs[:, :2])
        if ~np.any(grid > 1):
            break

    disp(grid)
    print(f"{nsteps=}")  # Answer: 7847


main()
