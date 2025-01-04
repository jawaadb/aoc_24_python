from helpers import load_text
import numpy as np

SMALL_EXAMPLE_PATH = "problem_15_eg_small.txt"
LARGE_EXAMPLE_PATH = "problem_15_eg_large.txt"
PART2_EXAMPLE_PATH = "problem_15_eg_part2.txt"
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
    def disp(grid: np.ndarray):
        print(
            "\n".join(
                "".join(map(bytes.decode, grid[ir, :])) for ir in range(grid.shape[0])
            )
        )

    def scale_up_map(grid: np.ndarray) -> np.ndarray:
        nrows, ncols = grid.shape
        new_grid: np.ndarray = np.full((nrows, ncols * 2), b" ", dtype=grid.dtype)

        for icol in range(ncols):
            new_grid[:, icol * 2] = grid[:, icol]
            new_grid[new_grid[:, icol * 2] == b"O", icol * 2] = b"["

        for icol in range(1, new_grid.shape[1], 2):
            new_grid[new_grid[:, icol - 1] == b"#", icol] = b"#"
            new_grid[new_grid[:, icol - 1] == b"[", icol] = b"]"
            new_grid[new_grid[:, icol - 1] == b".", icol] = b"."
            new_grid[new_grid[:, icol - 1] == b"@", icol] = b"."

        assert ~np.any(new_grid == " ")

        return new_grid

    grid, moves = load(DATA_PATH)
    grid = scale_up_map(grid)
    indices = np.indices(grid.shape)

    dd = {">": [0, 1], "v": [1, 0], "<": [0, -1], "^": [-1, 0]}

    def is_pushable(pos, dir) -> bool:
        ch = grid[*pos]
        if ch == b".":
            return True
        if ch == b"#":
            return False

        pos_next = pos + dd[dir]

        if dir in ["<", ">"]:
            return is_pushable(pos_next, dir)
        else:
            match ch:
                case b"[":
                    posL_next, posR_next = pos_next, pos_next + [0, 1]
                case b"]":
                    posL_next, posR_next = pos_next + [0, -1], pos_next
                case _:
                    assert False
            return is_pushable(posL_next, dir) & is_pushable(posR_next, dir)

    def push(pos, dir):
        ch = grid[*pos]
        if ch in [b".", b"#"]:
            return

        is_pair = (dir in ["^", "v"]) and (ch in [b"[", b"]"])

        if is_pair:
            match ch:
                case b"[":
                    posL, posR = pos, pos + [0, 1]
                case b"]":
                    posL, posR = pos + [0, -1], pos
                case _:
                    assert False

            posL_next, posR_next = posL + dd[dir], posR + dd[dir]
            if is_pushable(posL_next, dir) and is_pushable(posR_next, dir):
                push(posL_next, dir)
                push(posR_next, dir)
                grid[*posL_next], grid[*posR_next] = grid[*posL], grid[*posR]
                grid[*posL], grid[*posR] = b".", b"."
                return
            else:
                return
        else:  # push single
            pos_next = pos + dd[dir]
            if is_pushable(pos_next, dir):
                push(pos_next, dir)
                grid[*pos_next] = grid[*pos]
                grid[*pos] = b"."

    for move in moves:
        pos = np.hstack([indices[0][grid == b"@"][0], indices[1][grid == b"@"][0]])
        push(pos, move)

    disp(grid)

    box_mask = grid == b"["
    gps_sum = np.sum(indices[0][box_mask] * 100 + indices[1][box_mask])
    print(f"ans: {gps_sum}")  # Answer: 1319212


main()
