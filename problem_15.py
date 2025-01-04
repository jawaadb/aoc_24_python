from helpers import load_text
import numpy as np
import re

SMALL_EXAMPLE_PATH = "problem_15_eg_small.txt"
LARGE_EXAMPLE_PATH = "problem_15_eg_large.txt"
DATA_PATH = "problem_15_data.txt"


def load(fp: str) -> tuple[np.ndarray, list[str]]:
    txt = "".join(load_text(fp))
    str_grid, str_moves = txt.split("\n\n")
    str_grid = str_grid.strip()
    str_moves = str_moves.replace("\n", "").strip()
    moves = [ch for ch in str_moves]
    grid = np.array([[ch for ch in l] for l in str_grid.split("\n")], dtype="S1")
    assert np.sum(grid == b"@") == 1
    return grid, moves


def main():
    grid, moves = load(DATA_PATH)
    indices = np.indices(grid.shape)

    def push(pos, dir) -> bool:
        pos_next = pos + {">": [0, 1], "v": [1, 0], "<": [0, -1], "^": [-1, 0]}[dir]
        ch, ch_next = grid[*pos], grid[*pos_next]

        match ch_next:
            case b"#":
                return False
            case b".":
                grid[*pos_next] = ch
                grid[*pos] = b"."
                return True
            case b"O":
                if push(pos_next, dir):
                    grid[*pos_next] = ch
                    grid[*pos] = b"."
                    return True
                else:
                    return False
            case _:
                assert False

    def disp(grid: np.ndarray):
        print(
            "\n".join(
                "".join(map(bytes.decode, grid[ir, :])) for ir in range(grid.shape[0])
            )
        )

    for move in moves:
        pos = np.hstack([indices[0][grid == b"@"][0], indices[1][grid == b"@"][0]])
        push(pos, move)

    disp(grid)

    gps_sum = np.sum(indices[0][grid == b"O"] * 100 + indices[1][grid == b"O"])
    print(f"{gps_sum=}")  # Answer: 1294459


main()
