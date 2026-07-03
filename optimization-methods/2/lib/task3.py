from typing import Callable, IO
import csv

def newton_method(deriv_first: Callable[[float], float],
                  deriv_second: Callable[[float], float],
                  a: float, b: float,
                  eps: float, f: IO[str]) -> float:
  writer = csv.writer(f)
  writer.writerow(["k", "x", "x_prev", "f'(x_prev)", "f''(x_prev)", "f'(x)"])

  k = 1
  x = (a + b) / 2 # можно эффективнее
  # точка останова
  d1 = deriv_first(x)
  while abs(d1) > eps:
    if x < a or x > b:
      print("error: x вышел за пределы отрезка.")
      break
    d2 = deriv_second(x)

    x_prev = x
    x -= d1 / d2
    d1_prev = d1
    d1 = deriv_first(x)

    writer.writerow([k, f"{x:.6f}", f"{x_prev:.6f}", f"{d1_prev:.6f}", f"{d2:.6f}", f"{d1:.6f}"])

    k += 1
  return x