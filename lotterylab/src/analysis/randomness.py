"""
Randomness analysis module for Lottery Lab.

This module implements statistical tests to verify the randomness of lottery draws,
focusing on whether number distributions follow expected patterns.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple
from collections import Counter
import math
from scipy import stats
import numpy as np

from src.database.session import SessionLocal
from src.database.models import Draw


def chi_square_goodness_of_fit(
    observed_frequencies: Dict[int, int],
    expected_frequency: Optional[float] = None,
    degrees_of_freedom: Optional[int] = None
) -> Dict[str, float]:
    """
    Perform chi-square goodness-of-fit test to determine if observed frequencies
    match expected frequencies (uniform distribution for lottery numbers).

    H0: The observed frequencies follow the expected uniform distribution (random)
    H1: The observed frequencies do not follow the expected distribution (not random)

    Args:
        observed_frequencies: Dictionary mapping numbers (1-49) to their observed counts
        expected_frequency: Expected frequency per number (if None, calculated as uniform)
        degrees_of_freedom: Degrees of freedom (if None, calculated as len(observed)-1)

    Returns:
        Dictionary with test results:
        - chi_square_statistic: The chi-square test statistic
        - p_value: Probability of observing this result if H0 is true
        - degrees_of_freedom: Degrees of freedom used
        - is_random: Boolean indicating if result suggests randomness (p > 0.05)
        - expected_frequency: Expected frequency used
    """
    if not observed_frequencies:
        return {
            "chi_square_statistic": 0.0,
            "p_value": 1.0,
            "degrees_of_freedom": 0,
            "is_random": True,
            "expected_frequency": 0.0,
            "total_observations": 0
        }

    # Sort frequencies by number for consistent processing
    sorted_freqs = dict(sorted(observed_frequencies.items()))
    observed = list(sorted_freqs.values())

    total_observations = sum(observed)

    if total_observations == 0:
        return {
            "chi_square_statistic": 0.0,
            "p_value": 1.0,
            "degrees_of_freedom": 0,
            "is_random": True,
            "expected_frequency": 0.0,
            "total_observations": 0
        }

    # For lottery numbers, expected frequency should be uniform across all numbers
    # The expected frequency per number = total_observations / number_of_categories
    if expected_frequency is None:
        # For uniform distribution, expected = total / number of categories
        expected_frequency = total_observations / len(observed)

    expected = [expected_frequency] * len(observed)

    # Calculate chi-square statistic
    chi_square_stat = 0.0
    for obs, exp in zip(observed, expected):
        if exp > 0:  # Avoid division by zero
            chi_square_stat += ((obs - exp) ** 2) / exp

    # Degrees of freedom = number of categories - 1
    if degrees_of_freedom is None:
        degrees_of_freedom = len(observed) - 1

    # Calculate p-value using chi-square distribution
    p_value = 1 - stats.chi2.cdf(chi_square_stat, degrees_of_freedom)

    return {
        "chi_square_statistic": float(chi_square_stat),
        "p_value": float(p_value),
        "degrees_of_freedom": int(degrees_of_freedom),
        "is_random": bool(p_value > 0.05),  # Common significance level
        "expected_frequency": float(expected_frequency),
        "total_observations": int(total_observations)
    }


def autocorrelation_test(
    draw_sequence: List[int],
    lags: List[int] = None,
    max_lags: int = 10
) -> Dict[str, any]:
    """
    Perform autocorrelation analysis to detect temporal dependencies.

    Autocorrelation measures the correlation between a time series and its lagged versions.
    For lottery analysis, we test if past draws influence future draws.

    H0: No autocorrelation (draws are independent)
    H1: Significant autocorrelation (temporal dependencies exist)

    Args:
        draw_sequence: List of numbers in chronological order
        lags: Specific lags to test (if None, tests up to max_lags)
        max_lags: Maximum number of lags to test

    Returns:
        Dictionary with autocorrelation results:
        - autocorrelations: Dict of lag -> autocorrelation coefficient
        - significant_lags: List of lags with significant autocorrelation (p < 0.05)
        - p_values: Dict of lag -> p-value
        - confidence_intervals: Dict of lag -> (lower, upper) 95% CI
        - overall_significance: Boolean indicating if any lag shows significance
    """
    if not draw_sequence or len(draw_sequence) < 2:
        return {
            "autocorrelations": {},
            "significant_lags": [],
            "p_values": {},
            "confidence_intervals": {},
            "overall_significance": False,
            "sample_size": len(draw_sequence)
        }

    n = len(draw_sequence)

    # Determine which lags to test
    if lags is None:
        max_valid_lag = max(1, n // 3)  # At least 1, but don't test lags > n/3
        lags = list(range(1, min(max_lags + 1, max_valid_lag + 1)))
    else:
        # Filter provided lags to only include valid ones (< n/3 and < n)
        max_valid_lag = max(1, n // 3)
        lags = [lag for lag in lags if 1 <= lag < n and lag <= max_valid_lag]

    if not lags:
        return {
            "autocorrelations": {},
            "significant_lags": [],
            "p_values": {},
            "confidence_intervals": {},
            "overall_significance": False,
            "sample_size": n
        }

    # Convert to numpy array for easier computation
    data = np.array(draw_sequence)

    results = {
        "autocorrelations": {},
        "significant_lags": [],
        "p_values": {},
        "confidence_intervals": {},
        "overall_significance": False,
        "sample_size": n
    }

    # Calculate autocorrelation for each lag
    for lag in lags:
        if lag >= n:
            continue

        # Calculate autocorrelation coefficient
        try:
            # Use pandas autocorrelation for robust calculation
            import pandas as pd
            series = pd.Series(draw_sequence)
            acf = series.autocorr(lag=lag)
            results["autocorrelations"][lag] = float(acf) if not np.isnan(acf) else 0.0

            # Calculate p-value using Ljung-Box test for this lag
            try:
                from statsmodels.stats.diagnostic import acorr_ljungbox
                lb_test = acorr_ljungbox(series, lags=[lag], return_df=True)
                p_value = lb_test['lb_pvalue'].iloc[0]
            except ImportError:
                # Fallback: approximate p-value using normal distribution
                # For large samples, acf / sqrt(1/n) is approximately normal(0, 1/sqrt(n))
                standard_error = 1.0 / math.sqrt(n)
                z_score = abs(acf) / standard_error
                p_value = 2 * (1 - stats.norm.cdf(z_score))

            results["p_values"][lag] = float(p_value)

            # Calculate 95% confidence intervals
            # For large samples: ±1.96 * sqrt(1/n)
            lower_bound = acf - 1.96 * math.sqrt(1.0 / n)
            upper_bound = acf + 1.96 * math.sqrt(1.0 / n)
            results["confidence_intervals"][lag] = (float(lower_bound), float(upper_bound))

            # Check significance
            if p_value < 0.05:
                results["significant_lags"].append(lag)

        except Exception as e:
            # If calculation fails for this lag, skip it
            print(f"Warning: Autocorrelation calculation failed for lag {lag}: {e}")
            continue

    # Overall significance: any lag shows significant autocorrelation
    results["overall_significance"] = len(results["significant_lags"]) > 0

    return results


def runs_test(
    draw_sequence: List[int],
    test_type: str = "median"
) -> Dict[str, float]:
    """
    Perform runs test to check for sequence randomness.

    The runs test examines whether the sequence has the expected number of "runs"
    (consecutive sequences of the same type). Too few or too many runs suggest
    non-randomness.

    H0: The sequence is randomly ordered (expected number of runs)
    H1: The sequence is not randomly ordered (too few/many runs)

    Args:
        draw_sequence: List of numbers in the order they appeared
        test_type: Type of runs test - "median", "even_odd", "high_low", "ascending"

    Returns:
        Dictionary with test results:
        - observed_runs: Number of runs observed
        - expected_runs: Expected number of runs under randomness
        - z_score: Standardized test statistic
        - p_value: Two-tailed p-value
        - is_random: Boolean indicating if result suggests randomness (p > 0.05)
        - test_type: Type of test performed
    """
    if not draw_sequence or len(draw_sequence) < 2:
        return {
            "observed_runs": 0,
            "expected_runs": 0.0,
            "z_score": 0.0,
            "p_value": 1.0,
            "is_random": True,
            "test_type": test_type
        }

    n = len(draw_sequence)

    # Define the binary classification based on test type
    if test_type == "median":
        # Above/below median
        median = sorted(draw_sequence)[n // 2]
        binary_sequence = [1 if x > median else 0 for x in draw_sequence]
    elif test_type == "even_odd":
        # Even/odd
        binary_sequence = [1 if x % 2 == 0 else 0 for x in draw_sequence]
    elif test_type == "high_low":
        # High (26-49) vs Low (1-24) numbers
        binary_sequence = [1 if x > 25 else 0 for x in draw_sequence]
    elif test_type == "ascending":
        # Ascending/descending (compared to previous)
        binary_sequence = [1]  # First number is always a "run" start
        for i in range(1, n):
            if draw_sequence[i] > draw_sequence[i-1]:
                binary_sequence.append(1)  # ascending
            else:
                binary_sequence.append(0)  # descending or equal
    else:
        raise ValueError(f"Unknown test_type: {test_type}")

    # Count runs: consecutive sequences of the same value
    runs = 1  # At least one run
    for i in range(1, len(binary_sequence)):
        if binary_sequence[i] != binary_sequence[i-1]:
            runs += 1

    # Count number of 1s and 0s
    n1 = sum(binary_sequence)  # number of 1s
    n2 = n - n1  # number of 0s

    # Expected runs under randomness
    if n1 == 0 or n2 == 0:
        expected_runs = 1.0  # Only one type present
    else:
        expected_runs = (2 * n1 * n2) / (n1 + n2) + 1

    # Variance of runs
    if n1 == 0 or n2 == 0:
        variance = 0.0
    else:
        variance = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / ((n1 + n2) ** 2 * (n1 + n2 - 1))

    # Z-score and p-value
    if variance == 0:
        z_score = 0.0
        p_value = 1.0
    else:
        z_score = (runs - expected_runs) / math.sqrt(variance)
        # Two-tailed test using normal approximation
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

    return {
        "observed_runs": runs,
        "expected_runs": float(expected_runs),
        "z_score": float(z_score),
        "p_value": float(p_value),
        "is_random": bool(p_value > 0.05),
        "test_type": test_type,
        "n1": n1,
        "n2": n2
    }


def kolmogorov_smirnov_test(
    observed_frequencies: Dict[int, int],
    expected_distribution: Optional[List[float]] = None
) -> Dict[str, float]:
    """
    Perform Kolmogorov-Smirnov test to compare observed distribution against expected.

    The KS test measures the maximum difference between the empirical distribution
    function of the observed data and the cumulative distribution function of the
    reference distribution.

    H0: The observed data follows the expected distribution (random)
    H1: The observed data does not follow the expected distribution (not random)

    Args:
        observed_frequencies: Dictionary mapping numbers to their observed counts
        expected_distribution: Expected probabilities for each number (if None, uniform)

    Returns:
        Dictionary with test results:
        - ks_statistic: The KS test statistic (maximum difference)
        - p_value: Probability of observing this result if H0 is true
        - is_random: Boolean indicating if result suggests randomness (p > 0.05)
        - critical_value: Critical value at 0.05 significance level
    """
    if not observed_frequencies:
        return {
            "ks_statistic": 0.0,
            "p_value": 1.0,
            "is_random": True,
            "critical_value": 1.36  # For large samples
        }

    # Convert frequencies to empirical distribution
    total_observations = sum(observed_frequencies.values())
    if total_observations == 0:
        return {
            "ks_statistic": 0.0,
            "p_value": 1.0,
            "is_random": True,
            "critical_value": 1.36
        }

    # Create empirical CDF from observed data
    numbers = sorted(observed_frequencies.keys())
    observed_counts = [observed_frequencies.get(num, 0) for num in numbers]
    observed_cdf = np.cumsum(observed_counts) / total_observations

    # Create expected CDF (uniform distribution by default)
    if expected_distribution is None:
        # Uniform distribution: each number has equal probability
        expected_prob = 1.0 / len(numbers)
        expected_cdf = np.cumsum([expected_prob] * len(numbers))
    else:
        expected_cdf = np.cumsum(expected_distribution)

    # Calculate KS statistic (maximum absolute difference)
    ks_statistic = max(abs(obs - exp) for obs, exp in zip(observed_cdf, expected_cdf))

    # Calculate p-value using Kolmogorov-Smirnov distribution approximation
    n = total_observations

    # For perfect fit (KS statistic very close to 0), p-value should be 1.0
    if ks_statistic < 1e-10:
        p_value = 1.0
    elif n > 35:  # Use approximation for large samples
        # More accurate approximation for KS test p-value
        # The formula varies, but for two-sided test: p ≈ 2 * exp(-2 * n * ks^2)
        # However, this can exceed 1, so we need to cap it
        p_value = min(1.0, 2 * math.exp(-2 * n * ks_statistic**2))
    else:  # Use scipy for small samples
        # Convert to format scipy expects
        observed_data = []
        for num, count in observed_frequencies.items():
            observed_data.extend([num] * count)

        if expected_distribution is None:
            # Test against uniform distribution
            expected_probs = [1.0/49] * 49  # Lotto has 49 numbers
            p_value = stats.kstest(observed_data, lambda x: stats.uniform.cdf(x, 1, 49), alternative='two-sided').pvalue
        else:
            # Test against custom distribution (would need more complex setup)
            p_value = 1.0  # Placeholder

    # Critical value for 95% confidence (approximate)
    critical_value = 1.36 / math.sqrt(n) if n > 0 else 1.36

    return {
        "ks_statistic": float(ks_statistic),
        "p_value": float(p_value),
        "is_random": bool(p_value > 0.05),
        "critical_value": float(critical_value)
    }


def analyze_number_randomness(
    session: SessionLocal,
    game_type: str = "lotto",
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    window_days: Optional[int] = None,
    game_provider: Optional[str] = None
) -> Dict[str, any]:
    """
    Analyze the randomness of lottery draws using multiple statistical tests.

    Args:
        session: Database session
        game_type: Type of game to analyze
        date_from: Start date for analysis
        date_to: End date for analysis
        window_days: Number of days to look back
        game_provider: Game provider filter

    Returns:
        Dictionary containing randomness analysis results
    """
    # Import here to avoid circular imports
    from src.analysis.frequency import calculate_frequency, count_draws

    # Get frequency data
    freq_data = calculate_frequency(
        session=session,
        game_type=game_type,
        date_from=date_from,
        date_to=date_to,
        window_days=window_days,
        game_provider=game_provider
    )

    total_draws = count_draws(
        session=session,
        game_type=game_type,
        date_from=date_from,
        date_to=date_to,
        window_days=window_days,
        game_provider=game_provider
    )

    # Perform chi-square test
    chi_square_result = chi_square_goodness_of_fit(freq_data)

    # Perform Kolmogorov-Smirnov test
    ks_result = kolmogorov_smirnov_test(freq_data)

    # Get recent draws for runs test (need sequence data)
    from src.repositories.draws import DrawRepository
    repo = DrawRepository(session)
    recent_draws = repo.list(limit=100, game_type=game_type)  # Get last 100 draws

    # Extract numbers from recent draws for runs test
    if recent_draws:
        # Flatten all numbers from recent draws into a sequence
        draw_sequences = []
        for draw in recent_draws:
            # Parse numbers from the comma-separated string
            if 'numbers' in draw and isinstance(draw['numbers'], str):
                # Split comma-separated string and convert to integers
                numbers = [int(x.strip()) for x in draw['numbers'].split(',') if x.strip()]
                draw_sequences.extend(numbers)
            elif 'draw_numbers' in draw and isinstance(draw['draw_numbers'], list):
                draw_sequences.extend(draw['draw_numbers'])
            # If neither, try to get individual number fields
            else:
                numbers = []
                for key in draw:
                    if key.startswith('num') and isinstance(draw[key], int):
                        numbers.append(draw[key])
                draw_sequences.extend(sorted(numbers))  # Sort to maintain order

        # Perform runs tests on the sequence
        runs_median = runs_test(draw_sequences, "median")
        runs_even_odd = runs_test(draw_sequences, "even_odd")
        runs_high_low = runs_test(draw_sequences, "high_low")

        # Perform autocorrelation analysis
        autocorrelation = autocorrelation_test(draw_sequences, max_lags=10)
    else:
        # No data available
        runs_median = runs_test([], "median")
        runs_even_odd = runs_test([], "even_odd")
        runs_high_low = runs_test([], "high_low")

    # Calculate additional randomness metrics
    numbers_drawn = [num for num, count in freq_data.items() if count > 0]
    coverage_percentage = len(numbers_drawn) / 49 * 100

    # Calculate entropy as a measure of randomness
    total_observations = sum(freq_data.values())
    entropy = 0.0
    if total_observations > 0:
        for count in freq_data.values():
            if count > 0:
                probability = count / total_observations
                entropy -= probability * math.log2(probability)

    return {
        "game_type": game_type,
        "analysis_period": {
            "date_from": str(date_from) if date_from else None,
            "date_to": str(date_to) if date_to else None,
            "window_days": window_days,
            "game_provider": game_provider
        },
        "sample_size": {
            "total_draws": int(total_draws),
            "total_observations": int(total_observations),
            "numbers_covered": int(len(numbers_drawn)),
            "coverage_percentage": float(coverage_percentage)
        },
        "chi_square_test": chi_square_result,
        "kolmogorov_smirnov_test": ks_result,
        "runs_test_median": runs_median,
        "runs_test_even_odd": runs_even_odd,
        "runs_test_high_low": runs_high_low,
        "autocorrelation_analysis": autocorrelation,
        "entropy": {
            "shannon_entropy": float(entropy),
            "max_possible_entropy": float(math.log2(49)),  # For 49 possible numbers
            "normalized_entropy": float(entropy / math.log2(49) if entropy > 0 else 0)
        },
        "summary": {
            "appears_random": bool(chi_square_result["is_random"]),
            "confidence_level": "95%" if chi_square_result["p_value"] > 0.05 else "Not at 95%",
            "data_quality": "Good" if total_draws >= 100 else "Limited sample"
        }
    }
