import numpy as np
from helpers import load_matrix

FILE_PATH = "problem_02_example.txt"


def main():
    numbers = load_matrix(FILE_PATH)

    num_reports = numbers.shape[0]
    num_levels = numbers.shape[1]

    def check_if_safe(report: np.ndarray) -> bool:
        assert report.size == num_levels
        diff = np.diff(report)

        # all increasing or all decreasing
        all_increasing = np.all(diff >= 0)
        all_decreasing = np.all(diff <= 0)

        if not (all_increasing or all_decreasing):
            return False

        # adjacent levels differ by at least 1 and at most 3
        diff_abs = np.abs(diff)
        return np.all((diff_abs >= 1) & (diff_abs <= 3))

    is_safe = np.array(
        [check_if_safe(numbers[idx_report, :]) for idx_report in range(num_reports)],
        np.bool,
    )

    total_safe = np.sum(is_safe)

    print(f"{total_safe=}")


main()
