import numpy as np
from helpers import load_text, line_to_numbers

FILE_PATH = "problem_02_data.txt"


def main():
    lines = [line for line in load_text(FILE_PATH) if line != ""]
    reports = [np.array(line_to_numbers(line), dtype=np.int32) for line in lines]

    num_reports = len(reports)

    print(f"{num_reports=}")

    def check_if_safe(report: np.ndarray) -> bool:
        diff = np.diff(report)

        # all increasing or all decreasing
        all_increasing = np.all(diff >= 0)
        all_decreasing = np.all(diff <= 0)
        if not (all_increasing or all_decreasing):
            return False

        # adjacent levels differ by at least 1 and at most 3
        diff_abs = np.abs(diff)
        return np.all((diff_abs >= 1) & (diff_abs <= 3))

    is_safe = np.array([check_if_safe(report) for report in reports], np.bool)

    total_safe = np.sum(is_safe)

    print(f"{total_safe=}")  # Answer: 224


main()
