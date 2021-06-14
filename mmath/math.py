import math


def v_avg(*nums: int or float) -> float:
    """Compute the average for a variable amount of numbers.

    Args:
        nums: numbers to compute average for.

    Returns:
        Average of nums."""
    return sum(nums) / len(nums)


def cosine_rule(v_original: float, v_target: float, angle_dif: int) -> float:
    """Apply the cosign rule to compute the Delta-V needed to transfer from one velocity
    to another with a difference in angle.

    Args:
        v_original: the original velocity.
        v_target: the target velocity.
        angle_dif: the angle at which the 2 velocities differ in degrees.

    Returns:
        the length of the velocity vector connecting the 2 ends of v_original and v_target."""
    return (((v_original ** 2) + (v_target ** 2)) -
            (2 * v_original * v_target * math.cos(math.radians(angle_dif)))) ** (1/2)
