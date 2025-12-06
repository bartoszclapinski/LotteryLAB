from __future__ import annotations
from collections import Counter
from datetime import date, timedelta
from typing import Dict, List, Optional

from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session

from src.database.models import Draw


def _parse_numbers(numbers_csv: str) -> List[int]:
    return [int(x) for x in numbers_csv.split(",") if x]


def calculate_frequency(
    session: Session,
    game_type: str = "lotto",
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    window_days: Optional[int] = None,
    game_provider: Optional[str] = None,
) -> Dict[int, int]:
    if date_to is None:
        date_to = date.today()
    if window_days is not None and date_from is None:
        date_from = date_to - timedelta(days=window_days - 1)

    conditions = [Draw.game_type == game_type]
    if game_provider:
        conditions.append(Draw.game_provider == game_provider)
    if date_from is not None:
        conditions.append(Draw.draw_date >= date_from)
    if date_to is not None:
        conditions.append(Draw.draw_date <= date_to)

    stmt = select(Draw.numbers).where(and_(*conditions))
    counts: Counter[int] = Counter()

    for (numbers_csv,) in session.execute(stmt).all():
        for n in _parse_numbers(numbers_csv):
            counts[n] += 1

    for n in range(1, 50):
        counts.setdefault(n, 0)

    return dict(sorted(counts.items()))


def count_draws(
    session: Session,
    game_type: str = "lotto",
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    window_days: Optional[int] = None,
    game_provider: Optional[str] = None,
) -> int:
    if date_to is None:
        date_to = date.today()
    if window_days is not None and date_from is None:
        date_from = date_to - timedelta(days=window_days - 1)

    conditions = [Draw.game_type == game_type]
    if game_provider:
        conditions.append(Draw.game_provider == game_provider)
    if date_from is not None:
        conditions.append(Draw.draw_date >= date_from)
    if date_to is not None:
        conditions.append(Draw.draw_date <= date_to)

    stmt = select(func.count()).select_from(Draw).where(and_(*conditions))
    return int(session.execute(stmt).scalar_one() or 0)


def compute_expected_each(num_draws: int) -> float:
    return float(num_draws) * (6.0 / 49.0)


def compute_deltas(freq: Dict[int, int], expected_each: float) -> Dict[int, float]:
    return {k: (float(v) - expected_each) for k, v in freq.items()}


def compute_pct_deltas(freq: Dict[int, int], expected_each: float) -> Dict[int, float]:
    if expected_each == 0:
        return {k: 0.0 for k in freq}
    return {k: ((float(v) - expected_each) / expected_each * 100.0) for k, v in freq.items()}


def get_hot_cold_numbers(
    freq: Dict[int, int],
    expected_each: float,
    top_k: int = 6
) -> Dict[str, List[int]]:
    """
    Identify hot and cold numbers based on frequency vs expected.

    Hot: numbers appearing more frequently than expected
    Cold: numbers appearing less frequently than expected
    """
    deltas = compute_deltas(freq, expected_each)

    # Sort by delta (hot first, then cold)
    sorted_by_delta = sorted(deltas.items(), key=lambda x: x[1], reverse=True)

    hot_numbers = [num for num, delta in sorted_by_delta if delta > 0][:top_k]
    cold_numbers = [num for num, delta in sorted_by_delta if delta < 0][-top_k:]

    return {
        "hot": sorted(hot_numbers),
        "cold": sorted(cold_numbers)
    }