from collections import Counter
from typing import List


if __name__ == "__main__":
    input_file: str = "input.txt"
    with open(input_file, "r") as file:
        input_list = [line.split() for line in file.read().splitlines()]

    input_list_a: List[int] = sorted(int(line[0]) for line in input_list)
    input_list_b: List[int] = sorted(int(line[1]) for line in input_list)

    distances: List[int] = [abs(a - b) for a, b in zip(input_list_a, input_list_b)]
    print(f"The sum of the distances is: {sum(distances)}")

    b_counts: Counter = Counter(input_list_b)
    similarity_score: int = sum(a * b_counts[a] for a in input_list_a)
    print(f"The similarity score is: {similarity_score}")
