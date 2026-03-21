from typing import Callable
from lib.models import Point

def calc_parabola_coeffs(p1: Point, p2: Point, p3: Point) -> tuple[float, float, float]:
  denom = (p1.x - p2.x) * (p1.x - p3.x) * (p2.x - p3.x)
  if abs(denom) < 1e-12:
    return 0.0, 0.0, 0.0
  a = (p3.x * (p2.y - p1.y) + p2.x * (p1.y - p3.y) + p1.x * (p3.y - p2.y)) / denom
  b = (p3.x**2 * (p1.y - p2.y) + p2.x**2 * (p3.y - p1.y) + p1.x**2 * (p2.y - p3.y)) / denom
  c = (p2.x * p3.x * (p2.x - p3.x) * p1.y + p3.x * p1.x * (p3.x - p1.x) * p2.y + p1.x * p2.x * (p1.x - p2.x) * p3.y) / denom
  return a, b, c

def calc_x2_initial(x1: float, x3: float, func: Callable[[float], float]) -> tuple[float, float]:
  f1 = func(x1)
  f3 = func(x3)
  n = 10000
  step = (x3 - x1) / n
  candidates = list()
  for i in range(2, n):
    x2 = x1 + i * step
    f2 = func(x2)
    if f2 <= f1 and f2 <= f3:
      candidates.append(x2)
  if len(candidates) == 0:
    raise ValueError("No candidates for x2: function is possibly not unimodal.")
  x2 = candidates[0]
  min_x_delta = abs(x1 - x2)
  for x in candidates[1:]:
    m = min(abs(x - x1), abs(x - x3))
    if m > min_x_delta:
      x2 = x
      min_x_delta = m
  return x2, func(x2)

def calc_x_star(x1: float, x2: float, x3: float, f1: float, f2: float, f3: float) -> float:
  r23 = x2**2 - x3**2
  r31 = x3**2 - x1**2
  r12 = x1**2 - x2**2
  s23 = x2 - x3
  s31 = x3 - x1
  s12 = x1 - x2
  num = f1 * r23 + f2 * r31 + f3 * r12
  den = f1 * s23 + f2 * s31 + f3 * s12
  if abs(den) < 1e-12:
    return x2
  return 0.5 * (num / den)

def get_true_min(a: float, b: float, func: Callable[[float], float]) -> tuple[float, float]:
  n = 12500
  step = (b - a) / n
  min_x = a
  min_f = func(a)
  for i in range(1, n + 1):
    x = a + i * step
    val = func(x)
    if val < min_f:
      min_f = val
      min_x = x
  return min_x, min_f