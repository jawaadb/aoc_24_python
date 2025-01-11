from helpers import load_grid, disp_grid
import numpy as np
from functools import partial
import time

EG1_PATH = "problem_16_eg1.txt"
EG2_PATH = "problem_16_eg2.txt"
EG3_PATH = "problem_16_eg3.txt"
DATA_PATH = "problem_16_data.txt"

START, END, WALL, SPACE = b"S", b"E", b"#", b"."

to_tuple = lambda arr: (int(arr[0]), int(arr[1]))
add = lambda p1, p2: (p1[0] + p2[0], p1[1] + p2[1])
diff = lambda p1, p2: (p1[0] - p2[0], p1[1] - p2[1])


def main():
    grid, indices = load_grid(DATA_PATH)

    start_pos = to_tuple(
        np.hstack([indices[0][grid == START], indices[1][grid == START]])
    )

    best_score = [None]
    fd = {}

    dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    is_space = lambda p: (grid[p[0], p[1]] != WALL)
    DD = {0: ">", 1: "^", 2: "<", 3: "v"}

    def flood(pos, dir, sum):
        inp = pos + tuple([dir])
        if (inp in fd) and (sum >= fd[inp]):
            return
        fd[inp] = sum

        if grid[*pos] == END:
            if best_score[0] is None or sum < best_score[0]:
                best_score[0] = sum
                print(f"new best: {best_score[0]}")
            return

        if best_score[0] is not None and sum >= best_score[0]:
            return

        gcpy = grid.copy()

        while True:
            grid[*pos] = b" "
            dir_opp = (dir + 2) % 4
            cposs = [add(pos, dirs[i]) for i in range(4)]
            cposs = [p for p in cposs if is_space(p)]
            cdirs = [dirs.index(diff(p, pos)) for p in cposs]
            mask = [d != dir_opp for d in cdirs]
            cposs = [p for p, m in zip(cposs, mask) if m]
            cdirs = [d for d, m in zip(cdirs, mask) if m]

            if len(cposs) != 1:
                break
            if grid[*cposs[0]] == END:
                break

            if cdirs[0] != dir:
                sum += 1000
            sum += 1
            gcpy[*pos] = b"o"
            pos, dir = cposs[0], cdirs[0]

        gcpy[*pos] = DD[dir].encode("utf-8")
        for p, d in zip(cposs, cdirs):
            gcpy[*p] = DD[d].encode("utf-8")
        if False:
            if pos[0] < grid.shape[0] // 2:
                disp_grid(gcpy[: grid.shape[0] // 2, :])
            else:
                disp_grid(gcpy)
            print(f"(best: {best_score[0]}) {pos=}, {DD[dir]}, {sum=}")

        for p, d in zip(cposs, cdirs):
            flood(p, d, sum + 1 + (0 if dirs.index(diff(p, pos)) == dir else 1000))

    flood(start_pos, 0, 0)

    print(f"best: {best_score[0]}")


main()
