import itertools

from typing import List


class KMPSearch:
    @staticmethod
    def search(text: str, pattern: str) -> List[int]:
        i: int = 0
        j: int = 0

        lps: List[int] = KMPSearch._gen_lps(pattern)
        text = list(text)

        indices: List[int] = []

        while i < len(text):
            if text[i] == pattern[j]:
                i += 1
                j += 1

                if j == len(pattern):
                    indices.append(i - j)
                    j = lps[j - 1]
            else:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1

        return indices

    @staticmethod
    def count(text: str, pattern: str) -> int:
        return len(KMPSearch.search(text, pattern))

    @staticmethod
    def _gen_lps(pattern: str) -> List[int]:
        pattern: List[str] = list(pattern)
        lps: List[int] = [0] * len(pattern)

        l: int = 0
        i: int = 1

        while i < len(pattern):
            if pattern[i] == pattern[l]:
                l += 1
                lps[i] = l
                i += 1
            else:
                if l != 0:
                    l = lps[l - 1]
                else:
                    lps[i] = 0
                    i += 1

        return lps


class WordSearch:
    def __init__(self):
        self._search_grid: List[List[str]] = []

    def load_from_text(self, text: str) -> None:
        self._search_grid = [[char for char in line] for line in text.split("\n")]

    def count(self, word: str) -> int:
        row_strs: List[str] = self._gen_row_strs()
        col_strs: List[str] = self._gen_col_strs()
        diag_strs: List[str] = self._gen_diag_strs()

        return sum(
            [KMPSearch.count(row_str, word) for row_str in row_strs]
            + [KMPSearch.count(col_str, word) for col_str in col_strs]
            + [KMPSearch.count(diag_str, word) for diag_str in diag_strs]
        )

    def count_x(self, word: str) -> int:
        boxes: List[List[List[str]]] = self._gen_boxes(len(word))
        word_reversed: str = word[::-1]
        x_count: int = 0

        for box in boxes:
            diagonal: str = "".join([box[i][i] for i in range(len(box))])
            antidiagonal: str = "".join(
                [box[i][len(box) - i - 1] for i in range(len(box))]
            )

            if (word in diagonal or word_reversed in diagonal) and (
                word in antidiagonal or word_reversed in antidiagonal
            ):
                x_count += 1

        return x_count

    def _gen_row_strs(self) -> List[str]:
        return ["".join(row) for row in self._search_grid]

    def _gen_col_strs(self) -> List[str]:
        return ["".join(col) for col in zip(*self._search_grid)]

    def _gen_diag_strs(self) -> List[str]:
        # https://stackoverflow.com/a/43311126
        max_col = len(self._search_grid[0])
        max_row = len(self._search_grid)
        fdiag = [[] for _ in range(max_row + max_col - 1)]
        bdiag = [[] for _ in range(len(fdiag))]
        min_bdiag = -max_row + 1

        for x in range(max_col):
            for y in range(max_row):
                fdiag[x + y].append(self._search_grid[y][x])
                bdiag[x - y - min_bdiag].append(self._search_grid[y][x])

        return ["".join(row) for row in itertools.chain(fdiag, bdiag)]

    def _gen_boxes(self, size: int) -> List[List[List[str]]]:
        boxes: List[List[List[str]]] = []
        max_row: int = len(self._search_grid)
        max_col: int = len(self._search_grid[0])

        for i in range(max_row - size + 1):
            for j in range(max_col - size + 1):
                box: List[List[str]] = []
                for k in range(size):
                    box.append(self._search_grid[i + k][j : j + size])
                boxes.append(box)

        return boxes


def main():
    input_file: str = "input.txt"
    with open(input_file, "r") as file:
        text: str = file.read()

    word_search: WordSearch = WordSearch()
    word_search.load_from_text(text)

    total_xmas = word_search.count("XMAS") + word_search.count("SAMX")
    print(f"Total occurrences of XMAS: {total_xmas}")

    total_x_mas = word_search.count_x("MAS")
    print(f"Total occurrences of X-MAS: {total_x_mas}")


if __name__ == "__main__":
    main()
