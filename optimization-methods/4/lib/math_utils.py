import math

class Vector:
  def __init__(self, *components):
    self.components = list(components)
    
  def __add__(self, other):
    return Vector(*[a + b for a, b in zip(self.components, other.components)])
    
  def __sub__(self, other):
    return Vector(*[a - b for a, b in zip(self.components, other.components)])
    
  def __mul__(self, scalar):
    return Vector(*[a * scalar for a in self.components])
    
  def __rmul__(self, scalar):
    return self.__mul__(scalar)
    
  def dot(self, other):
    return sum(a * b for a, b in zip(self.components, other.components))
    
  def norm(self):
    return math.sqrt(sum(a**2 for a in self.components))
    
  def normalize(self):
    n = self.norm()
    if n == 0:
      return self
    return self * (1.0 / n)
    
  def __getitem__(self, index):
    return self.components[index]
    
  def __len__(self):
    return len(self.components)
    
  def to_latex(self, precision):
    coords = ", ".join([f"{x:.{precision}f}" for x in self.components])
    return f"({coords})^T"