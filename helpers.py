import numpy as np


def load_text(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        return f.readlines()


def line_to_numbers(line: str):
    return [int(num_str) for num_str in line.strip().split() if num_str != ""]


def load_matrix(file_path: str, dtype=np.int64):
    lines = [line for line in load_text(file_path) if line != ""]
    return np.array([line_to_numbers(line) for line in lines], dtype=dtype)


def load_grid(fp: str) -> np.ndarray:
    str_grid = ("".join(load_text(fp))).strip()
    grid = np.array([[ch for ch in l] for l in str_grid.split("\n")], dtype="S1")
    indices = np.indices(grid.shape)
    return grid, indices


def disp_grid(grid: np.ndarray):
    print(
        "\n".join(
            "".join(map(bytes.decode, grid[ir, :])) for ir in range(grid.shape[0])
        )
    )
