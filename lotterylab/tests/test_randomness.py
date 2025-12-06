import pytest
from src.analysis.randomness import chi_square_goodness_of_fit, kolmogorov_smirnov_test, runs_test, autocorrelation_test, analyze_number_randomness
from src.database.session import SessionLocal


def test_chi_square_uniform_distribution():
    """Test chi-square test with perfectly uniform distribution (should be random)."""
    # Perfectly uniform distribution: each number appears exactly 10 times
    observed = {i: 10 for i in range(1, 50)}  # 49 numbers
    result = chi_square_goodness_of_fit(observed)

    assert result["chi_square_statistic"] == 0.0  # Perfect fit = 0
    assert result["p_value"] == 1.0  # p=1.0 for perfect fit
    assert result["is_random"] is True
    assert result["degrees_of_freedom"] == 48  # 49 categories - 1 = 48
    # expected_frequency = total_observations / num_categories = 490 / 49 = 10
    assert result["expected_frequency"] == 10.0
    assert result["total_observations"] == 490


def test_chi_square_skewed_distribution():
    """Test chi-square test with heavily skewed distribution (should not be random)."""
    # Very skewed distribution: one number appears 300 times, others appear 1 time each
    observed = {1: 300}
    for i in range(2, 50):
        observed[i] = 1

    result = chi_square_goodness_of_fit(observed)

    assert result["chi_square_statistic"] > 0  # Some deviation
    assert result["p_value"] < 0.05  # Very unlikely to be random
    assert result["is_random"] is False
    assert result["degrees_of_freedom"] == 48  # 49 categories - 1 = 48


def test_chi_square_empty_data():
    """Test chi-square test with empty data."""
    result = chi_square_goodness_of_fit({})

    assert result["chi_square_statistic"] == 0.0
    assert result["p_value"] == 1.0
    assert result["is_random"] is True
    assert result["total_observations"] == 0


def test_chi_square_single_observation():
    """Test chi-square test with minimal data."""
    observed = {1: 6}  # Only one number observed 6 times
    result = chi_square_goodness_of_fit(observed)

    assert result["total_observations"] == 6
    # expected_frequency = total_observations / num_categories = 6 / 1 = 6.0
    # (only 1 number in observed dictionary)
    assert result["expected_frequency"] == 6.0
    assert result["degrees_of_freedom"] == 0  # 1 category - 1 = 0


def test_analyze_number_randomness_basic():
    """Test the main randomness analysis function."""
    with SessionLocal() as session:
        result = analyze_number_randomness(session, game_type="lotto", window_days=30)

    # Check structure of returned data
    required_keys = [
        "game_type", "analysis_period", "sample_size",
        "chi_square_test", "entropy", "summary"
    ]

    for key in required_keys:
        assert key in result

    assert result["game_type"] == "lotto"
    assert "total_draws" in result["sample_size"]
    assert "appears_random" in result["summary"]

    # Check chi-square test results
    chi_square = result["chi_square_test"]
    required_chi_keys = [
        "chi_square_statistic", "p_value", "degrees_of_freedom",
        "is_random", "expected_frequency", "total_observations"
    ]

    for key in required_chi_keys:
        assert key in chi_square

    # Check entropy results
    entropy = result["entropy"]
    required_entropy_keys = [
        "shannon_entropy", "max_possible_entropy", "normalized_entropy"
    ]

    for key in required_entropy_keys:
        assert key in entropy


def test_analyze_number_randomness_date_filters():
    """Test randomness analysis with date filtering."""
    from datetime import date, timedelta

    with SessionLocal() as session:
        # Test with specific date range
        end_date = date.today()
        start_date = end_date - timedelta(days=30)

        result = analyze_number_randomness(
            session,
            game_type="lotto",
            date_from=start_date,
            date_to=end_date
        )

        assert result["analysis_period"]["date_from"] == start_date.isoformat()
        assert result["analysis_period"]["date_to"] == end_date.isoformat()
        assert result["analysis_period"]["window_days"] is None  # Should be None when dates provided


def test_analyze_number_randomness_coverage():
    """Test that randomness analysis covers all expected numbers."""
    with SessionLocal() as session:
        result = analyze_number_randomness(session, game_type="lotto", window_days=365)

        sample_size = result["sample_size"]

        # Should have some coverage data
        assert "coverage_percentage" in sample_size
        assert 0 <= sample_size["coverage_percentage"] <= 100

        # Numbers covered should be reasonable
        assert 0 <= sample_size["numbers_covered"] <= 49


def test_entropy_calculation():
    """Test entropy calculation in randomness analysis."""
    with SessionLocal() as session:
        result = analyze_number_randomness(session, game_type="lotto", window_days=30)

        entropy = result["entropy"]

        # Shannon entropy should be >= 0
        assert entropy["shannon_entropy"] >= 0

        # Max possible entropy for 49 numbers is log2(49)
        import math
        expected_max = math.log2(49)
        assert entropy["max_possible_entropy"] == expected_max

        # Normalized entropy should be 0-1
        assert 0 <= entropy["normalized_entropy"] <= 1


def test_ks_uniform_distribution():
    """Test KS test with perfectly uniform distribution (should be random)."""
    # Perfectly uniform distribution: each number appears exactly 10 times
    observed = {i: 10 for i in range(1, 50)}
    result = kolmogorov_smirnov_test(observed)

    assert abs(result["ks_statistic"]) < 1e-10  # Perfect fit ≈ 0
    assert result["p_value"] == 1.0  # p=1.0 for perfect fit
    assert result["is_random"] is True
    assert result["critical_value"] > 0


def test_ks_skewed_distribution():
    """Test KS test with heavily skewed distribution (should not be random)."""
    # Very skewed distribution: one number appears 300 times, others appear 1 time each
    observed = {1: 300}
    for i in range(2, 50):
        observed[i] = 1

    result = kolmogorov_smirnov_test(observed)

    assert result["ks_statistic"] > 0  # Some deviation
    assert result["p_value"] < 0.05  # Very unlikely to be random
    assert result["is_random"] is False
    assert result["critical_value"] > 0


def test_ks_empty_data():
    """Test KS test with empty data."""
    result = kolmogorov_smirnov_test({})

    assert result["ks_statistic"] == 0.0
    assert result["p_value"] == 1.0
    assert result["is_random"] is True
    assert result["critical_value"] == 1.36


def test_ks_single_observation():
    """Test KS test with minimal data."""
    observed = {25: 1}  # Only one observation
    result = kolmogorov_smirnov_test(observed)

    assert result["ks_statistic"] >= 0
    assert result["p_value"] >= 0
    assert isinstance(result["is_random"], bool)
    assert result["critical_value"] > 0


def test_runs_test_random_sequence():
    """Test runs test with a random-like sequence."""
    # Random sequence: alternating high/low numbers
    sequence = [5, 35, 12, 42, 8, 28, 15, 38, 3, 45]
    result = runs_test(sequence, "median")

    assert result["observed_runs"] > 0
    assert result["expected_runs"] > 0
    assert isinstance(result["p_value"], float)
    assert isinstance(result["is_random"], bool)
    assert result["test_type"] == "median"
    assert result["n1"] + result["n2"] == len(sequence)


def test_runs_test_trending_sequence():
    """Test runs test with a trending sequence (should show non-randomness)."""
    # Sequence with some ascending and descending: should have more variation
    sequence = [1, 3, 2, 5, 4, 7, 6, 9, 8, 10]  # Alternating up/down slightly
    result = runs_test(sequence, "ascending")

    # This sequence has both ascending and descending runs
    assert result["observed_runs"] >= 3  # Multiple runs expected
    assert result["n1"] > 0  # Some ascending
    assert result["n2"] > 0  # Some descending
    assert isinstance(result["p_value"], float)


def test_runs_test_empty_sequence():
    """Test runs test with empty sequence."""
    result = runs_test([], "median")

    assert result["observed_runs"] == 0
    assert result["expected_runs"] == 0.0
    assert result["p_value"] == 1.0
    assert result["is_random"] is True


def test_runs_test_single_element():
    """Test runs test with single element."""
    result = runs_test([25], "median")

    assert result["observed_runs"] == 0
    assert result["expected_runs"] == 0.0
    assert result["p_value"] == 1.0
    assert result["is_random"] is True


def test_runs_test_even_odd():
    """Test runs test with even/odd classification."""
    # Mix of even and odd numbers
    sequence = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # Even, odd, even, odd, etc.
    result = runs_test(sequence, "even_odd")

    assert result["test_type"] == "even_odd"
    assert result["n1"] > 0  # Number of even numbers
    assert result["n2"] > 0  # Number of odd numbers
    assert result["observed_runs"] > 0


def test_runs_test_high_low():
    """Test runs test with high/low classification."""
    # Mix of high and low numbers
    sequence = [5, 35, 12, 42, 8, 28]  # Low, high, low, high, low, high
    result = runs_test(sequence, "high_low")

    assert result["test_type"] == "high_low"
    assert result["n1"] + result["n2"] == len(sequence)
    assert isinstance(result["p_value"], float)


def test_runs_test_invalid_type():
    """Test runs test with invalid test type."""
    sequence = [1, 2, 3, 4, 5]

    with pytest.raises(ValueError):
        runs_test(sequence, "invalid_type")


def test_autocorrelation_random_sequence():
    """Test autocorrelation with a random-like sequence (should show no significant autocorrelation)."""
    # Generate a pseudo-random sequence
    sequence = [15, 32, 8, 47, 23, 12, 39, 5, 28, 41, 16, 33, 9, 48, 24, 13, 40, 6, 29, 42]
    result = autocorrelation_test(sequence)

    assert result["sample_size"] == len(sequence)
    assert isinstance(result["autocorrelations"], dict)
    assert isinstance(result["p_values"], dict)
    assert isinstance(result["significant_lags"], list)
    assert isinstance(result["overall_significance"], bool)
    assert len(result["autocorrelations"]) > 0  # Should have tested some lags


def test_autocorrelation_trending_sequence():
    """Test autocorrelation with a trending sequence (should show significant autocorrelation)."""
    # Linear trend: should show strong autocorrelation at lag 1
    sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    result = autocorrelation_test(sequence)

    assert result["sample_size"] == len(sequence)
    assert 1 in result["autocorrelations"]  # Lag 1 should be calculated
    assert result["autocorrelations"][1] > 0.8  # Strong positive correlation expected
    # Should have significant autocorrelation
    assert len(result["significant_lags"]) > 0
    assert result["overall_significance"] is True


def test_autocorrelation_oscillating_sequence():
    """Test autocorrelation with an oscillating sequence (should show negative autocorrelation at lag 1)."""
    # Alternating high/low pattern
    sequence = [10, 2, 10, 2, 10, 2, 10, 2, 10, 2, 10, 2, 10, 2, 10, 2]
    result = autocorrelation_test(sequence)

    assert result["sample_size"] == len(sequence)
    assert 1 in result["autocorrelations"]  # Lag 1 should be calculated
    assert result["autocorrelations"][1] < -0.5  # Strong negative correlation expected
    assert len(result["significant_lags"]) > 0  # Should be significant
    assert result["overall_significance"] is True


def test_autocorrelation_short_sequence():
    """Test autocorrelation with minimal sequence."""
    result = autocorrelation_test([1, 2])

    assert result["sample_size"] == 2
    assert 1 in result["autocorrelations"]  # Should test lag 1 for n=2
    assert result["significant_lags"] == []  # But no lags should be significant
    assert result["overall_significance"] is False


def test_autocorrelation_empty_sequence():
    """Test autocorrelation with empty sequence."""
    result = autocorrelation_test([])

    assert result["sample_size"] == 0
    assert result["autocorrelations"] == {}
    assert result["significant_lags"] == []
    assert result["overall_significance"] is False


def test_autocorrelation_single_element():
    """Test autocorrelation with single element."""
    result = autocorrelation_test([25])

    assert result["sample_size"] == 1
    assert result["autocorrelations"] == {}
    assert result["significant_lags"] == []
    assert result["overall_significance"] is False


def test_autocorrelation_specific_lags():
    """Test autocorrelation with specific lags only."""
    sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = autocorrelation_test(sequence, lags=[1, 5])

    assert result["sample_size"] == len(sequence)
    assert 1 in result["autocorrelations"]
    assert 5 not in result["autocorrelations"]  # Lag 5 > n/3=3, should be filtered out
    assert 2 not in result["autocorrelations"]  # Should not have tested lag 2


def test_autocorrelation_too_many_lags():
    """Test autocorrelation when requested lags exceed sequence length."""
    sequence = [1, 2, 3, 4, 5]
    result = autocorrelation_test(sequence, lags=[1, 2, 3, 4, 5, 6, 7])

    # Should only test valid lags (< n/3 = 1.66, so max lag 1)
    assert 1 in result["autocorrelations"]
    # For n=5, n//3=1, so max_valid_lag=1, only lag 1 should be tested
    assert 2 not in result["autocorrelations"]  # Lag 2 should be filtered out
