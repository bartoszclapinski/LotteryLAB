from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from typing import Tuple

from .file_parser import ParsedDraw

@dataclass
class ValidationResult:
    ok: bool
    reason: str | None = None


def validate_draw(parsed: ParsedDraw) -> ValidationResult:
    # Six numbers
    if len(parsed.numbers) != 6:
        return ValidationResult(False, "must have 6 numbers")
    # Integers in range 1..49
    for n in parsed.numbers:
        if not (1 <= n <= 49):
            return ValidationResult(False, f"number out of range: {n}")
    # Unique numbers
    if len(set(parsed.numbers)) != 6:
        return ValidationResult(False, "numbers must be unique")
    # Reasonable date (not in future)
    today = date.today()
    if parsed.draw_date > today:
        return ValidationResult(False, "date in future")
    # Draw number positive
    if parsed.draw_number <= 0:
        return ValidationResult(False, "draw_number must be positive")
    return ValidationResult(True)


def serialize_numbers(numbers: list[int]) -> str:
    return ",".join(str(n) for n in numbers)
