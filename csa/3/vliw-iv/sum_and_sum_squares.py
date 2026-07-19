def sum_and_sum_squares(*xs):
    """Input: first word N, then N values.

    Output: two words: sum(X) and sum(x*x for x in X).
    """
    n = xs[0]
    if n < 0:
        return [-1]

    total = 0
    square_total = 0
    for i in range(n):
        x = xs[1 + i]
        total += x
        square_total += x * x

    if (
        total < -0x80000000
        or total > 0x7FFFFFFF
        or square_total < -0x80000000
        or square_total > 0x7FFFFFFF
    ):
        return [0xCCCCCCCC]

    return [total, square_total]


assert sum_and_sum_squares(0) == [0, 0]
assert sum_and_sum_squares(3, 1, 2, 3) == [6, 14]
assert sum_and_sum_squares(4, -2, 5, 0, -3) == [0, 38]
assert sum_and_sum_squares(5, 10, 20, 30, 40, 50) == [150, 5500]