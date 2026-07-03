from lib.task1 import golden_ratio_method
from lib.task2 import midpoint_method
from lib.task3 import newton_method
import math

def f(x):
  return math.log(1+x**2)-math.sin(x)

def d1(x):
  return 2 * x / (1 + x ** 2) - math.cos(x)

def d2(x):
  return 2*(1-x**2)/(1+ x ** 2) ** 2 + math.sin(x)

a, b = 0, math.pi / 4
eps = 0.001

with open('1.csv', 'w') as f1:
  print("1. Запускаем метод нулевого порядка.")
  x = golden_ratio_method(f, a, b, eps, f1)
  print(f"Ответ: x*={x:.7f}, f(x*)={f(x)}")
with open('2.csv', 'w') as f2:
  print("2. Запускаем метод первого порядка.")
  x = midpoint_method(d1, a, b, eps, f2)
  print(f"Ответ: x*={x:.7f}, f(x*)={f(x)}")
with open('3.csv', 'w') as f3:
  print("3. Запускаем метод второго порядка.")
  x = newton_method(d1, d2, a, b, eps, f3)
  print(f"Ответ: x*={x:.7f}, f(x*)={f(x)}")