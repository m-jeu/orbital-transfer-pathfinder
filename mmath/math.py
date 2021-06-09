def v_avg(*nums: int or float) -> float:
    """Compute the average for a variable amount of numbers.

    Args:
        nums: numbers to compute average for.

    Returns:
        Average of nums."""
    return sum(nums) / len(nums)