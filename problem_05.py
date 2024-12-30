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


def check_against_rule(book: np.ndarray, rule: np.ndarray) -> bool:
    book_indices = np.arange(book.size)
    idxL = book_indices[book == rule[0]][0]
    idxR = book_indices[book == rule[1]][0]
    return idxL < idxR, idxL, idxR


def check_against_rules(book: np.ndarray, rules: np.ndarray) -> bool:
    assert isinstance(book, np.ndarray) and isinstance(rules, np.ndarray)
    assert rules.shape[1] == 2

    rules_sub = rules[np.sum(np.isin(rules, book), axis=1) == 2, :]

    rule_passed = np.array(
        [
            check_against_rule(book, rules_sub[irule, :])[0]
            for irule in range(rules_sub.shape[0])
        ],
        np.bool,
    )

    return np.all(rule_passed)


def sort_book(book: np.ndarray, rules: np.ndarray) -> np.ndarray:
    rules = rules[np.sum(np.isin(rules, book), axis=1) == 2, :]

    all_good = False
    while all_good == False:
        all_good = True
        for irule in range(rules.shape[0]):
            is_good, idxL, idxR = check_against_rule(book, rules[irule, :])
            if is_good:
                continue
            all_good = False
            book[idxL], book[idxR] = book[idxR], book[idxL]

    assert check_against_rules(book, rules)
    return book


def main():
    def extract_middle_page(book: np.ndarray) -> int:
        assert book.size % 2 == 1
        return book[(book.size - 1) // 2]

    def sum_mid_pages(books) -> int:
        return np.sum([extract_middle_page(book) for book in books])

    rules, books = load_file(FILE_PATH)

    incorrect_books = filter(
        lambda book: check_against_rules(book, rules) == False, books
    )

    sorted_books = [sort_book(book, rules) for book in incorrect_books]

    print(f"{sum_mid_pages(sorted_books)=}")  # Answer: 4679


main()
