from typing import Optional

class Point:
  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y

class State:
  def __init__(self, k: int, x1: float, x2: float, x3: float, f1: float, f2: float, f3: float) -> None:
    self.k = k
    self.x1 = x1
    self.x2 = x2
    self.x3 = x3
    self.f1 = f1
    self.f2 = f2
    self.f3 = f3
    self.x_star: Optional[float] = None
    self.f_star: Optional[float] = None
    self.condition: Optional[str] = None