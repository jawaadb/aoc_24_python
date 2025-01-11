from helpers import load_grid, disp_grid
import numpy as np
from typing import Dict
from dataclasses import dataclass

EG1_PATH = "problem_16_eg1.txt"
EG2_PATH = "problem_16_eg2.txt"
DATA_PATH = "problem_16_data.txt"

START, END, WALL, SPACE = b"S", b"E", b"#", b"."

to_tuple = lambda arr: (int(arr[0]), int(arr[1]))
add = lambda p1, p2: (p1[0] + p2[0], p1[1] + p2[1])
diff = lambda p1, p2: (p1[0] - p2[0], p1[1] - p2[1])

dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]
DD = {0: ">", 1: "^", 2: "<", 3: "v"}


def main():
    grid, indices = load_grid(DATA_PATH)

    score_mem: Dict[tuple[int, int, int], int] = {}

    @dataclass
    class Path:
        pts: list[tuple[int, int, int]]
        score: int

        def append(self, p: tuple[int, int, int]):
            self.pts.append(p)
            if len(self.pts) <= 1:
                self.score = 0
            else:
                self.score += 1 + (1000 if self.pts[-1][2] != self.pts[-2][2] else 0)
            if p not in score_mem:
                score_mem[p] = self.score
            else:
                score_mem[p] = min(self.score, score_mem[p])
            return self

        def copy(self):
            return Path(pts=self.pts.copy(), score=self.score)

        def disp(self):
            gcpy = grid.copy()
            for p in self.pts:
                gcpy[*p[:2]] = DD[p[2]].encode("utf-8")
            disp_grid(gcpy)

    start_pos = to_tuple(
        np.hstack([indices[0][grid == START], indices[1][grid == START]])
    )
    start_dir = dirs.index((0, 1))

    paths: list[Path] = [Path(pts=[], score=0).append(start_pos + tuple([start_dir]))]

    best_score: int = None

    def next_point_options(path: Path):
        while True:
            if score_mem[path.pts[-1]] < path.score:
                return []

            p, d = path.pts[-1][:2], path.pts[-1][2]
            if grid[*p] == END:
                return []
            dir_opp = (d + 2) % 4
            cpds = (add(p, dirs[i]) + tuple([i]) for i in range(4))  # cardinal pts
            cpds = filter(lambda pd: pd[-1] != dir_opp, cpds)  # exclude reversing
            cpds = filter(lambda pd: grid[*pd[:2]] != WALL, cpds)  # exclude walls

            cpds = list(cpds)
            if len(cpds) == 1:
                path.append(cpds[0])
            else:
                return cpds

    full_paths: list[Path] = []
    while True:
        ipath = 0
        for _ in range(len(paths)):
            path: Path = paths[ipath]
            cposs = next_point_options(path)

            match len(cposs):
                case 0:
                    end_path = paths.pop(ipath)
                    if grid[*end_path.pts[-1][:2]] == END:
                        if best_score is None or end_path.score < best_score:
                            best_score = end_path.score
                            print(f"new best: {best_score}", end="\r")
                        full_paths.append(end_path)
                case 1:
                    assert False
                case _:
                    for i in range(len(cposs) - 1):
                        paths.insert(ipath + i + 1, path.copy())
                    for i in range(len(cposs)):
                        paths[ipath + i].append(cposs[i])
                    ipath += len(cposs)

        if best_score is not None:
            paths = list(filter(lambda pth: pth.score <= best_score, paths))
        if len(paths) == 0:
            break

    full_paths = list(filter(lambda pth: pth.score <= best_score, full_paths))

    for path in full_paths:
        for p in path.pts:
            grid[*p[:2]] = b"O"

    num_best_path_tiles = np.sum(grid == b"O")

    disp_grid(grid)
    print(f"{best_score=}")
    print(f"tiles visited: {num_best_path_tiles}")


main()
