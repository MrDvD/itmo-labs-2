import numpy as np
from typing import List, Tuple, Protocol, runtime_checkable
from abc import ABC

@runtime_checkable
class OptimizerProtocol(Protocol):
  iter_history: List[Tuple[float, float]]
  def optimize(self, params_start: Tuple[float, float]) -> List[float]: ...

class BaseOptimizer(ABC):
  def __init__(self) -> None:
    self.iter_history: List[Tuple[float, float]] = list()

  def _callback(self, x: Tuple[float, float]) -> None:
    self.iter_history.append(x)

class GradientDescentOptimizer(BaseOptimizer):
  def __init__(self, learning_rate: float, max_iter: int, eps: float) -> None:
    super().__init__()
    self.learning_rate = learning_rate
    self.max_iter = max_iter
    self.eps = eps
  
  def _get_gradient(self, params: np.ndarray) -> np.ndarray:
    x, y = params[0], params[1]
    df_dx = 10**-2 * (16 * x + 2 * y + 43)
    df_dy = 10**-2 * (2 * x + 10)
    return np.array([df_dx, df_dy], dtype=float)

  def optimize(self, params_start: Tuple[float, float]) -> List[Tuple[float, float]]:
    params = np.array(params_start, dtype=float)
    self.iter_history = [tuple(params)]
    for _ in range(self.max_iter):
      grad = self._get_gradient(params)
      if np.linalg.norm(grad) < self.eps:
        break
      next_params = params - self.learning_rate * grad
      self._callback(tuple(next_params))
      if np.linalg.norm(next_params - params) < self.eps:
        params = next_params
        break
      params = next_params
    return self.iter_history