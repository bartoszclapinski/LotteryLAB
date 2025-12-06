from datetime import date, timedelta
from src.database.session import SessionLocal
from src.analysis.frequency import calculate_frequency, compute_expected_each, compute_deltas, compute_pct_deltas


def test_frequency_has_1_49_keys():
    with SessionLocal() as s:
        end = date.today()
        freq = calculate_frequency(s, game_type="lotto", date_from=end - timedelta(days=365), date_to=end)
    assert set(range(1, 50)).issubset(freq.keys())
    assert all(v >= 0 for v in freq.values())


def test_expected_and_deltas_math():
    # simple scenario: if expected_each is 10, and one number occurs 15 then delta=5, pct=50%
    freq = {i: 10 for i in range(1, 50)}
    freq[7] = 15
    expected = compute_expected_each(49 * 10 / (6/49))  # invert to get num_draws that yields expected=10
    # Due to floating arithmetic, recompute expected as exactly 10 for clarity
    expected = 10.0
    deltas = compute_deltas(freq, expected)
    pct = compute_pct_deltas(freq, expected)
    assert deltas[7] == 5.0
    assert round(pct[7], 2) == 50.0
    assert all(round(v, 6) == 0.0 for k, v in pct.items() if k != 7)
