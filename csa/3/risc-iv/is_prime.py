def is_prime(n):
    """Check if a natural number is prime"""
    if n < 1:
        return -1
    if n == 1:
        return 0
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return 0
    return 1

def sqrt(n, l, r):
    if l == r:
        return r
    mid = l + ((r - l) >> 1)
    x = mid * mid
    if x == n:
        return mid
    if x > n:
        return sqrt(n, l, mid)
    return sqrt(n, mid + 1, r)

def is_prime_recursive(n):
    if n < 1:
        return -1
    
    if n == 1:
        return 0
    
    if n == 2:
        return 1

    return div(n, sqrt(n, 1, n), 2)

def div(n, sqrt_n, divider):
  if sqrt_n == divider:
      return n % divider > 0

  if n % divider == 0:
      return 0
  else:
      return div(n, sqrt_n, divider + 1)

assert is_prime_recursive(2) == 1
assert is_prime_recursive(3) == 1
assert is_prime_recursive(4) == 0
assert is_prime_recursive(5) == 1
assert is_prime_recursive(4) == 0
assert is_prime_recursive(7) == 1
assert is_prime_recursive(8) == 0
assert is_prime_recursive(283) == 1
assert is_prime_recursive(284) == 0
assert is_prime_recursive(293) == 1

assert sqrt(17, 0, 17 >> 1) == 5
assert sqrt(14, 0, 14 >> 1) == 4
assert sqrt(16, 0, 16 >> 1) == 4
assert sqrt(13, 0, 13 >> 1) == 4
assert sqrt(100, 0, 100 >> 1) == 10
assert sqrt(101, 0, 101 >> 1) == 11