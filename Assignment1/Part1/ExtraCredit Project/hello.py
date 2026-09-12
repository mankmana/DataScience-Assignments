print("Hello, World!")


def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def add_two_integers(a: int, b: int) -> int:
    """Alias for adding two integers."""
    return add(a, b)
