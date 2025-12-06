from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, date
from typing import Iterable, Iterator, Optional

@dataclass
class ParsedDraw:
    draw_number: int
    draw_date: date
    numbers: list[int]


def parse_initial_txt(lines: Iterable[str]) -> Iterator[ParsedDraw]:
    """Parse lines like '1234. 05.01.1994 1,5,11,23,31,48'.
    - Ignores blank/comment lines.
    - Yields ParsedDraw records.
    """
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        # Expect pattern: '<idx>. <dd.mm.yyyy> <n1,n2,n3,n4,n5,n6>'
        # Split once after the dot to be resilient to spacing
        try:
            left, right = line.split(".", 1)
            draw_number = int(left)
        except Exception:
            continue
        right = right.strip()
        try:
            date_str, nums_str = right.split(" ", 1)
        except ValueError:
            continue
        try:
            draw_date = datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            continue
        try:
            numbers = [int(x) for x in nums_str.split(",")]
        except Exception:
            continue
        yield ParsedDraw(draw_number=draw_number, draw_date=draw_date, numbers=numbers)
