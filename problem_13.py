from helpers import load_text
from collections import namedtuple
import re
import numpy as np
from numpy.linalg import inv

EXAMPLE_FILE_PATH = "problem_13_example.txt"
DATA_FILE_PATH = "problem_13_data.txt"

Game = namedtuple("Game", ["dA", "dB", "pos"])


def extract_game(c: str):
    pattern = re.compile(
        r"^.*A: X\+(\d+), Y\+(\d+)\n.*B: X\+(\d+), Y\+(\d+)\n.*X=(\d+), Y=(\d+)$"
    )
    nums = list(map(int, pattern.match(c).groups()))
    return Game(
        dA=np.array(nums[0:2], dtype=np.int64),
        dB=np.array(nums[2:4], dtype=np.int64),
        pos=np.array(nums[4:6], dtype=np.int64),
    )


def main():
    def load_games(file_path):
        chunks = "".join(load_text(file_path)).split("\n\n")
        return [extract_game(c.strip()) for c in chunks]

    def solve_game(g: Game):
        k = np.int64(np.round(inv(np.vstack([g.dA, g.dB]).transpose()) @ g.pos))

        if np.all(g.dA * k[0] + g.dB * k[1] == g.pos):
            return np.sum(k * [3, 1], dtype=np.int64)
        else:
            return 0

    games = load_games(DATA_FILE_PATH)
    answer = sum(solve_game(g) for g in games)

    print(f"{answer=}")  # Answer: 29187


main()
