import pytest
from src.analysis.patterns import (
    detect_consecutive_numbers,
    detect_arithmetic_sequences,
    detect_digit_patterns,
    detect_sum_patterns,
    analyze_patterns
)
from src.database.session import SessionLocal


def test_consecutive_numbers_basic():
    """Test consecutive number detection with simple sequence."""
    sequence = [1, 2, 3, 5, 6, 8, 9, 10]
    result = detect_consecutive_numbers(sequence, min_length=2)

    assert result["total_sequences"] == 3  # [1,2,3], [5,6], [8,9,10]
    assert result["max_length"] == 3  # [1,2,3] or [8,9,10]
    assert abs(result["avg_length"] - 2.666) < 0.001  # (3+2+3)/3 ≈ 2.666
    assert len(result["sequences"]) == 3


def test_consecutive_numbers_single():
    """Test consecutive detection with single numbers."""
    sequence = [1, 3, 5, 7]
    result = detect_consecutive_numbers(sequence, min_length=2)

    assert result["total_sequences"] == 0
    assert result["max_length"] == 0
    assert result["avg_length"] == 0.0
    assert result["sequences"] == []


def test_consecutive_numbers_min_length():
    """Test consecutive detection with minimum length requirement."""
    sequence = [1, 2, 5, 6, 7]
    result = detect_consecutive_numbers(sequence, min_length=3)

    assert result["total_sequences"] == 1  # Only [5,6,7] meets min_length=3
    assert result["max_length"] == 3
    assert len(result["sequences"]) == 1
    assert result["sequences"][0] == [5, 6, 7]


def test_consecutive_numbers_empty():
    """Test consecutive detection with empty sequence."""
    result = detect_consecutive_numbers([])

    assert result["total_sequences"] == 0
    assert result["max_length"] == 0
    assert result["avg_length"] == 0.0
    assert result["sequences"] == []


def test_arithmetic_sequences_basic():
    """Test arithmetic sequence detection."""
    draws = [[1, 3, 5, 7], [2, 4, 6, 8], [10, 15, 20]]
    result = detect_arithmetic_sequences(draws, min_length=3)

    assert result["total_sequences"] >= 3  # Algorithm finds all arithmetic subsequences, not just one per draw
    assert len(result["sequences_found"]) >= 3  # Should find multiple sequences
    assert len(result["common_differences"]) > 0

    # Check first sequence
    seq = result["sequences_found"][0]
    assert seq["sequence"] == [1, 3, 5]
    assert seq["common_difference"] == 2


def test_arithmetic_sequences_no_sequences():
    """Test arithmetic detection with no valid sequences."""
    draws = [[1, 2, 4, 8], [3, 6, 9, 12]]  # No arithmetic sequences of length 3
    result = detect_arithmetic_sequences(draws, min_length=3)

    assert result["total_sequences"] == 0
    assert result["sequences_found"] == []


def test_digit_patterns_basic():
    """Test digit pattern detection."""
    sequence = [12, 23, 34, 45]  # Digits: 1,2,2,3,3,4,4,5
    result = detect_digit_patterns(sequence)

    assert result["digit_frequencies"][2] == 2  # Digit 2 appears twice
    assert result["digit_frequencies"][3] == 2  # Digit 3 appears twice
    assert len(result["repeating_digits"]) > 0
    assert 2 in result["repeating_digits"]  # 2 is a repeating digit


def test_digit_patterns_single():
    """Test digit patterns with single occurrence digits."""
    sequence = [1, 2, 3, 4, 5]
    result = detect_digit_patterns(sequence)

    assert len(result["repeating_digits"]) == 0  # No repeating digits
    assert result["digit_frequencies"][1] == 1
    assert result["digit_sums"] == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}  # Each digit appears once


def test_sum_patterns_basic():
    """Test sum pattern detection."""
    draws = [[1, 2, 3], [4, 5, 6], [1, 2, 3], [7, 8, 9]]
    result = detect_sum_patterns(draws)

    assert result["sum_range"] == (6, 24)  # min=1+2+3=6, max=7+8+9=24
    assert result["most_common_sums"][6] == 2  # Sum 6 appears twice
    assert len(result["sum_distribution"]) > 0


def test_sum_patterns_empty():
    """Test sum patterns with empty draws."""
    result = detect_sum_patterns([])

    assert result["sum_range"] == (0, 0)
    assert result["most_common_sums"] == {}
    assert result["sum_distribution"] == {}


def test_analyze_patterns_comprehensive():
    """Test comprehensive pattern analysis."""
    # This would require database setup, so we'll test with mock data
    from unittest.mock import Mock, patch

    mock_session = Mock()
    mock_repo = Mock()
    mock_repo.list.return_value = [
        {"numbers": "1,2,3,4,5,6"},
        {"numbers": "7,8,9,10,11,12"},
        {"numbers": "13,14,15,16,17,18"}
    ]

    with patch('src.analysis.patterns.DrawRepository', return_value=mock_repo):
        result = analyze_patterns(mock_session, "lotto", 365)

        assert "consecutive_numbers" in result
        assert "arithmetic_sequences" in result
        assert "digit_patterns" in result
        assert "sum_patterns" in result
        assert result["total_draws_analyzed"] == 3
        # Should have 3 draws * 6 numbers = 18 numbers
        assert result["total_numbers_analyzed"] == 18

    with patch('src.analysis.patterns.DrawRepository', return_value=mock_repo):
        result = analyze_patterns(mock_session, "lotto", 365)

        assert "consecutive_numbers" in result
        assert "arithmetic_sequences" in result
        assert "digit_patterns" in result
        assert "sum_patterns" in result
        assert result["total_draws_analyzed"] == 3
        assert result["total_numbers_analyzed"] == 18  # 3 draws * 6 numbers


def test_analyze_patterns_no_data():
    """Test pattern analysis with no data."""
    from unittest.mock import Mock, patch

    mock_session = Mock()
    mock_repo = Mock()
    mock_repo.list.return_value = []

    with patch('src.analysis.patterns.DrawRepository', return_value=mock_repo):
        result = analyze_patterns(mock_session, "lotto", 365)

        assert "error" in result
        assert result["error"] == "No draws found for analysis"


def test_analyze_patterns_invalid_data():
    """Test pattern analysis with invalid data."""
    from unittest.mock import Mock, patch

    mock_session = Mock()
    mock_repo = Mock()
    mock_repo.list.return_value = [
        {"numbers": "invalid"},
        {"numbers": "also_invalid"}
    ]

    with patch('src.analysis.patterns.DrawRepository', return_value=mock_repo):
        result = analyze_patterns(mock_session, "lotto", 365)

        assert "error" in result
        assert result["error"] == "No valid numbers found in draws"
