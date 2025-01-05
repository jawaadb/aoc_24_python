from helpers import load_grid, disp_grid
import numpy as np
from functools import partial

EG1_PATH = "problem_16_eg1.txt"
EG2_PATH = "problem_16_eg2.txt"
EG3_PATH = "problem_16_eg3.txt"
DATA_PATH = "problem_16_data.txt"

START, END, WALL, SPACE = b"S", b"E", b"#", b"."


def main():
    to_tuple = lambda arr: (int(arr[0]), int(arr[1]))
    add = lambda p1, p2: (p1[0] + p2[0], p1[1] + p2[1])
    diff = lambda p1, p2: (p1[0] - p2[0], p1[1] - p2[1])

    def score_path(path: list[tuple[int, int]]):
        nsteps = len(path) - 1
        d_prev = (0, 1)
        nturns = 0
        for p0, p1 in zip(path[:-1], path[1:]):
            d_this = diff(p1, p0)
            if d_this != d_prev:
                nturns += 1
            d_prev = d_this
        return nsteps + 1000 * nturns

    grid = load_grid(DATA_PATH)
    indices = np.indices(grid.shape)
    start_pos = to_tuple(
        np.hstack([indices[0][grid == START], indices[1][grid == START]])
    )
    end_pos = to_tuple(np.hstack([indices[0][grid == END], indices[1][grid == END]]))

    paths: list[list[np.ndarray]] = []
    dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    is_space = lambda p: (grid[p[0], p[1]] != WALL)
    is_not_visited = lambda p, index: (p in paths[index]) == False

    best_score = [None]

    def solve(pos: tuple[int, int], index):
        this_path: list[tuple[int, int]] = paths[index]

        # candidate positions
        while True:
            this_path.append(pos)
            print(f"{index}: {pos}", end="\r")
            if grid[pos[0], pos[1]] == END:
                this_score = score_path(this_path)
                if (best_score[0] is None) or (this_score < best_score[0]):
                    best_score[0] = this_score
                    print(f"\nbest: {best_score[0]}")
                return
            cposs = [add(d, pos) for d in dirs]
            cposs = [p for p in cposs if is_space(p)]
            cposs = [p for p in cposs if is_not_visited(p, index)]

            match len(cposs):
                case 0:  # dead end
                    return
                case 1:  # only one
                    pos = cposs[0]
                case _:
                    break

        assert len(cposs) > 1

        if False:
            gcpy = grid.copy()
            for pt in this_path:
                gcpy[pt[0], pt[1]] = b"x"
            gcpy[this_path[-1][0], this_path[-1][1]] = b"O"
            if this_path[-1][0] < gcpy.shape[0] // 2:
                disp_grid(gcpy[: gcpy.shape[0] // 2, :])
            else:
                disp_grid(gcpy)
            input()

        indices = [index] + list(range(len(paths), len(paths) + len(cposs) - 1))
        for p in cposs[1:]:
            paths.append(this_path.copy())

        for i, p in zip(indices, cposs):
            if (best_score[0] is None) or (score_path(paths[i]) < best_score[0]):
                solve(p, i)
            else:
                print(f"already bettered ({i}): {best_score[0]}")

    paths.append([])
    solve(start_pos, 0)
    print("")

    disp_grid(grid)

    complete_paths = [p for p in paths if p[-1] == end_pos]

    if len(complete_paths) == 0:
        return

    path_scores = [score_path(p) for p in complete_paths]
    min_score = min(path_scores)

    print(f"{min_score=}")


main()
