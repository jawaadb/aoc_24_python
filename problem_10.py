import numpy as np
from helpers import load_text


# FILE_PATH = "problem_10_example.txt"
FILE_PATH = "problem_10_data.txt"


def main():
    # load map
    grid = np.array(
        [[int(ch) for ch in line.strip()] for line in load_text(FILE_PATH)],
        dtype=np.int64,
    )
    nrows, ncols = grid.shape

    # locate trailheads
    indices = np.indices(grid.shape)
    trailhead_locs = np.vstack([indices[0][grid == 0], indices[1][grid == 0]])

    dirs = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]], dtype=np.int64).transpose()

    def score_trailhead(
        grid: np.ndarray, pos: np.ndarray, reachable: np.ndarray, height=0
    ):
        # print(f"{height}: {pos[:].reshape(-1)}")
        next_poss = dirs + pos @ np.ones((1, 4), dtype=np.int64)
        next_poss = next_poss[
            :,
            (next_poss[0, :] >= 0)
            & (next_poss[0, :] < nrows)
            & (next_poss[1, :] >= 0)
            & (next_poss[1, :] < ncols),
        ]

        next_height = height + 1

        near_heights = np.array(
            [grid[*next_poss[:, ipos]] for ipos in range(next_poss.shape[1])],
            dtype=np.int64,
        )

        next_poss = next_poss[:, near_heights == next_height]

        if next_poss.shape[1] == 0:
            return

        for ipos in range(next_poss.shape[1]):
            next_pos = next_poss[:, ipos].reshape((2, 1))
            if next_height == 9:
                reachable[next_pos[0], next_pos[1]] = True
            else:
                score_trailhead(grid, next_pos, reachable, next_height)

    total_score = 0
    for itrailhead in range(trailhead_locs.shape[1]):
        print(f"{itrailhead+1}/{trailhead_locs.shape[1]}", end="\r")
        reachable = np.zeros(grid.shape, dtype=np.bool)
        start_pos = trailhead_locs[:, itrailhead].reshape((2, 1))
        score_trailhead(grid, start_pos, reachable)
        trail_score = np.sum(reachable)
        total_score += trail_score
    print("")

    print(f"{total_score=}")  # Answer: 489


main()
