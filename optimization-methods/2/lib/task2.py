from typing import Callable, IO
import csv

def midpoint_method(deriv: Callable[[float], float],
                  a: float, b: float,
                  eps: float, f: IO[str]) -> float:
  writer = csv.writer(f)
  writer.writerow(["k", "a", "b", "x", "f'(x)", "L_k"])

  k = 1
  while True:
    x = (a + b) / 2
    d_x = deriv(x)

    writer.writerow([k, f"{a:.6f}", f"{b:.6f}", f"{x:.6f}", f"{d_x:.6f}", f"{b-a:.6f}"])

    # точка останова
    if abs(d_x) <= eps:
      break
    if d_x > 0:
      b = x
    else:
      a = x
    k += 1
  return x

def chord_method(deriv: Callable[[float], float],
                  a: float, b: float,
                  eps: float, f: IO[str]) -> float:
  writer = csv.writer(f)
  writer.writerow(["k", "a", "b", "x", "f'(x)", "L_k"])

  k = 1
  while True:
    x = a - deriv(a) * (b - a) / (deriv(b) - deriv(a))
    d_x = deriv(x)

    writer.writerow([k, f"{a:.6f}", f"{b:.6f}", f"{x:.6f}", f"{d_x:.6f}", f"{b-a:.6f}"])

    # точка останова
    if abs(d_x) <= eps:
      break
    if d_x > 0:
      b = x
    else:
      a = x
    k += 1
  return x