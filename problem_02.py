import numpy as np
from helpers import load_text, line_to_numbers

FILE_PATH = "problem_02_data.txt"


def main():
    lines = [line for line in load_text(FILE_PATH) if line != ""]
    reports = [np.array(line_to_numbers(line), dtype=np.int64) for line in lines]

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

    def check_if_safe_with_dampener(report: np.ndarray) -> bool:
        # check without removal
        if check_if_safe(report):
            return True

        # check with removal
        indices = np.arange(report.size)
        for idx in range(report.size):
            report_sub = report[indices != idx]
            if check_if_safe(report_sub):
                return True

        return False

    is_safe = np.array(
        [check_if_safe_with_dampener(report) for report in reports], np.bool
    )

    total_safe = np.sum(is_safe)

    print(f"{total_safe=}")  # Answer: 293


main()
