from collections import defaultdict
from typing import Dict, List, Tuple


class PageOrderHandler:
    def __init__(self, page_rules: List[str]) -> None:
        self._page_rules: Dict[int, List[int]] = self._parse_page_rules(page_rules)

    def _parse_page_rules(self, page_rules_strs: List[str]) -> Dict[int, List[int]]:
        page_rules_graph: defaultdict = defaultdict(list)
        for page_rule in page_rules_strs:
            page_rule_split: List[int] = [int(num) for num in page_rule.split("|")]
            page_rules_graph[page_rule_split[0]].append(page_rule_split[1])
        return dict(page_rules_graph)

    def _parse_page_order(self, page_order_str: str) -> List[int]:
        return [int(num) for num in page_order_str.split(",")]

    def _locate_invalid_pages(self, page_order: List[int]) -> List[Tuple[int, int]]:
        invalid_pages: List[Tuple[int, int]] = []
        for i in range(len(page_order)):
            for j in range(i + 1, len(page_order)):
                if page_order[j] not in self._page_rules.get(page_order[i], []):
                    invalid_pages.append((j, i))
        return invalid_pages

    def validate_page_order(self, page_order_str: str) -> bool:
        page_order: List[int] = self._parse_page_order(page_order_str)
        return not self._locate_invalid_pages(page_order)

    def fix_page_order(self, page_order_str: str) -> str:
        page_order: List[int] = self._parse_page_order(page_order_str)
        invalid_pages: List[Tuple[int, int]] = self._locate_invalid_pages(page_order)

        while invalid_pages:
            for j, i in invalid_pages:
                page_order[i], page_order[j] = page_order[j], page_order[i]
            invalid_pages = self._locate_invalid_pages(page_order)

        return ",".join(map(str, page_order))

    def get_middle_page(self, page_order_str: str) -> int:
        page_order: List[int] = self._parse_page_order(page_order_str)
        middle_index: int = len(page_order) // 2
        return page_order[middle_index]


def main() -> None:
    input_file: str = "input.txt"

    with open(input_file, "r") as file:
        lines: List[str] = file.readlines()

    break_index: int = lines.index("\n")
    page_rule_strs: List[str] = [line.strip() for line in lines[:break_index]]
    page_update_strs: List[str] = [line.strip() for line in lines[break_index + 1:]]

    page_handler = PageOrderHandler(page_rule_strs)

    middle_page_sum: int = sum(
        page_handler.get_middle_page(page_update)
        for page_update in page_update_strs
        if page_handler.validate_page_order(page_update)
    )
    print(f"Sum of middle pages of valid updates: {middle_page_sum}")

    fixed_page_orders: List[str] = [
        page_handler.fix_page_order(page_update)
        for page_update in page_update_strs
        if not page_handler.validate_page_order(page_update)
    ]
    fixed_page_sum: int = sum(
        page_handler.get_middle_page(fixed_page) for fixed_page in fixed_page_orders
    )
    print(f"Sum of middle pages of fixed updates: {fixed_page_sum}")


if __name__ == "__main__":
    main()
