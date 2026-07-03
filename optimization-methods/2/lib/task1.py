from functools import cache
from typing import Callable, IO
import math, csv

@cache
def fib(n):
  if n == 1:
    return 1
  if n == 2:
    return 1
  return fib(n - 1) + fib(n - 2)

def interval_halving_method(func: Callable[[float], float],
                            a: float, b: float,
                            eps: float, f: IO[str]) -> float:
  writer = csv.writer(f)
  writer.writerow(["k", "a", "b", "L_k", "mid_left", "mid_right", "f_left", "f_right"])
  k = 1
  while True:
    # критерий останова
    L_k = b - a
    if L_k <= 2 * eps:
      break
    mid_left = (a + b - eps) / 2
    mid_right = (a + b + eps) / 2

    f_left = func(mid_left)
    f_right = func(mid_right)

    writer.writerow([k, f"{a:.6f}", f"{b:.6f}", f"{L_k:.6f}", 
                        f"{mid_left:.6f}", f"{mid_right:.6f}", 
                        f"{f_left:.6f}", f"{f_right:.6f}"])
    # процедура исключения отрезка
    if f_left < f_right:
      b = mid_right
    elif f_left > f_right:
      a = mid_left
    else:
      print("error: не найден промежуток определённости")
      break
    k += 1
  return (a + b) / 2

def golden_ratio_method(func: Callable[[float], float],
                        a: float, b: float,
                        eps: float, f: IO[str]) -> float:
  writer = csv.writer(f)
  writer.writerow(["k", "a", "b", "L_k", "x1", "x2", "f_x1", "f_x2"])
  k = 1
  tau = (math.sqrt(5) - 1) / 2
  x1 = b - (b - a) * tau
  x2 = a + (b - a) * tau
  f_x1 = func(x1)
  f_x2 = func(x2)
  while True:
    L_k = b - a
    # критерий останова
    if L_k <= eps:
      break

    writer.writerow([k, f"{a:.6f}", f"{b:.6f}", f"{L_k:.6f}", 
                        f"{x1:.6f}", f"{x2:.6f}", 
                        f"{f_x1:.6f}", f"{f_x2:.6f}"])
    # процедура исключения отрезка
    if f_x1 > f_x2:
      a = x1
      x1 = x2
      f_x1 = f_x2
      x2 = a + tau * (b - a)
      f_x2 = func(x2)
    elif f_x1 < f_x2:
      b = x2
      x2 = x1
      f_x2 = f_x1
      x1 = b - tau * (b - a)
      f_x1 = func(x1)
    else:
      print("error: не найден промежуток определённости")
      break
    k += 1
  return (a + b) / 2

def fibonacci_method(func: Callable[[float], float],
                     a: float, b: float,
                     eps: float, f: IO[str]) -> float:
  writer = csv.writer(f)
  writer.writerow(["k", "a", "b", "L_k", "x1", "x2", "f_x1", "f_x2"])
  n = 1
  # критерий останова
  while (b - a) / fib(n) > eps:
    n += 1
  
  def calc_x1(k):
    return a + fib(n - k) * (b - a) / fib(n - k + 1)
  def calc_x2(k):
    return a +  fib(n - k - 1) * (b - a) / fib(n - k + 1)

  x1 = calc_x1(1)
  x2 = calc_x2(2)
  for k in range(1, n + 1):
    L_k = b - a
    f_x1 = func(x1)
    f_x2 = func(x2)

    writer.writerow([k, f"{a:.6f}", f"{b:.6f}", f"{L_k:.6f}", 
                        f"{x1:.6f}", f"{x2:.6f}", 
                        f"{f_x1:.6f}", f"{f_x2:.6f}"])
    # процедура исключения отрезка
    if f_x1 < f_x2:
      b = x2
      x2 = x1
      x1 = calc_x1(k)
    elif f_x1 > f_x2:
      a = x1
      x1 = x2
      x2 = calc_x2
    else:
      print("error: не найден промежуток определённости")
      break
  return (a + b) / 2