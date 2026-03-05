import math


def compute_bracket_size(n: int) -> int:
    """
    Compute the nearest power-of-two bracket size for n participants.

    If n is exactly a power of two, returns n (no BYEs, no cuts).
    If n is closer to the lower power → lower bracket (bottom participants cut).
    If n is closer to the upper power or equidistant → upper bracket (BYEs for top seeds).
    """
    lower = 2 ** math.floor(math.log2(n))
    if lower == n:
        return n
    upper = lower * 2
    if n - lower < upper - n:
        return lower
    return upper
