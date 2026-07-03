from lib.math_utils import Vector

class QuadraticFunction:
  def __init__(self, a, b, c, d, e, f):
    self.a = a
    self.b = b
    self.c = c
    self.d = d
    self.e = e
    self.f = f
    
  def evaluate(self, v: Vector):
    x, y = v[0], v[1]
    return self.a * x**2 + self.b * y**2 + self.c * x * y + self.d * x + self.e * y + self.f
    
  def gradient(self, v: Vector):
    x, y = v[0], v[1]
    dx = 2 * self.a * x + self.c * y + self.d
    dy = 2 * self.b * y + self.c * x + self.e
    return Vector(dx, dy)
  
  def get_extremum(self):
    x_star = (self.e * self.c - 2 * self.b * self.d) / (4 * self.a * self.b - self.c ** 2)
    y_star = -(self.c * x_star + self.e) / (2 * self.b)
    return Vector(x_star, y_star)
  
  def minor(self, number: int):
    match number:
      case 1:
        return 2 * self.a
      case 2:
        return 4 * self.a * self.b - self.c ** 2
      case _:
        raise ValueError
    
  def minimize_1d(self, origin: Vector, direction: Vector):
    x0, y0 = origin[0], origin[1]
    u, v = direction[0], direction[1]
    
    numerator = 2 * self.a * x0 * u + 2 * self.b * y0 * v + self.c * (x0 * v + y0 * u) + self.d * u + self.e * v
    denominator = 2 * self.a * u**2 + 2 * self.b * v**2 + 2 * self.c * u * v
    
    if denominator == 0:
      return 0.0
      
    return -numerator / denominator