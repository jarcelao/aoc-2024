from typing import List


def is_safe(report: List[int], dampened: bool = False) -> bool:
    previous: int = report[0]
    increasing: bool = report[1] > previous
    dampened_used: bool = False

    for i in range(1, len(report)):
        difference: int = report[i] - previous

        if (
            not (1 <= abs(difference) <= 3)
            or (increasing and report[i] < previous)
            or (not increasing and report[i] > previous)
        ):
            if dampened and not dampened_used:
                dampened_used = True
            else:
                return False

        previous = report[i]

    return True


if __name__ == "__main__":
    input_file: str = "input.txt"
    with open(input_file, "r") as file:
        input_list: List[List[int]] = [
            [int(i) for i in line.split()] for line in file.read().splitlines()
        ]

    reports: List[bool] = [is_safe(report) for report in input_list]
    print(f"Number of safe reports: {sum(reports)}")

    reports_dampened: List[bool] = [
        is_safe(report, dampened=True) for report in input_list
    ]
    print(f"Number of safe reports (with Problem Dampener): {
        sum(reports_dampened)}")
