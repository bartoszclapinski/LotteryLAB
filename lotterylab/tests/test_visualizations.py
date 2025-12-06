"""
Tests for visualization analysis module.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch

from src.analysis.visualizations import (
    calculate_number_correlations,
    analyze_number_clusters,
    create_correlation_heatmap_data
)


def test_calculate_number_correlations_basic():
    """Test basic correlation calculation with mock data."""
    mock_session = Mock()

    # Mock the repository to return sample draws
    mock_repo = Mock()
    mock_draws = [
        {"numbers": "1,2,3,4,5,6"},
        {"numbers": "7,8,9,10,11,12"},
        {"numbers": "1,3,5,7,9,11"},
        {"numbers": "2,4,6,8,10,12"},
        {"numbers": "1,2,3,7,8,9"},
        {"numbers": "13,14,15,16,17,18"},  # Additional draws for sufficient data
        {"numbers": "19,20,21,22,23,24"},
        {"numbers": "25,26,27,28,29,30"},
    ]
    mock_repo.list.return_value = mock_draws

    with patch('src.analysis.visualizations.DrawRepository', return_value=mock_repo):
        result = calculate_number_correlations(mock_session, game_type="lotto", window_days=365)

        assert "correlation_matrix" in result
        assert "summary_stats" in result
        assert "significant_pairs" in result
        assert "top_pairs" in result
        assert result["total_draws_analyzed"] == 8
        assert isinstance(result["summary_stats"]["average_correlation"], float)
        assert result["summary_stats"]["average_correlation"] >= -1.0
        assert result["summary_stats"]["average_correlation"] <= 1.0


def test_calculate_number_correlations_insufficient_data():
    """Test correlation calculation with insufficient data."""
    mock_session = Mock()
    mock_repo = Mock()
    mock_repo.list.return_value = [{"numbers": "1,2,3"}]  # Only one draw

    with patch('src.analysis.visualizations.DrawRepository', return_value=mock_repo):
        result = calculate_number_correlations(mock_session, game_type="lotto")

        assert "error" in result
        assert "Insufficient draw data" in result["error"]


def test_calculate_number_correlations_no_data():
    """Test correlation calculation with no data."""
    mock_session = Mock()
    mock_repo = Mock()
    mock_repo.list.return_value = []

    with patch('src.analysis.visualizations.DrawRepository', return_value=mock_repo):
        result = calculate_number_correlations(mock_session, game_type="lotto")

        assert "error" in result
        assert "No draws found" in result["error"]


def test_calculate_number_correlations_invalid_data():
    """Test correlation calculation with invalid data."""
    mock_session = Mock()
    mock_repo = Mock()
    mock_repo.list.return_value = [
        {"numbers": "invalid"},
        {"numbers": "1,2,3,4,5,6"},
        {"numbers": "7,8,9,10,11,12"},
        {"numbers": "also_invalid"},
        {"numbers": "1,2,3,7,8,9"},
        {"numbers": "13,14,15,16,17,18"},  # Additional valid draws
        {"numbers": "19,20,21,22,23,24"},
        {"numbers": "25,26,27,28,29,30"},
    ]

    with patch('src.analysis.visualizations.DrawRepository', return_value=mock_repo):
        result = calculate_number_correlations(mock_session, game_type="lotto")

        # Should still work with valid data
        assert "correlation_matrix" in result
        assert result["total_draws_analyzed"] == 6  # Only valid draws


def test_analyze_number_clusters():
    """Test number clustering analysis."""
    mock_session = Mock()
    mock_repo = Mock()

    # Create mock draws with some clustering patterns
    mock_draws = [
        {"numbers": "1,2,3,10,11,12"},  # Two clusters
        {"numbers": "4,5,6,13,14,15"},  # Two clusters
        {"numbers": "1,3,5,7,9,11"},    # Spread out
        {"numbers": "2,4,6,8,10,12"},   # Even numbers
        {"numbers": "1,2,3,4,5,6"},     # Consecutive
        {"numbers": "7,8,9,10,11,12"},  # Consecutive
        {"numbers": "1,2,7,8,13,14"},   # Mixed clusters
    ] * 5  # Repeat to have enough data

    mock_repo.list.return_value = mock_draws

    with patch('src.analysis.visualizations.DrawRepository', return_value=mock_repo):
        result = analyze_number_clusters(mock_session, game_type="lotto")

        assert "frequent_pairs" in result
        assert "number_partners" in result
        assert "cluster_insights" in result
        assert result["total_draws_analyzed"] == len(mock_draws)
        assert len(result["frequent_pairs"]) > 0


def test_analyze_number_clusters_insufficient_data():
    """Test clustering analysis with insufficient data."""
    mock_session = Mock()
    mock_repo = Mock()
    mock_repo.list.return_value = [{"numbers": "1,2,3"}]  # Only one draw

    with patch('src.analysis.visualizations.DrawRepository', return_value=mock_repo):
        result = analyze_number_clusters(mock_session, game_type="lotto")

        assert "error" in result
        assert "Insufficient data" in result["error"]


def test_create_correlation_heatmap_data():
    """Test heatmap data preparation."""
    mock_session = Mock()
    mock_repo = Mock()

    # Mock data similar to correlation test
    mock_draws = [
        {"numbers": "1,2,3,4,5,6"},
        {"numbers": "7,8,9,10,11,12"},
        {"numbers": "1,3,5,7,9,11"},
        {"numbers": "2,4,6,8,10,12"},
        {"numbers": "1,2,3,7,8,9"},
        {"numbers": "13,14,15,16,17,18"},
        {"numbers": "19,20,21,22,23,24"},
        {"numbers": "25,26,27,28,29,30"},
    ]
    mock_repo.list.return_value = mock_draws

    with patch('src.analysis.visualizations.DrawRepository', return_value=mock_repo):
        result = create_correlation_heatmap_data(mock_session, game_type="lotto")

        assert "numbers" in result
        assert "correlation_matrix" in result
        assert "summary" in result
        assert "top_pairs" in result
        assert result["game_type"] == "lotto"
        assert result["total_draws"] == 8

        # Check that correlation_matrix is a 2D array
        assert isinstance(result["correlation_matrix"], list)
        assert len(result["correlation_matrix"]) == len(result["numbers"])


def test_create_correlation_heatmap_data_error():
    """Test heatmap data preparation with error."""
    mock_session = Mock()
    mock_repo = Mock()
    mock_repo.list.return_value = []  # No data

    with patch('src.analysis.visualizations.DrawRepository', return_value=mock_repo):
        result = create_correlation_heatmap_data(mock_session, game_type="lotto")

        assert "error" in result


def test_correlation_matrix_properties():
    """Test that correlation matrix has expected mathematical properties."""
    mock_session = Mock()
    mock_repo = Mock()

    # Create a larger dataset for better statistical properties
    mock_draws = []
    for i in range(50):  # 50 draws
        # Create some patterns but mostly random
        base = np.random.randint(1, 40, 6)
        draw_str = ",".join(map(str, sorted(base)))
        mock_draws.append({"numbers": draw_str})

    mock_repo.list.return_value = mock_draws

    with patch('src.analysis.visualizations.DrawRepository', return_value=mock_repo):
        result = calculate_number_correlations(mock_session, game_type="lotto")

        if "error" not in result:
            corr_matrix = result["correlation_matrix"]

            # Check that diagonal is 1.0 (self-correlation)
            numbers = list(corr_matrix.keys())
            for num in numbers:
                assert abs(corr_matrix[num][num] - 1.0) < 1e-10, f"Diagonal should be 1.0 for {num}"

            # Check symmetry (correlation matrix should be symmetric)
            for i, num1 in enumerate(numbers):
                for j, num2 in enumerate(numbers):
                    assert abs(corr_matrix[num1][num2] - corr_matrix[num2][num1]) < 1e-10, \
                           f"Matrix should be symmetric: {num1},{num2}"

            # Check range (-1 to 1)
            for num1 in numbers:
                for num2 in numbers:
                    corr_val = corr_matrix[num1][num2]
                    assert -1.0 <= corr_val <= 1.0, f"Correlation should be between -1 and 1: {corr_val}"


def test_significant_pairs_filtering():
    """Test that significant pairs are properly filtered."""
    mock_session = Mock()
    mock_repo = Mock()

    # Create a dataset with known correlations
    mock_draws = []
    for i in range(100):  # Large dataset for statistical significance
        if i % 2 == 0:
            # Even draws: numbers 1,2,3 tend to appear together
            draw = [1, 2, 3] + list(np.random.randint(4, 49, 3))
        else:
            # Odd draws: numbers 45,46,47 tend to appear together
            draw = [45, 46, 47] + list(np.random.randint(4, 44, 3))

        np.random.shuffle(draw)
        mock_draws.append({"numbers": ",".join(map(str, draw))})

    mock_repo.list.return_value = mock_draws

    with patch('src.analysis.visualizations.DrawRepository', return_value=mock_repo):
        result = calculate_number_correlations(mock_session, game_type="lotto")

        if "error" not in result:
            significant_pairs = result["significant_pairs"]

            # Should find some significant pairs
            assert len(significant_pairs) > 0

            # Check that pairs are sorted by correlation strength
            correlations = [abs(p["correlation"]) for p in significant_pairs]
            assert correlations == sorted(correlations, reverse=True)

            # Check that significant pairs have proper structure
            for pair in significant_pairs[:5]:  # Check first few
                assert "number1" in pair
                assert "number2" in pair
                assert "correlation" in pair
                assert "p_value" in pair
                assert "significant" in pair
                assert isinstance(pair["significant"], (bool, np.bool_))
