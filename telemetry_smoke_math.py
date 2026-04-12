"""Telemetry smoke test: minimal math utility for delegate verification."""


def sum_float(*args: float) -> float:
    """Return the sum of all provided float arguments."""
    return float(sum(args))


if __name__ == "__main__":
    result = sum_float(1.5, 2.5, 3.0)
    print(f"sum_float(1.5, 2.5, 3.0) = {result}")
