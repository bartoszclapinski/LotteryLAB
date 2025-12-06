"""
Visualization analysis module for Lottery Lab.

This module implements correlation analysis and other visualizations
to provide deeper insights into lottery data patterns.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
from scipy import stats
from collections import defaultdict
import math

from src.database.session import SessionLocal
from src.repositories.draws import DrawRepository


def calculate_number_correlations(
    session: SessionLocal,
    game_type: str = "lotto",
    window_days: Optional[int] = None,
    min_correlation: float = 0.05
) -> Dict[str, Any]:
    """
    Calculate correlation matrix between lottery numbers.

    This creates a correlation matrix showing which numbers tend to appear
    together in draws, indicating potential clustering patterns.

    Args:
        session: Database session
        game_type: Type of lottery game
        window_days: Number of days to look back (None for all data)
        min_correlation: Minimum correlation threshold to report

    Returns:
        Dictionary containing correlation matrix and analysis results
    """
    # Get draws data
    repo = DrawRepository(session)
    draws = repo.list(limit=5000, game_type=game_type)  # Get up to 5000 draws for analysis

    if not draws:
        return {
            "error": "No draws found for correlation analysis"
        }

    # Extract numbers from draws
    draw_numbers = []
    for draw in draws:
        if 'numbers' in draw and isinstance(draw['numbers'], str):
            try:
                numbers = [int(x.strip()) for x in draw['numbers'].split(',') if x.strip()]
                draw_numbers.append(numbers)
            except (ValueError, TypeError):
                continue

    if len(draw_numbers) < 5:
        return {
            "error": "Insufficient draw data for correlation analysis (need at least 5 draws)"
        }

    # Get unique numbers that appeared
    all_numbers = sorted(set(num for draw in draw_numbers for num in draw))

    # Create binary presence/absence matrix
    # Rows: draws, Columns: numbers (1 if number appeared in draw, 0 otherwise)
    presence_matrix = np.zeros((len(draw_numbers), len(all_numbers)))

    number_to_idx = {num: idx for idx, num in enumerate(all_numbers)}

    for draw_idx, draw in enumerate(draw_numbers):
        for num in draw:
            if num in number_to_idx:
                presence_matrix[draw_idx, number_to_idx[num]] = 1

    # Calculate correlation matrix using Pearson correlation
    # This shows which numbers co-occur more than expected by chance
    corr_matrix = np.corrcoef(presence_matrix.T)

    # Convert to DataFrame for easier manipulation
    corr_df = pd.DataFrame(corr_matrix, index=all_numbers, columns=all_numbers)

    # Find significant correlations
    significant_pairs = []
    for i in range(len(all_numbers)):
        for j in range(i + 1, len(all_numbers)):
            num1, num2 = all_numbers[i], all_numbers[j]
            corr_value = corr_matrix[i, j]

            # Calculate statistical significance (approximate)
            n = len(draw_numbers)
            if abs(corr_value) >= 0.999:  # Nearly perfect correlation
                p_value = 1e-10  # Very significant
            elif n <= 2:
                p_value = 1.0  # Not enough data for significance testing
            else:
                try:
                    denominator = 1 - corr_value**2
                    if denominator <= 0:
                        p_value = 1e-10  # Very significant
                    else:
                        t_stat = corr_value * np.sqrt((n - 2) / denominator)
                        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2))
                except (ZeroDivisionError, FloatingPointError):
                    p_value = 1.0  # Default to not significant

            if abs(corr_value) >= min_correlation:
                significant_pairs.append({
                    "number1": num1,
                    "number2": num2,
                    "correlation": float(corr_value),
                    "p_value": float(p_value),
                    "significant": p_value < 0.05
                })

    # Sort by absolute correlation strength
    significant_pairs.sort(key=lambda x: abs(x["correlation"]), reverse=True)

    # Calculate summary statistics
    corr_values = corr_matrix[np.triu_indices_from(corr_matrix, k=1)]
    avg_correlation = float(np.mean(corr_values))
    max_correlation = float(np.max(corr_values))
    min_correlation = float(np.min(corr_values))

    # Identify highly correlated number pairs (top 10)
    top_pairs = significant_pairs[:10]

    # Calculate correlation strength distribution
    corr_bins = [-1, -0.7, -0.3, -0.1, 0.1, 0.3, 0.7, 1.0]
    corr_labels = ["Strong Negative", "Moderate Negative", "Weak Negative",
                   "Weak Positive", "Moderate Positive", "Strong Positive"]

    corr_distribution = {}
    for i in range(len(corr_labels)):
        mask = (corr_values >= corr_bins[i]) & (corr_values < corr_bins[i + 1])
        corr_distribution[corr_labels[i]] = int(np.sum(mask))

    return {
        "game_type": game_type,
        "total_draws_analyzed": len(draw_numbers),
        "total_numbers": len(all_numbers),
        "correlation_matrix": corr_df.to_dict(),
        "significant_pairs": significant_pairs[:50],  # Limit to top 50 pairs
        "top_pairs": top_pairs,
        "summary_stats": {
            "average_correlation": avg_correlation,
            "max_correlation": max_correlation,
            "min_correlation": min_correlation,
            "correlation_distribution": corr_distribution
        },
        "analysis_metadata": {
            "min_correlation_threshold": min_correlation,
            "correlation_method": "pearson",
            "significance_level": 0.05
        }
    }


def analyze_number_clusters(
    session: SessionLocal,
    game_type: str = "lotto",
    window_days: Optional[int] = None
) -> Dict[str, Any]:
    """
    Analyze number clustering patterns in lottery draws.

    This identifies groups of numbers that frequently appear together,
    potentially indicating non-random clustering behavior.

    Args:
        session: Database session
        game_type: Type of lottery game
        window_days: Number of days to look back

    Returns:
        Dictionary with cluster analysis results
    """
    # Get draws data
    repo = DrawRepository(session)
    draws = repo.list(limit=2000, game_type=game_type)

    if not draws:
        return {"error": "No draws found for cluster analysis"}

    # Extract numbers
    draw_numbers = []
    for draw in draws:
        if 'numbers' in draw and isinstance(draw['numbers'], str):
            try:
                numbers = [int(x.strip()) for x in draw['numbers'].split(',') if x.strip()]
                draw_numbers.append(sorted(numbers))
            except (ValueError, TypeError):
                continue

    if len(draw_numbers) < 20:
        return {"error": "Insufficient data for cluster analysis"}

    # Calculate frequency of number pairs
    pair_frequencies = defaultdict(int)
    for draw in draw_numbers:
        for i in range(len(draw)):
            for j in range(i + 1, len(draw)):
                pair = tuple(sorted([draw[i], draw[j]]))
                pair_frequencies[pair] += 1

    # Find most frequent pairs
    frequent_pairs = []
    total_draws = len(draw_numbers)

    for pair, count in pair_frequencies.items():
        expected_frequency = (count / total_draws) * (total_draws - 1)
        # Simple chi-square test for significance
        observed = count
        expected = expected_frequency
        chi_square = ((observed - expected) ** 2) / expected if expected > 0 else 0

        frequent_pairs.append({
            "numbers": list(pair),
            "frequency": count,
            "percentage": float(count / total_draws * 100),
            "expected_frequency": float(expected_frequency),
            "chi_square": float(chi_square),
            "significant": chi_square > 3.84  # Chi-square critical value for p=0.05
        })

    # Sort by frequency
    frequent_pairs.sort(key=lambda x: x["frequency"], reverse=True)

    # Group numbers by their most frequent partners
    number_partners = defaultdict(list)
    for pair_info in frequent_pairs[:50]:  # Top 50 pairs
        num1, num2 = pair_info["numbers"]
        number_partners[num1].append({
            "partner": num2,
            "frequency": pair_info["frequency"],
            "percentage": pair_info["percentage"]
        })
        number_partners[num2].append({
            "partner": num1,
            "frequency": pair_info["frequency"],
            "percentage": pair_info["percentage"]
        })

    return {
        "game_type": game_type,
        "total_draws_analyzed": len(draw_numbers),
        "frequent_pairs": frequent_pairs[:20],  # Top 20 pairs
        "number_partners": dict(number_partners),
        "cluster_insights": {
            "most_connected_number": max(number_partners.keys(),
                                       key=lambda x: len(number_partners[x])) if number_partners else None,
            "total_significant_pairs": sum(1 for p in frequent_pairs if p["significant"]),
            "average_pair_frequency": float(np.mean([p["frequency"] for p in frequent_pairs]))
        }
    }


def create_correlation_heatmap_data(
    session: SessionLocal,
    game_type: str = "lotto",
    window_days: Optional[int] = None
) -> Dict[str, Any]:
    """
    Prepare data specifically formatted for heatmap visualization.

    Returns correlation matrix in a format suitable for Plotly heatmap.
    """
    correlation_data = calculate_number_correlations(session, game_type, window_days)

    if "error" in correlation_data:
        return correlation_data

    corr_matrix_dict = correlation_data["correlation_matrix"]

    # Extract numbers and correlation values
    numbers = list(corr_matrix_dict.keys())
    heatmap_values = []

    for num1 in numbers:
        row = []
        for num2 in numbers:
            # Ensure values are regular Python floats for JSON serialization
            value = float(corr_matrix_dict[num1][num2])
            row.append(value)
        heatmap_values.append(row)

    # Ensure all summary stats are JSON serializable
    summary = correlation_data["summary_stats"]
    json_safe_summary = {
        "average_correlation": float(summary["average_correlation"]),
        "max_correlation": float(summary["max_correlation"]),
        "min_correlation": float(summary["min_correlation"]),
        "correlation_distribution": summary["correlation_distribution"]
    }

    # Ensure top_pairs are JSON serializable
    json_safe_top_pairs = []
    for pair in correlation_data["top_pairs"]:
        json_safe_top_pairs.append({
            "number1": int(pair["number1"]),
            "number2": int(pair["number2"]),
            "correlation": float(pair["correlation"]),
            "p_value": float(pair["p_value"]),
            "significant": bool(pair["significant"])
        })

    return {
        "numbers": [int(n) for n in numbers],  # Ensure numbers are ints
        "correlation_matrix": heatmap_values,
        "summary": json_safe_summary,
        "top_pairs": json_safe_top_pairs,
        "game_type": game_type,
        "total_draws": int(correlation_data["total_draws_analyzed"])
    }
