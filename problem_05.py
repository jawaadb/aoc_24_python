import numpy as np
from helpers import load_text


FILE_PATH = "problem_05_example.txt"


def load_file(file_path):
    lines = [line.strip() for line in load_text(file_path)]

    idx_blank = lines.index("")
    rule_lines = lines[:idx_blank]
    book_lines = lines[idx_blank + 1 :]

    rules = np.array(
        [list(map(int, line.split("|"))) for line in rule_lines], dtype=np.int64
    )
    books = [
        np.array([int(num) for num in line.split(",")], dtype=np.int64)
        for line in book_lines
    ]
    return rules, books


def main():
    rules, books = load_file(FILE_PATH)
    print(rules)
    print(books)


main()
