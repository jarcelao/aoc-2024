import re
from re import Pattern
from typing import List


class MulHandler:
    def __init__(self):
        self.do: bool = True
        self._mul_pattern: Pattern = re.compile(r"mul\(\d+,\d+\)")
        self._all_pattern: Pattern = re.compile(r"mul\(\d+,\d+\)|\bdo\(\)|\bdon't\(\)")
        self._numbers_pattern: Pattern = re.compile(r"\d+")

    def extract_instructions(self, input: str, with_do: bool = False) -> List[str]:
        return (
            self._all_pattern.findall(input)
            if with_do
            else self._mul_pattern.findall(input)
        )

    def process_mul(self, mul: str) -> int:
        a, b = map(int, self._numbers_pattern.findall(mul))
        return a * b

    def process_instructions(self, instructions: List[str]) -> List[str]:
        self.do = True
        result: List[str] = []

        for instruction in instructions:
            if instruction == "do()":
                self.do = True
            elif instruction == "don't()":
                self.do = False
            elif self.do and "mul(" in instruction:
                result.append(instruction)

        return result

    def get_sum(self, muls: List[str]) -> int:
        return sum(self.process_mul(mul) for mul in muls)


def main():
    with open("input.txt", "r") as file:
        input_str: str = file.read().replace("\n", "")

    mul_handler: MulHandler = MulHandler()

    muls: List[str] = mul_handler.extract_instructions(input_str)
    print(f"Sum of muls: {mul_handler.get_sum(muls)}")

    instructions: List[str] = mul_handler.extract_instructions(input_str, with_do=True)
    muls: List[str] = mul_handler.process_instructions(instructions)
    print(f"Sum of muls (with do instructions): {mul_handler.get_sum(muls)}")


if __name__ == "__main__":
    main()
