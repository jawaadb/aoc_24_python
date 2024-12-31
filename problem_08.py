import numpy as np
from helpers import load_text
from itertools import combinations

# FILE_PATH = "problem_08_example.txt"
FILE_PATH = "problem_08_data.txt"


def main():
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
            anode1 = locB + dstBA
            anode2 = locA - dstBA

            for anode in [anode1, anode2]:
                # mark antinode if in bounds
                if np.all((anode >= [0, 0]) & (anode < [nrows, ncols])):
                    antinodes[anode[0], anode[1]] = True

    antinode_count = np.sum(antinodes)
    print(f"{antinode_count=}")  # Answer: 222


main()
