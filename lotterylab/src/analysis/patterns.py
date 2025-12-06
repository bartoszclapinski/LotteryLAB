"""
Pattern detection module for Lottery Lab.

This module implements algorithms to detect patterns in lottery draws,
including consecutive numbers, arithmetic sequences, and other statistical patterns.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple, Set
from collections import defaultdict, Counter
import math
from scipy import stats
import numpy as np

from src.database.session import SessionLocal
from src.repositories.draws import DrawRepository


def detect_consecutive_numbers(draw_sequence: List[int], min_length: int = 2) -> Dict[str, any]:
    """
    Detect consecutive numbers in lottery draws.

    Args:
        draw_sequence: List of numbers from draws
        min_length: Minimum length of consecutive sequence to detect

    Returns:
        Dictionary with consecutive pattern results
    """
    if not draw_sequence or len(draw_sequence) < min_length:
        return {
            "total_sequences": 0,
            "max_length": 0,
            "avg_length": 0.0,
            "sequences": []
        }

    # Sort and find consecutive sequences
    sorted_numbers = sorted(draw_sequence)
    sequences = []
    current_sequence = [sorted_numbers[0]]

    for i in range(1, len(sorted_numbers)):
        if sorted_numbers[i] == current_sequence[-1] + 1:
            current_sequence.append(sorted_numbers[i])
        else:
            if len(current_sequence) >= min_length:
                sequences.append(current_sequence.copy())
            current_sequence = [sorted_numbers[i]]

    # Add last sequence if it meets criteria
    if len(current_sequence) >= min_length:
        sequences.append(current_sequence)

    # Calculate statistics
    total_sequences = len(sequences)
    max_length = max((len(seq) for seq in sequences), default=0)
    avg_length = sum(len(seq) for seq in sequences) / total_sequences if total_sequences > 0 else 0.0

    return {
        "total_sequences": total_sequences,
        "max_length": max_length,
        "avg_length": float(avg_length),
        "sequences": sequences
    }


def detect_arithmetic_sequences(draws: List[List[int]], min_length: int = 3) -> Dict[str, any]:
    """
    Detect arithmetic sequences in draws.

    Args:
        draws: List of draws (each draw is a list of numbers)
        min_length: Minimum length of arithmetic sequence

    Returns:
        Dictionary with arithmetic sequence results
    """
    if not draws or len(draws) < min_length:
        return {
            "total_sequences": 0,
            "sequences_found": [],
            "common_differences": {}
        }

    sequences_found = []
    all_differences = []

    for draw in draws:
        if not isinstance(draw, list) or len(draw) < min_length:
            continue

        # Convert string numbers to integers if needed
        try:
            draw_nums = [int(x) for x in draw] if isinstance(draw[0], str) else draw
        except (ValueError, TypeError):
            continue

        # Check for arithmetic sequences in each draw
        for i in range(len(draw_nums)):
            for j in range(i + min_length, len(draw_nums) + 1):
                sequence = draw_nums[i:j]
                if len(sequence) < min_length:
                    continue

                # Check if it's an arithmetic sequence
                differences = []
                is_arithmetic = True
                for k in range(1, len(sequence)):
                    diff = sequence[k] - sequence[k-1]
                    differences.append(diff)
                    if k > 1 and diff != differences[0]:
                        is_arithmetic = False
                        break

                if is_arithmetic and len(sequence) >= min_length:
                    sequences_found.append({
                        "draw": draw,
                        "sequence": sequence,
                        "common_difference": differences[0] if differences else 0,
                        "length": len(sequence)
                    })
                    all_differences.extend(differences)

    # Analyze common differences
    common_differences = dict(Counter(all_differences))

    return {
        "total_sequences": len(sequences_found),
        "sequences_found": sequences_found,
        "common_differences": common_differences
    }


def detect_digit_patterns(draw_sequence: List[int]) -> Dict[str, any]:
    """
    Detect patterns based on individual digits.

    Args:
        draw_sequence: List of numbers from draws

    Returns:
        Dictionary with digit pattern analysis
    """
    if not draw_sequence:
        return {
            "digit_frequencies": {},
            "repeating_digits": {},
            "digit_sums": {},
            "digit_products": {}
        }

    # Extract digits from each number
    all_digits = []
    digit_sums = []
    digit_products = []

    for number in draw_sequence:
        digits = [int(d) for d in str(number)]
        all_digits.extend(digits)

        # Calculate digit sum and product
        digit_sum = sum(digits)
        digit_product = math.prod(digits) if digits else 0

        digit_sums.append(digit_sum)
        digit_products.append(digit_product)

    # Analyze digit frequencies
    digit_frequencies = dict(Counter(all_digits))

    # Find repeating digit patterns
    repeating_digits = {}
    for digit, count in digit_frequencies.items():
        if count > 1:
            repeating_digits[digit] = count

    # Analyze digit sums
    sum_frequencies = dict(Counter(digit_sums))

    # Analyze digit products
    product_frequencies = dict(Counter(digit_products))

    return {
        "digit_frequencies": digit_frequencies,
        "repeating_digits": repeating_digits,
        "digit_sums": sum_frequencies,
        "digit_products": product_frequencies
    }


def detect_sum_patterns(draws: List[List[int]]) -> Dict[str, any]:
    """
    Detect patterns in the sum of numbers in each draw.

    Args:
        draws: List of draws (each draw is a list of numbers)

    Returns:
        Dictionary with sum pattern analysis
    """
    if not draws:
        return {
            "sum_range": (0, 0),
            "most_common_sums": {},
            "sum_distribution": {}
        }

    sums = []
    for draw in draws:
        if not draw:
            continue
        try:
            # Convert to integers if strings
            if isinstance(draw[0], str):
                draw_nums = [int(x.strip()) for x in draw if x.strip()]
            else:
                draw_nums = draw

            draw_sum = sum(draw_nums)
            sums.append(draw_sum)
        except (ValueError, TypeError):
            continue

    if not sums:
        return {
            "sum_range": (0, 0),
            "most_common_sums": {},
            "sum_distribution": {}
        }

    min_sum = min(sums)
    max_sum = max(sums)

    # Most common sums
    sum_counter = Counter(sums)
    most_common_sums = dict(sum_counter.most_common(10))

    # Sum distribution
    sum_distribution = dict(sum_counter)

    return {
        "sum_range": (min_sum, max_sum),
        "most_common_sums": most_common_sums,
        "sum_distribution": sum_distribution
    }


def analyze_patterns(
    session: SessionLocal,
    game_type: str = "lotto",
    window_days: Optional[int] = None
) -> Dict[str, any]:
    """
    Comprehensive pattern analysis for lottery draws.

    Args:
        session: Database session
        game_type: Type of game to analyze
        window_days: Number of days to look back

    Returns:
        Dictionary containing all pattern analysis results
    """
    # Get recent draws
    repo = DrawRepository(session)
    draws = repo.list(limit=1000, game_type=game_type)  # Get last 1000 draws

    if not draws:
        return {
            "error": "No draws found for analysis"
        }

    # Extract all numbers from draws
    all_numbers = []
    for draw in draws:
        if 'numbers' in draw and isinstance(draw['numbers'], str):
            try:
                numbers = [int(x.strip()) for x in draw['numbers'].split(',') if x.strip()]
                all_numbers.extend(numbers)
            except (ValueError, TypeError):
                continue  # Skip invalid draws

    if not all_numbers:
        return {
            "error": "No valid numbers found in draws"
        }

    # Perform all pattern analyses
    consecutive = detect_consecutive_numbers(all_numbers, min_length=2)

    # Prepare draws for arithmetic sequences
    draws_for_arithmetic = []
    for draw in draws:
        if 'numbers' in draw and isinstance(draw['numbers'], str):
            try:
                numbers = [int(x.strip()) for x in draw['numbers'].split(',') if x.strip()]
                draws_for_arithmetic.append(numbers)
            except (ValueError, TypeError):
                continue

    arithmetic = detect_arithmetic_sequences(draws_for_arithmetic, min_length=3)
    digits = detect_digit_patterns(all_numbers)

    # Prepare draws for sum patterns
    draws_for_sums = []
    for draw in draws:
        if 'numbers' in draw and isinstance(draw['numbers'], str):
            try:
                numbers = [int(x.strip()) for x in draw['numbers'].split(',') if x.strip()]
                draws_for_sums.append(numbers)
            except (ValueError, TypeError):
                continue

    sums = detect_sum_patterns(draws_for_sums)

    return {
        "game_type": game_type,
        "window_days": window_days,
        "total_draws_analyzed": len(draws),
        "total_numbers_analyzed": len(all_numbers),
        "consecutive_numbers": consecutive,
        "arithmetic_sequences": arithmetic,
        "digit_patterns": digits,
        "sum_patterns": sums
    }
