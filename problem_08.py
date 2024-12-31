import numpy as np
from helpers import load_text
from itertools import combinations

# FILE_PATH = "problem_08_example.txt"
FILE_PATH = "problem_08_data.txt"


def main():
    def gcd(nums: np.ndarray):
        assert nums.size == 2
        assert nums.dtype == np.int64
        abs_nums = np.abs(nums)
        a, b = np.max(abs_nums), np.min(abs_nums)
        while b != 0:
            a, b = b, a % b
        return a

    grid = np.array([list(line.strip()) for line in load_text(FILE_PATH)], "S1")
    antenna_types = np.unique(grid[grid != b"."])

    antinodes = np.zeros(grid.shape, dtype=np.bool)
    nrows, ncols = antinodes.shape

    indicies = np.indices(grid.shape)

    for atype in antenna_types:
        # locate antennas
        amask = grid == atype
        alocs = np.vstack([indicies[0][amask], indicies[1][amask]]).transpose()
        acount = alocs.shape[0]

        for iA, iB in combinations(range(acount), 2):
            locA = alocs[iA, :]
            locB = alocs[iB, :]
            dstBA = locB - locA
            dstBA //= gcd(dstBA)

            n = 0
            while True:
                anode = locA + n * dstBA
                if np.all((anode >= [0, 0]) & (anode < [nrows, ncols])):
                    antinodes[anode[0], anode[1]] = True
                    n += 1
                else:
                    break

            n = 0
            while True:
                anode = locA - n * dstBA
                if np.all((anode >= [0, 0]) & (anode < [nrows, ncols])):
                    antinodes[anode[0], anode[1]] = True
                    n += 1
                else:
                    break

    antinode_count = np.sum(antinodes)
    print(f"{antinode_count=}")  # Answer: 884


main()
