from helpers import load_grid, disp_grid
import numpy as np
from functools import partial
from typing import Dict

EG1_PATH = "problem_16_eg1.txt"
EG2_PATH = "problem_16_eg2.txt"
EG3_PATH = "problem_16_eg3.txt"
DATA_PATH = "problem_16_data.txt"

START, END, WALL, SPACE = b"S", b"E", b"#", b"."

to_tuple = lambda arr: (int(arr[0]), int(arr[1]))
add = lambda p1, p2: (p1[0] + p2[0], p1[1] + p2[1])
diff = lambda p1, p2: (p1[0] - p2[0], p1[1] - p2[1])

dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def main():
    grid, indices = load_grid(EG1_PATH)

    start_pos = to_tuple(
        np.hstack([indices[0][grid == START], indices[1][grid == START]])
    )
    start_dir = dirs.index((0, 1))

    paths: list[list[tuple[int, int]]] = [[start_pos + tuple([start_dir])]]

    def next_pos_options(path: list[tuple[int, int, int]]):
        while True:
            p, d = path[-1][:2], path[-1][2]
            if grid[*p] == END:
                return []
            dir_opp = (d + 2) % 4
            cpds = (add(p, dirs[i]) + tuple([i]) for i in range(4))  # cardinal pts
            cpds = filter(lambda pd: pd[-1] != dir_opp, cpds)  # exclude reversing
            cpds = filter(lambda pd: grid[*pd[:2]] != WALL, cpds)  # exclude walls
            cpds = filter(lambda pd: pd not in path, cpds)  # exclude revisiting

            cpds = list(cpds)
            if len(cpds) == 1:
                path.append(cpds[0])
            else:
                return cpds

    def score_path(path: tuple[int, int, int]) -> int:
        assert len(path) != 0
        nsteps = len(path) - 1
        nturns = sum(
            0 if path[i][2] == path[i - 1][2] else 1 for i in range(1, len(path))
        )
        return nsteps + 1000 * nturns

    best_score = None
    full_paths = []
    while True:
        ipath = 0
        for _ in range(len(paths)):
            path = paths[ipath]
            cposs = next_pos_options(path)

            match len(cposs):
                case 0:
                    if grid[path[-1][:2]] == END:
                        this_score = score_path(path)
                        if best_score is None or this_score < best_score:
                            best_score = this_score
                            print(f"new best: {best_score}")
                        full_paths.append(path)
                    paths.pop(ipath)
                case 1:
                    path.append(cposs[0])
                    ipath += 1
                    assert False
                case _:
                    for i in range(len(cposs) - 1):
                        paths.insert(ipath + i + 1, path.copy())
                    for i in range(len(cposs)):
                        paths[ipath + i].append(cposs[i])
                    ipath += len(cposs)

        if best_score is not None:
            paths = list(filter(lambda pth: score_path(pth) <= best_score, paths))
        if len(paths) == 0:
            break
    print("")

    full_paths = list(filter(lambda pth: score_path(pth) <= best_score, full_paths))

    for path in full_paths:
        for p in path:
            grid[*p[:2]] = b"O"

    num_best_path_tiles = np.sum(grid == b"O")

    disp_grid(grid)
    print(f"{best_score=}")
    print(f"tiles visited: {num_best_path_tiles}")


main()
