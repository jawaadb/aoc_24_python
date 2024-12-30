import numpy as np
from helpers import load_text
from functools import partial


# FILE_PATH = "problem_05_example.txt"
FILE_PATH = "problem_05_data.txt"


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


def check_against_rules(book: np.ndarray, rules: np.ndarray) -> bool:
    assert isinstance(book, np.ndarray) and isinstance(rules, np.ndarray)
    assert rules.shape[1] == 2

    def check_against_rule(book: np.ndarray, rule: np.ndarray) -> bool:
        book_indices = np.arange(book.size)
        idxL = book_indices[book == rule[0]][0]
        idxR = book_indices[book == rule[1]][0]
        return idxL < idxR

    rules_sub = rules[np.sum(np.isin(rules, book), axis=1) == 2, :]

    rule_passed = np.array(
        [
            check_against_rule(book, rules_sub[irule, :])
            for irule in range(rules_sub.shape[0])
        ],
        np.bool,
    )

    return np.all(rule_passed)


def main():
    def extract_middle_page(book: np.ndarray) -> int:
        assert book.size % 2 == 1
        return book[(book.size - 1) // 2]

    def sum_mid_pages(books) -> int:
        return np.sum([extract_middle_page(book) for book in books])

    rules, books = load_file(FILE_PATH)

    correct_books = filter(partial(check_against_rules, rules=rules), books)

    print(f"{sum_mid_pages(correct_books)=}")


main()
