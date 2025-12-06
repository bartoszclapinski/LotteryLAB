from __future__ import annotations
from collections import Counter
import random
from datetime import date, datetime, timedelta, UTC
from pathlib import Path
import csv
import sys
from typing import List

# Ensure project root on path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy import select, and_, desc  # type: ignore
from src.database.session import SessionLocal  # type: ignore
from src.database.models import Draw  # type: ignore

LOG_PATH = PROJECT_ROOT / ".data" / "predictions_log.csv"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def _parse_numbers(numbers_csv: str) -> List[int]:
    return [int(x) for x in numbers_csv.split(",") if x]


def frequency(session, game_type: str, start: date, end: date) -> Counter[int]:
    stmt = select(Draw.numbers).where(
        and_(Draw.game_type == game_type, Draw.draw_date >= start, Draw.draw_date <= end)
    )
    c: Counter[int] = Counter()
    for (nums,) in session.execute(stmt).all():
        c.update(_parse_numbers(nums))
    for n in range(1, 50):
        c.setdefault(n, 0)
    return c


def last_seen_days(session, game_type: str, end: date) -> dict[int, int]:
    stmt = select(Draw.draw_date, Draw.numbers).where(
        and_(Draw.game_type == game_type, Draw.draw_date <= end)
    )
    last: dict[int, date | None] = {n: None for n in range(1, 50)}
    for d, nums in session.execute(stmt).all():
        for n in _parse_numbers(nums):
            if last[n] is None or d > last[n]:
                last[n] = d
    return {n: (end - last[n]).days if last[n] is not None else 10**9 for n in range(1, 50)}


def get_latest_draw(session, game_type: str) -> list[int] | None:
    stmt = (
        select(Draw.draw_date, Draw.draw_number, Draw.numbers)
        .where(Draw.game_type == game_type)
        .order_by(desc(Draw.draw_date), desc(Draw.draw_number))
        .limit(1)
    )
    row = session.execute(stmt).first()
    if not row:
        return None
    _, _, nums = row
    return _parse_numbers(nums)


def read_last_predictions() -> list[tuple[str, list[int]]]:
    if not LOG_PATH.exists():
        return []
    import csv as _csv
    rows: list[dict[str, str]] = []
    with LOG_PATH.open("r", encoding="utf-8", newline="") as f:
        r = _csv.DictReader(f)
        for row in r:
            rows.append(row)  # type: ignore
    if not rows:
        return []
    # group by timestamp and pick the latest
    latest_ts = max(r["timestamp_utc"] for r in rows)
    last_batch = [r for r in rows if r["timestamp_utc"] == latest_ts]
    out: list[tuple[str, list[int]]] = []
    for r in last_batch:
        out.append((r["strategy"], _parse_numbers(r["numbers"].replace("\"", ""))))
    return out


def read_last_predictions_map() -> dict[str, list[int]]:
    pairs = read_last_predictions()
    d: dict[str, list[int]] = {}
    for name, arr in pairs:
        d[name] = arr
    return d


def diversify_set(
    strategy: str,
    nums: list[int],
    last_batch: dict[str, list[int]],
    last_draw: set[int] | None,
    hot_order: list[int],
) -> list[int]:
    target = sorted(nums)
    prev = sorted(last_batch.get(strategy, []))
    if target != prev:
        return target
    # If identical to last time, replace 1-2 numbers with next best alternatives
    forbidden: set[int] = set(prev)
    if last_draw:
        forbidden |= last_draw
    replacement_pool = [n for n in hot_order if n not in forbidden]
    if not replacement_pool:
        return target
    new = set(target)
    # remove the two lowest-ranked numbers within current set (by hot_order index descending)
    rank = {n: i for i, n in enumerate(hot_order)}
    drop_candidates = sorted(new, key=lambda n: rank.get(n, 10**9), reverse=True)
    drops = drop_candidates[:2] if len(drop_candidates) >= 2 else drop_candidates[:1]
    for d in drops:
        new.discard(d)
    add_needed = 6 - len(new)
    adds = replacement_pool[:max(1, add_needed)]
    for a in adds:
        if len(new) < 6:
            new.add(a)
    out = sorted(new)
    # final guard: ensure size 6
    if len(out) < 6:
        for n in range(1, 50):
            if n not in out and (not last_draw or n not in last_draw):
                out.append(n)
            if len(out) == 6:
                break
    return sorted(out)


def pick_top(counter: Counter[int], k: int = 6, exclude: set[int] | None = None) -> list[int]:
    ex = exclude or set()
    arr = [n for n, _ in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])) if n not in ex]
    return sorted(arr[:k])


def pick_bottom(counter: Counter[int], k: int = 6, exclude: set[int] | None = None) -> list[int]:
    ex = exclude or set()
    arr = [n for n, _ in sorted(counter.items(), key=lambda kv: (kv[1], kv[0])) if n not in ex]
    return sorted(arr[:k])


def pick_mixed(hot: Counter[int], cold: Counter[int], k: int = 6) -> list[int]:
    h = [n for n, _ in sorted(hot.items(), key=lambda kv: (-kv[1], kv[0]))]
    c = [n for n, _ in sorted(cold.items(), key=lambda kv: (kv[1], kv[0]))]
    res: set[int] = set()
    i = j = 0
    while len(res) < k and (i < len(h) or j < len(c)):
        if i < len(h):
            res.add(h[i]); i += 1
        if len(res) >= k:
            break
        if j < len(c):
            res.add(c[j]); j += 1
    out = sorted(res)
    return out[:k]


def ensure_rules(nums: list[int]) -> list[int]:
    nums = sorted(set(n for n in nums if 1 <= n <= 49))
    if len(nums) > 6:
        nums = nums[:6]
    candidate = 1
    while len(nums) < 6 and candidate <= 49:
        if candidate not in nums:
            adj = sum(1 for x in nums if abs(x - candidate) == 1)
            if adj <= 1:
                nums.append(candidate)
                nums = sorted(nums)
        candidate += 1
    return nums


def main() -> None:
    game = "lotto"
    now = datetime.now(UTC).isoformat()
    today = date.today()
    with SessionLocal() as s:
        f365 = frequency(s, game, today - timedelta(days=364), today)
        f180 = frequency(s, game, today - timedelta(days=179), today)
        f090 = frequency(s, game, today - timedelta(days=89), today)
        gaps = last_seen_days(s, game, today)
        last_draw = get_latest_draw(s, game)
        last_draw_set = set(last_draw) if last_draw else None

    sets: list[tuple[str, list[int]]] = []
    sets.append(("hot_365", ensure_rules(pick_top(f365))))
    sets.append(("hot_180", ensure_rules(pick_top(f180))))
    sets.append(("hot_090", ensure_rules(pick_top(f090))))
    sets.append(("cold_365", ensure_rules(pick_bottom(f365))))
    sets.append(("balanced_365", ensure_rules(pick_mixed(f365, f365))))
    gap_sorted = [n for n, _ in sorted(gaps.items(), key=lambda kv: (-kv[1], kv[0]))]
    sets.append(("gap_top", ensure_rules(gap_sorted[:6])))
    hot_list = [n for n, _ in sorted(f365.items(), key=lambda kv: (-kv[1], kv[0]))]
    ev = [n for n in hot_list if n % 2 == 0][:3]
    od = [n for n in hot_list if n % 2 == 1][:3]
    sets.append(("even_odd_hot", ensure_rules(ev + od)))
    by_dec: dict[int, list[int]] = {d: [] for d in range(5)}
    for n in hot_list:
        d = (n - 1) // 10
        if d < 5 and len(by_dec[d]) < 2:
            by_dec[d].append(n)
    dec_sel: list[int] = []
    for d in range(5):
        dec_sel += by_dec[d]
    sets.append(("decade_bal", ensure_rules(dec_sel)))
    rand_ctrl = sorted(set(hot_list[3:3 + 48:8]))[:6]
    sets.append(("random_ctrl", ensure_rules(rand_ctrl)))
    # Feedback-aware ensemble: weigh numbers by frequency and last-batch strategy performance
    union: set[int] = set()
    for _, arr in sets[:5]:
        union.update(arr)
    base_score = {n: (f365[n] + f180[n] + f090[n]) for n in range(1, 50)}
    # Strategy performance from last predictions vs last actual draw
    perf_weight_by_strategy: dict[str, float] = {}
    last_preds = read_last_predictions()
    alpha = 0.25  # impact per hit
    if last_draw:
        last_draw_set = set(last_draw)
        for strat, nums in last_preds:
            hits = len(set(nums) & last_draw_set)
            perf_weight_by_strategy[strat] = 1.0 + alpha * hits
    # Aggregate number weights
    number_bonus = {n: 0.0 for n in range(1, 50)}
    for strat, nums in last_preds:
        w = perf_weight_by_strategy.get(strat, 1.0)
        for n in nums:
            if 1 <= n <= 49:
                number_bonus[n] += w
    # Small penalty to numbers that just appeared in the last draw (mean reversion bias)
    if last_draw:
        for n in last_draw:
            number_bonus[n] -= 0.5
    # Final score and selection
    beta = 1.0
    scored = [(n, base_score.get(n, 0) + beta * number_bonus.get(n, 0.0)) for n in union or range(1, 50)]
    scored.sort(key=lambda kv: (-kv[1], kv[0]))
    ens_fb = ensure_rules([n for n, _ in scored][:6])
    # Diversify any set that repeats previous batch exactly
    last_map = read_last_predictions_map()
    diversified: list[tuple[str, list[int]]] = []
    for name, arr in sets:
        diversified.append((name, diversify_set(name, arr, last_map, last_draw_set, hot_list)))
    # Replace with diversified versions
    sets = diversified
    sets.append(("ensemble_fb", ens_fb))

    # Append to CSV log
    new_file = not LOG_PATH.exists()
    with LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["timestamp_utc", "game_type", "strategy", "numbers"])
        for name, arr in sets[:10]:
            w.writerow([now, game, name, ",".join(map(str, arr))])
            print(f"{name}: {','.join(map(str, arr))}")


if __name__ == "__main__":
    main()
